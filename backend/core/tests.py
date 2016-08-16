from django.test import TestCase
from .models import City


class HomeTest(TestCase):
    def setUp(self):
        self.resp = self.client.get('/')

    def test_get(self):
        """
        GET / must return status code 200
        """
        self.assertEqual(200, self.resp.status_code)


class CityModelTest(TestCase):
    def setUp(self):
        self.city = City.objects.create(name='Bom Despacho', state='MG')

    def test_has_created(self):
        """
        City instance must be created in the database
        """
        self.assertTrue(City.objects.get(pk=self.city.pk))

    def test_object_name(self):
        """
        City instance must be return city name
        """
        self.assertEqual(self.city.__str__(), self.city.name + '/' + self.city.state)
