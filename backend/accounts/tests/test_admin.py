from django.contrib import admin
from django.contrib.auth.hashers import make_password
from django.forms import PasswordInput
from django.forms import model_to_dict
from django.test import Client
from django.test import RequestFactory
from django.test import TestCase
from django.forms.formsets import formset_factory
from django.urls import reverse
from model_mommy import mommy

from ..admin import UserAdmin
from ..models import User


class UserAdminTest(TestCase):
    def setUp(self):
        user = mommy.make_recipe('backend.core.user', is_staff=True, is_superuser=True)
        # self.rf = RequestFactory()
        self.client = Client()
        self.client.force_login(user)
        self.request = self.client.get("/admin/accounts/")
        self.request.user = user
        self.admin = UserAdmin(User, admin.site)

    def test_display_full_name(self):
        """
        Check if list has been displaying field full name
        """
        self.assertIn('get_full_name', self.admin.list_display)

    def test_password_widget(self):
        """
        Check if password field has been renderized by PasswordInput widget
        """
        self.assertIsInstance(self.admin.get_form(self.request).base_fields['password'].widget, PasswordInput)

    def test_create_coordenador_user(self):
        """
        On create a Coordenador user field is_staff should be checked.
        """
        group = mommy.make_recipe('backend.core.group', name='Coordenador')
        normal_user = mommy.make_recipe('backend.core.user', username='coordenador')
        data = model_to_dict(normal_user)
        data['groups'] = group.id
        response = self.client.post(reverse("admin:accounts_user_change", args=[normal_user.id]), data=data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.get(id=normal_user.pk).is_staff)

    def test_encode_password(self):
        """
        Make sure on create a new user his password should had encoded
        """
        data = {'username': 'test_user', 'password': 'test_password_not_encoded', 'phone': '999999999', 'city': 1}
        response = self.client.post(reverse("admin:accounts_user_add"), data=data, follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertRedirects(response, reverse('admin:accounts_user_changelist'))
        self.assertEquals(User.objects.filter(username='test_user').count(), 1)
        self.assertNotEquals(User.objects.get(username='test_user').password, data['password'])

    def test_change_password(self):
        """
        Check if user has changed his password.
        """
        user = User.objects.get(id=1)
        data = model_to_dict(user)
        data['password'] = 'new_password'
        response = self.client.post(reverse("admin:accounts_user_change", args=[user.id]), data=data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(user.password, User.objects.get(id=1).password)

    def test_not_change_password(self):
        """
        Make sure that User's password hadn't changed after POST
        """
        user = User.objects.get(id=1)
        data = model_to_dict(user)
        data['first_name'] = 'Carlos'
        response = self.client.post(reverse("admin:accounts_user_change", args=[user.id]), data=data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(user.password, User.objects.get(id=1).password)
