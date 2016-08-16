from django.test import TestCase
from model_mommy import mommy
from .models import Report


class ReportTest(TestCase):
    def setUp(self):
        self.resp = self.client.get('')


class ReportModelTest(TestCase):
    def setUp(self):
        self.report = mommy.make_one(Report, city__name='Bom Despacho')

    def test_has_created(self):
        """
        Report instance must be created in the database
        """
        self.assertIsInstance(self.report, Report)

    def test_report_has_city(self):
        """
        Report instance must be have a city and state associated
        """
        self.assertTrue(self.report.city.name == 'Bom Despacho' and self.report.city.state)