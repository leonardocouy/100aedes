from django.test import TestCase

from ..forms import ContactForm


class ContactFormTest(TestCase):
    def setUp(self):
        self.form = ContactForm()

    def test_form_has_fields(self):
        """
        Form must have 4 fields.
        """
        expected = ['name', 'email', 'subject', 'message']
        self.assertSequenceEqual(expected, list(self.form.fields))
