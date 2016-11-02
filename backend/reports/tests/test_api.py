import json

from django.forms import model_to_dict
from django.urls import reverse
from model_mommy import mommy
from rest_framework import status
from rest_framework.test import APITestCase

from backend.accounts.tests.test_api import get_jwt_token
from ..models import Report


class UserAuthReportApiTest(APITestCase):
    def setUp(self):
        self.user = mommy.make_recipe('backend.core.user')
        self.login = self.client.login(username=self.user.username, password='leo')
        self.report = mommy.make_one(Report, user=self.user)
        self.jwt_authorization = get_jwt_token(self.user)

    def test_user_is_authenticated(self):
        """
        Check if user is authenticated
        """
        self.assertTrue(self.login)

    def test_user_can_use_api(self):
        """
        User can use report endpoints
        """
        urls = (reverse('report-list'), reverse('report-detail', kwargs={'pk': self.report.pk}))
        with self.subTest():
            for expected in urls:
                response = self.client.get(expected, HTTP_AUTHORIZATION=self.jwt_authorization)
                self.assertEqual(200, response.status_code)


class UserAuthErrorsReportApiTest(APITestCase):
    def setUp(self):
        self.report = mommy.make_one(Report)

    def test_user_cant_use_api(self):
        """
        Check if user has a INVALID JWT TOKEN authorizated else must return status code 401 NOT AUTHORIZATED
        """
        urls = (reverse('report-list'), reverse('report-detail', kwargs={'pk': self.report.pk}))
        with self.subTest():
            for expected in urls:
                response = self.client.get(expected)
                self.assertEqual(401, response.status_code)


class CreateReportApiTest(APITestCase):
    def setUp(self):
        city = mommy.make_recipe('backend.core.city')
        user = mommy.make_recipe('backend.core.user')
        report = mommy.prepare_one(Report, city=city, user=user, _fill_optional=True)
        jwt_authorization = get_jwt_token(user)
        self.data = model_to_dict(report)
        self.resp = self.client.post(reverse('report-list'), self.data, HTTP_AUTHORIZATION=jwt_authorization)

    def test_create_report(self):
        """
        POST /api/v1/reports/ must return status code 201 CREATED and
        return data created
        """
        response_data = json.loads(self.resp.content.decode('utf8'))
        expected_fields = {'user', 'city', 'number'}
        with self.subTest():
            for expected_field in expected_fields:
                self.assertEquals(self.data[expected_field], response_data[expected_field])
        self.assertEqual(self.resp.status_code, status.HTTP_201_CREATED)

    def test_save_report(self):
        """
        Check if report has been saved
        """
        self.assertTrue(Report.objects.exists())


class CreateInvalidReportApiTest(APITestCase):
    def setUp(self):
        user = mommy.make_recipe('backend.core.user')
        jwt_authorization = get_jwt_token(user)
        data = {'description': 'Invalid report'}
        self.resp = self.client.post(reverse('report-list'), data, HTTP_AUTHORIZATION=jwt_authorization)

    def test_create_invalid_report(self):
        """
        POST invalid report at /api/v1/reports/
        Must return status code 400 BAD REQUEST
        """
        self.assertEqual(400, self.resp.status_code)

    def test_has_errors(self):
        """
        Context must return errors
        """
        self.assertTrue(self.resp.data.serializer.errors)

    def test_save_invalid_report(self):
        """
        Check if invalid report has not been saved
        """
        self.assertFalse(Report.objects.exists())


class ReadReportApiTest(APITestCase):
    def setUp(self):
        group = mommy.make_recipe('backend.core.group', name='Agente')
        user = mommy.make_recipe('backend.core.user')
        user2 = mommy.make_recipe('backend.core.user', username='test_user2')
        super_user = mommy.make_recipe('backend.core.user', username='superuser', is_superuser=True)

        ''' Create a agent user with group Agente'''
        agent_user = mommy.make_recipe('backend.core.user', username='test_agent')
        agent_user.groups.add(group)
        agent_user.save()

        self.jwt_authorizations = {
            'user_1': get_jwt_token(user),
            'user_2': get_jwt_token(user2),
            'agent_user': get_jwt_token(agent_user),
            'super_user': get_jwt_token(super_user)
        }

        self.report1 = mommy.make_one(Report, description='have things here', user=user, status=1)
        self.report2 = mommy.make_one(Report, description='have two things here', user=user, status=2)
        self.report_user2 = mommy.make_one(Report, description='I am user 2', user=user2, status=1)

    def test_read_report_list(self):
        """
        GET at /api/v1/reports/
        Must return status code 200 OK and
        check if reports are being shown
        """
        response = self.client.get(reverse('report-list'), HTTP_AUTHORIZATION=self.jwt_authorizations['user_1'])
        self.assertEqual(200, response.status_code)
        self.assertContains(response, self.report1.description)
        self.assertContains(response, self.report2.description)

    def test_read_valid_report_details(self):
        """
        GET at /api/v1/reports/report_id
        Must return status code 200 OK and
        check if reports are being shown
        """
        response = self.client.get(reverse('report-detail', kwargs={'pk': self.report1.pk}),
                                   HTTP_AUTHORIZATION=self.jwt_authorizations['user_1'])
        self.assertEqual(200, response.status_code)
        self.assertContains(response, self.report1.description)

    def test_can_read_only_own_reports(self):
        """
        GET at /api/v1/reports/
        Must return status code 200 OK and
        certify that only own reports are being shown
        """
        response = self.client.get(reverse('report-list'), HTTP_AUTHORIZATION=self.jwt_authorizations['user_2'])
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['user'], self.report_user2.user.pk)

    def test_agent_can_read_all_reports(self):
        """
        GET at /api/v1/reports/
        Must return all reports if user is superuser or agent
        and check if all reports are being shown
        """
        users_token = [self.jwt_authorizations['agent_user'], self.jwt_authorizations['super_user']]
        with self.subTest():
            for expected in users_token:
                response = self.client.get(reverse('report-list'),
                                           HTTP_AUTHORIZATION=expected)
                self.assertEqual(len(response.data), 3)
                self.assertContains(response, self.report1.description)
                self.assertContains(response, self.report2.description)
                self.assertContains(response, self.report_user2.description)


class ReadReportDetailErrorsApiTest(APITestCase):
    def setUp(self):
        user = mommy.make_recipe('backend.core.user')
        self.jwt_authorization = get_jwt_token(user)

    def test_read_invalid_report(self):
        """
        GET invalid report_id at /api/v1/reports/report_id
        Must return status code 404 NOT FOUND
        """
        response = self.client.get(reverse('report-detail', kwargs={'pk': 0}),
                                   HTTP_AUTHORIZATION=self.jwt_authorization)
        self.assertEqual(404, response.status_code)

    def test_not_read_other_report_details(self):
        """
        User can't read other report details that which aren't his
        GET at /api/v1/reports/
        Must return status code 403 FORBIDDEN
        """
        other_user = mommy.make_recipe('backend.core.user', username='leonardo2')
        report = mommy.make_one(Report, user=other_user)
        response = self.client.get(reverse('report-detail', kwargs={'pk': report.pk}),
                                   HTTP_AUTHORIZATION=self.jwt_authorization)
        self.assertEqual(403, response.status_code)


class UpdateReportApiTest(APITestCase):
    def setUp(self):
        user = mommy.make_recipe('backend.core.user')
        self.jwt_authorization = get_jwt_token(user)
        self.report = mommy.make_one(Report, city__name='Bom Despacho', user=user, _fill_optional=True)

    def test_update_report(self):
        """
        PUT /api/v1/reports/report_id/ must return status code 200 OK and
        return data updated
        """
        self.report.description = 'Changed'
        data = model_to_dict(self.report)
        response = self.client.put(reverse('report-detail', kwargs={'pk': self.report.pk}), data,
                                   HTTP_AUTHORIZATION=self.jwt_authorization)
        response_data = json.loads(response.content.decode('utf8'))
        self.assertEqual(200, response.status_code)
        self.assertEqual(response_data['description'], 'Changed')


class UpdateInvalidReportApiTest(APITestCase):
    def setUp(self):
        user = mommy.make_recipe('backend.core.user')
        jwt_authorization = get_jwt_token(user)
        self.report = mommy.make_one(Report, city__name='Bom Despacho', user=user, _fill_optional=True)
        self.report.city = None
        data = model_to_dict(self.report)
        self.resp = self.client.put(reverse('report-detail', kwargs={'pk': self.report.pk}), data,
                                    HTTP_AUTHORIZATION=jwt_authorization)

    def test_update_invalid_report(self):
        """
        PUT invalid report at /api/v1/reports/report_id/
        Must return status code 400 BAD REQUEST
        """
        self.assertEqual(400, self.resp.status_code)

    def test_has_errors(self):
        """
        Context must return errors
        """
        self.assertTrue(self.resp.data.serializer.errors)

    def test_save_invalid_report(self):
        """
        Check if invalid updated report has not been saved
        """
        original_report = Report.objects.get(pk=self.report.pk)
        self.assertTrue(original_report.city)


class DeleteReportApiTest(APITestCase):
    def setUp(self):
        user = mommy.make_recipe('backend.core.user')
        self.jwt_authorization = get_jwt_token(user)
        self.report = mommy.make_one(Report, city__name='Bom Despacho', user=user)

    def test_delete_report(self):
        """
        DELETE at /api/v1/reports/report_id/
        Must return status code 204 NO CONTENT
        """
        response = self.client.delete(reverse('report-detail', kwargs={'pk': self.report.pk}),
                                      HTTP_AUTHORIZATION=self.jwt_authorization)
        self.assertEqual(204, response.status_code)

