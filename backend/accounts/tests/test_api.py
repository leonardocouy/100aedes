import json

from django.urls import reverse
from django.forms.models import model_to_dict
from rest_framework import status
from rest_framework.test import APITestCase
from model_mommy import mommy
from rest_framework_jwt import utils

from backend.core.utils import get_jwt_token
from backend.core.models import City
from ..models import User
from ..serializers import UserSerializer


class AuthTest(APITestCase):
    def setUp(self):
        city = mommy.make_recipe('backend.core.city')
        self.user = mommy.make_recipe('backend.core.user', city=city)
        data = {'username': self.user.username, 'password': 'leo'}
        self.response = self.client.post(reverse('auth-user'), data)

    def test_get_valid_token(self):
        """
        Valid login user POST at /api/v1/users/auth must return status code 200 OK and
        return valid token to the authenticated user
        """

        decoded_payload = utils.jwt_decode_handler(self.response.data['token'])
        self.assertEqual(200, self.response.status_code)
        self.assertEqual(decoded_payload['username'], self.user.username)

    def test_user_fields(self):
        """
        Check if users fields has been returning
        """
        expected_fields = UserSerializer(self.user).get_fields()
        with self.subTest():
            for expected in expected_fields:
                self.assertEquals(UserSerializer(self.user).data[expected], self.response.data['user'][expected])


class InvalidAuthTest(APITestCase):
    def setUp(self):
        city = mommy.make_recipe('backend.core.city')
        self.user = mommy.make_recipe('backend.core.user', city=city)

    def test_invalid_login(self):
        """
        Invalid login user POST at /api/v1/users/auth must return status code 400 BAD REQUEST and
        return errors
        """
        data = {'username': self.user.username, 'password': 'INVALID_PASSWORD_TO_FAIL_TEST'}
        response = self.client.post(reverse('auth-user'), data)
        self.assertEqual(400, response.status_code)
        self.assertTrue(response.data['non_field_errors'])


class CreateUserTest(APITestCase):
    def setUp(self):
        city = City.objects.create(name='TestLand', state='PR')
        self.user = mommy.prepare_recipe('backend.core.user', city=city)
        self.data = model_to_dict(self.user)
        self.resp = self.client.post(reverse('user'), self.data)

    def test_create_user(self):
        """
        POST /api/v1/users/ must return status code 201 CREATED and
        return data created
        """
        expected_fields = {'city', 'email', 'first_name', 'last_name', 'first_name', 'username'}
        response_data = json.loads(self.resp.content.decode('utf8'))
        self.assertEqual(self.resp.status_code, status.HTTP_201_CREATED)
        with self.subTest():
            for expected in expected_fields:
                self.assertEquals(self.data[expected], response_data[expected])

    def test_save_user(self):
        """
        Check if user has been saved
        """
        self.assertTrue(User.objects.exists())

    def test_return_token_after_registration(self):
        """
        Check if token has been returning after registration
        """
        response_data = json.loads(self.resp.content.decode('utf8'))
        self.assertTrue(response_data['user_token'])


class CreateInvalidUserTest(APITestCase):
    def setUp(self):
        data = {'email': 'invalidemail'}
        self.resp = self.client.post(reverse('user'), data)

    def test_create_invalid_user(self):
        """
        POST invalid user at /api/v1/users/
        Must return status code 400 BAD REQUEST
        """
        self.assertEqual(400, self.resp.status_code)

    def test_has_errors(self):
        """
        Context must return errors
        """
        self.assertTrue(self.resp.data.serializer.errors)

    def test_save_invalid_user(self):
        """
        Check if invalid user has not been saved
        """
        self.assertFalse(User.objects.exists())


class UpdateUserTest(APITestCase):
    def setUp(self):
        city = mommy.make_recipe('backend.core.city')
        self.user = mommy.make_recipe('backend.core.user', city=city)
        self.jwt_authorization = get_jwt_token(self.user)
        self.user.username = 'newname'
        self.user.email = 'newemail@email.com'

    def test_update_existing_user(self):
        """
        PUT /api/v1/users/user_id/ must return status code 200 OK and
        return data updated
        """
        data = model_to_dict(self.user)
        resp = self.client.put(reverse('user-update', kwargs={'pk': self.user.pk}), data,
                               HTTP_AUTHORIZATION=self.jwt_authorization)
        response_data = json.loads(resp.content.decode('utf8'))
        self.assertEqual('newname', response_data['username'])
        self.assertEqual('newemail@email.com', response_data['email'])
        self.assertEqual(200, resp.status_code)


class UpdateInvalidUserTest(APITestCase):
    def setUp(self):
        city = City.objects.create(name='TestLand', state='PR')
        user = mommy.make_recipe('backend.core.user', city=city)
        jwt_authorization = get_jwt_token(user)

        user.email = 'invalid_email_without_at'
        data = model_to_dict(user)
        self.resp = self.client.put(reverse('user-update', kwargs={'pk': user.pk}), data,
                                    HTTP_AUTHORIZATION=jwt_authorization)

    def test_update_invalid_data_user(self):
        """
        PUT invalid user at /api/v1/users/user_id/
        Must return status code 400 BAD REQUEST
        """
        self.assertEqual(400, self.resp.status_code)

    def test_has_errors(self):
        """
        Context must return errors
        """
        self.assertTrue(self.resp.data.serializer.errors)

    def test_save_invalid_user(self):
        """
        Check if invalid updated user has not been saved
        """
        self.assertTrue(User.objects.get().email != self.resp.data.serializer.data['email'])


class UpdateErrorsUserTest(APITestCase):
    def setUp(self):
        city = City.objects.create(name='TestLand', state='PR')
        self.user = mommy.make_recipe('backend.core.user', city=city)
        self.jwt_authorization = get_jwt_token(self.user)

    def test_user_cant_edit_other_users(self):
        """
        Current authenticated user can't edit other User's information
        PUT at /api/v1/users/user_id
        Must return status code 403 Forbidden
        """
        other_user = mommy.make_recipe('backend.core.user', username='leonardo2')
        other_user.first_name = 'Trying to change other user data'
        data = model_to_dict(other_user)
        resp = self.client.put(reverse('user-update', kwargs={'pk': other_user.pk}), data,
                               HTTP_AUTHORIZATION=self.jwt_authorization)
        self.assertEqual(403, resp.status_code)
