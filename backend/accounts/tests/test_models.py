from django.test import TestCase
from model_mommy import mommy

from backend.core.models import City
from ..models import User


class UserModelTest(TestCase):
    def setUp(self):
        self.user = mommy.make_recipe('backend.core.user')

    def test_has_created(self):
        """
        Check if instance is a valid User instance.
        """
        self.assertIsInstance(self.user, User)

    def test_has_city_associated(self):
        """
        Check if user has a City instance
        """
        self.assertIsInstance(self.user.city, City)

    def test_str(self):
        """
        Class User must return FIRST_NAME LAST_NAME - CITY/STATE
        """
        self.assertEqual(self.user.__str__(),
                         '{} - {}'.format(self.user.get_full_name(), self.user.city.__str__()))

