import json

from django.forms import model_to_dict
from django.urls import reverse
from model_mommy import mommy
from rest_framework import status
from rest_framework.test import APITestCase
from ..models import Report


class UserAuthReportApiTest(APITestCase):
    def setUp(self):
        self.user = mommy.make_recipe('backend.core.user')
        self.login = self.client.login(username=self.user.username, password='leo')
        self.report = mommy.make_one(Report, user=self.user)

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
                response = self.client.get(expected)
                self.assertEqual(200, response.status_code)


class UserAuthErrorsReportApiTest(APITestCase):
    def setUp(self):
        self.report = mommy.make_one(Report)

    def test_user_is_not_authenticated(self):
        """
        Check if user is authenticated else must return status code 403 FORBIDDEN
        """
        urls = (reverse('report-list'), reverse('report-detail', kwargs={'pk': self.report.pk}))
        with self.subTest():
            for expected in urls:
                response = self.client.get(expected)
                self.assertEqual(403, response.status_code)


class CreateReportApiTest(APITestCase):
    def setUp(self):
        city = mommy.make_recipe('backend.core.city')
        user = mommy.make_recipe('backend.core.user')
        report = mommy.prepare_one(Report, city=city, user=user)
        self.data = model_to_dict(report)
        self.client.login(username=user.username, password='leo')
        self.resp = self.client.post(reverse('report-list'), self.data)

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
        self.client.login(username=user.username, password='leo')
        data = {'description': 'Invalid report'}
        self.resp = self.client.post(reverse('report-list'), data)

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
        user = mommy.make_recipe('backend.core.user')
        self.login = self.client.login(username=user.username, password='leo')
        mommy.make_one(Report, description='have things here', user=user)
        mommy.make_one(Report, description='have two things here', user=user)

    def test_read_report_list(self):
        """
        GET at /api/v1/reports/
        Must return status code 200 OK and
        check if reports are being shown
        """
        response = self.client.get(reverse('report-list'))
        self.assertEqual(200, response.status_code)
        self.assertContains(response, "have things here")
        self.assertContains(response, "have two things here")

    def test_read_valid_report_details(self):
        """
        GET at /api/v1/reports/report_id
        Must return status code 200 OK and
        check if reports are being shown
        """
        response = self.client.get(reverse('report-detail', kwargs={'pk': 1}))
        self.assertEqual(200, response.status_code)
        self.assertContains(response, "have things here")


class ReadReportDetailErrorsApiTest(APITestCase):
    def setUp(self):
        user = mommy.make_recipe('backend.core.user')
        self.client.login(username=user.username, password='leo')

    def test_read_invalid_report(self):
        """
        GET invalid report_id at /api/v1/reports/report_id
        Must return status code 404 NOT FOUND
        """
        response = self.client.get(reverse('report-detail', kwargs={'pk': 0}))
        self.assertEqual(404, response.status_code)

    def test_not_read_other_report_details(self):
        """
        User can't read other report details that which aren't his
        GET at /api/v1/reports/
        Must return status code 403 FORBIDDEN
        """
        other_user = mommy.make_recipe('backend.core.user', username='leonardo2')
        report = mommy.make_one(Report, user=other_user)
        response = self.client.get(reverse('report-detail', kwargs={'pk': report.pk}))
        self.assertEqual(403, response.status_code)


class UpdateReportApiTest(APITestCase):
    def setUp(self):
        user = mommy.make_recipe('backend.core.user')
        self.client.login(username=user.username, password='leo')
        self.report = mommy.make_one(Report, city__name='Bom Despacho', user=user)
        self.report.description = 'Changed'

    def test_update_report(self):
        """
        PUT /api/v1/reports/report_id/ must return status code 200 OK and
        return data updated
        """
        data = model_to_dict(self.report)
        response = self.client.put(reverse('report-detail', kwargs={'pk': self.report.pk}), data)
        response_data = json.loads(response.content.decode('utf8'))
        self.assertEqual(200, response.status_code)
        self.assertEqual(response_data['description'], 'Changed')


class UpdateInvalidReportApiTest(APITestCase):
    def setUp(self):
        user = mommy.make_recipe('backend.core.user')
        self.client.login(username=user.username, password='leo')
        self.report = mommy.make_one(Report, city__name='Bom Despacho', user=user)
        self.report.city = None
        data = model_to_dict(self.report)
        self.resp = self.client.put(reverse('report-detail', kwargs={'pk': self.report.pk}), data)

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
        self.login = self.client.login(username=user.username, password='leo')
        self.report = mommy.make_one(Report, city__name='Bom Despacho', user=user)

    def test_delete_report(self):
        """
        DELETE at /api/v1/reports/report_id/
        Must return status code 204 NO CONTENT
        """
        response = self.client.delete(reverse('report-detail', kwargs={'pk': self.report.pk}))
        self.assertEqual(204, response.status_code)

