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

from ..admin import ReportAdmin, ReadOnlyReportAdmin
from ..models import User, Report


class ReportReadOnlyAdminTest(TestCase):
    def setUp(self):
        group = mommy.make_recipe('backend.core.group', name='Agente')
        self.user = mommy.make_recipe('backend.core.user', phone='9999-9999', groups=[group], is_staff=True)
        self.report = mommy.make_one(Report, city__name='Bom Despacho', city__state='MG', user=self.user, _fill_optional=True)
        self.client = Client()
        self.client.force_login(self.user)
        self.response = self.client.get("/admin/reports/report/")
        self.response.user = self.user
        self.admin = ReadOnlyReportAdmin(Report, admin.site)

    def check_groups_are_readonly(self):
        """
        Check if groups are readonly (group like: Agente).
        """
        groups = ("Agente",)

        for group in groups:
            with self.subTest():
                self.assertIn(group, self.admin.READ_ONLY_GROUPS)

    def check_user_is_readonly(self):
        """
        Check if user is readonly
        """
        user_groups = [group.name for group in self.user.groups.all()]
        for user_group in user_groups:
            with self.subTest():
                self.assertIn(user_group, list(self.admin.READ_ONLY_GROUPS))
        self.assertFalse(self.response.user.is_superuser)

    def check_fields_are_readonly(self):
        """
        Check if fields are readonly for specify group like: Agente
        """
        readonly_fields = ['location']
        readonly_fields += [f.name for f in self.admin.model._meta.fields]

        self.assertTrue(self.admin.has_change_permission(self.response))
        self.assertListEqual(readonly_fields, self.admin.readonly_fields)

    def check_actions_are_readonly(self):
        """
        Check if actions are readonly for specify group like: Agente
        """
        current_actions = self.admin.get_actions(self.response.wsgi_request)
        self.assertEqual(self.response.status_code, 200)
        self.assertNotIn('delete_selected', current_actions)


class ReportNotReadOnlyAdminTest(TestCase):
    def setUp(self):
        self.user = mommy.make_recipe('backend.core.user', phone='9999-9999', is_staff=True, is_superuser=True)
        self.report = mommy.make_one(Report, city__name='Bom Despacho', city__state='MG', user=self.user, _fill_optional=True)
        self.client = Client()
        self.client.force_login(self.user)
        self.response = self.client.get(reverse("admin:reports_report_changelist"))
        self.response.user = self.user
        self.admin = ReadOnlyReportAdmin(Report, admin.site)

    def check_user_is_not_readonly(self):
        """
        Check if user is not readonly
        """
        user_groups = [group.name for group in self.user.groups.all()]
        for user_group in user_groups:
            with self.subTest():
                self.assertNotIn(user_group, list(self.admin.READ_ONLY_GROUPS))

    def check_actions_are_not_readonly(self):
        """
        Check if actions are not readonly for specify group like: Superuser, coordenador
        """
        current_actions = self.admin.get_actions(self.response.wsgi_request)
        self.assertEqual(self.response.status_code, 200)
        self.assertEqual(1, len(current_actions))


class ReportAdminTest(TestCase):
    def setUp(self):
        user = mommy.make_recipe('backend.core.user', phone='9999-9999', is_staff=True, is_superuser=True)
        self.report = mommy.make_one(Report, city__name='Bom Despacho', city__state='MG', user=user, _fill_optional=True)
        self.client = Client()
        self.client.force_login(user)
        self.response = self.client.get("/admin/reports/report")
        self.response.user = user
        self.admin = ReportAdmin(Report, admin.site)

    def test_display_first_name(self):
        """
        Check if list has been displaying field first_name and if first name it's correct.
        """
        self.assertEqual(self.admin.get_first_name(self.report), 'Leonardo')
        self.assertIn('get_first_name', self.admin.list_display)

    def test_display_user_email(self):
        """
        Check if list has been displaying field email and if email it's correct.
        """
        self.assertEqual(self.admin.get_email(self.report), 'leonardo@leo.com')
        self.assertIn('get_email', self.admin.list_display)

    def test_display_user_phone(self):
        """
        Check if list has been displaying field phone and if phone it's correct.
        """
        self.assertEqual(self.admin.get_phone(self.report), '9999-9999')
        self.assertIn('get_phone', self.admin.list_display)

    def test_display_city_state(self):
        """
        Check if list has been displaying field city and state, and if city it's correct.
        """
        self.assertEqual(self.admin.get_city_and_state(self.report), 'Bom Despacho/MG')
        self.assertIn('get_city_and_state', self.admin.list_display)


class ReportDetailAdminTest(TestCase):
    def setUp(self):
        user = mommy.make_recipe('backend.core.user', is_staff=True, is_superuser=True)
        self.report = mommy.make_one(Report, city__name='Bom Despacho', user=user, _fill_optional=True)
        self.client = Client()
        self.client.force_login(user)
        self.response = self.client.get(reverse("admin:reports_report_change", args=[self.report.id]))
        self.response.user = user
        self.admin = ReportAdmin(Report, admin.site)

    def test_display_location(self):
        """
        Check if location url has been filled correctly in form
        """
        self.assertContains(self.response, '<a target="_blank" href="http://maps.google.com/maps?q=loc:{},{}">Abrir localização no Google Maps</a>'
                            .format(self.report.latitude, self.report.longitude))

    def test_remove_choice_nao_enviada(self):
        """
        Make sure the choice "Não enviada" must not be append to the list of status.
        """
        form = self.admin.get_form(self.response, obj=self.report)
        self.assertNotIn((0, 'Não Enviada'), form.base_fields['status'].choices)
