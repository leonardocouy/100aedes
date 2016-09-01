from django.test import TestCase
from model_mommy import mommy
from ..models import City


class CityModelTest(TestCase):
    def setUp(self):
        self.city = mommy.make_one(City)

    def test_has_created(self):
        """
        City instance must be created in the database
        """
        self.assertIsInstance(self.city, City)

    def test_object_name(self):
        """
        City instance must be return city name with state separated by /
        """
        self.assertEqual(self.city.__str__(), self.city.name + '/' + self.city.state)
