from django.test import TestCase
from django.utils import formats
from model_mommy import mommy

from backend.accounts.models import User
from backend.core.models import City
from ..models import Report


class ReportModelTest(TestCase):
    def setUp(self):
        self.report = mommy.make_one(Report, city__name='Bom Despacho', user__first_name="Leonardo")

    def test_has_created(self):
        """
        Check if instance is a valid Report instance.
        """
        self.assertIsInstance(self.report, Report)

    def test_report_has_city(self):
        """
        Check if report has a City instance
        """
        self.assertIsInstance(self.report.city, City)

    def test_report_has_user(self):
        """
        Check if report has a User instance
        """
        self.assertIsInstance(self.report.user, User)

    def test_object_name(self):
        """
        Report instance must be return 'Denúncia' with User's first_name and date of creation
        """
        self.assertEqual(self.report.__str__(), 'Denúncia feita por - {} - {}'
                         .format(self.report.user.first_name, formats.date_format(self.report.created_at,
                                                                                 "SHORT_DATE_FORMAT")))


class ReportPermissionsTest(TestCase):
    def setUp(self):
        self._make_group_with_permission()
        self.user = mommy.make_recipe('backend.core.user')

    def _make_group_with_permission(self):
        self.group = mommy.make_recipe('backend.core.group')
        self.permission = mommy.make_recipe('backend.core.permission',
                                            codename='can_view_reports', name='Can View Reports')
        self.group.permissions.add(self.permission)
        self.group.save()

    def test_user_can_view_reports(self):
        """
        Check if user can view reports
        """
        self.user.groups.add(self.group)
        self.assertTrue(self.user.has_perm('reports.can_view_reports'))
