from django.test import TestCase
from backend.core.models import City
from .models import Report


class ReportTest(TestCase):
    def setUp(self):
        self.resp = self.client.get('')


class ReportModelTest(TestCase):
    def setUp(self):
        self.city = City.objects.create(name='Bom Despacho', state='MG')
        self.report = Report.objects.create(city=self.city, address='Av. Maria da Conceição Del Duca',
                                            district='Jaraguá', landmark='SESC',
                                            description='Ao lado direito do SESC está um pneu cheio de água parada')

    def test_has_created(self):
        """
        Report instance must be created in the database
        """
        self.assertTrue(Report.objects.get(pk=self.report.pk))