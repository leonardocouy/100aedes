from django.core import mail
from django.test import TestCase

from ..forms import ContactForm


class HomeTest(TestCase):
    def setUp(self):
        self.resp = self.client.get('/')

    def test_get(self):
        """
        GET / must return status code 200
        """
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        """
        Home must return a template
        """
        self.assertTemplateUsed(self.resp, 'base.html')

    def test_compile_scss_to_css(self):
        """
        css/main.scss needs compile in runtime to css/main.css
        """
        self.assertContains(self.resp, '.css', 1)

    def test_check_csrf(self):
        """
        Form must have CSRF
        """
        self.assertContains(self.resp, 'csrfmiddlewaretoken')

    def test_has_contact_form(self):
        """
        Context must have contact form
        """
        form = self.resp.context['form']
        self.assertIsInstance(form, ContactForm)

    def test_has_form_fields(self):
        """
        HTML must contain form input tags
        """

        tags = (
            ('<form', 1),
            ('<input', 4),
            ('<textarea', 1),
            ('type="text', 3),
            ('type="email', 1),
            ('type="submit', 1),
        )

        for text, count in tags:
            with self.subTest():
                self.assertContains(self.resp, text, count)


class ContactFormPost(TestCase):
    def setUp(self):
        data = dict(name='Leonardo Flores', email='leonardocouy@Hotmail.com',
                    subject='Suggestion', message='Make it better!')
        self.resp = self.client.post('/', data)

    def test_post(self):
        """
        Valid POST should redirect to home
        """
        self.assertRedirects(self.resp, '/')

    def test_send_contact_email(self):
        """
        Send email after successful
        """
        self.assertEqual(1, len(mail.outbox))


class ContactInvalidFormPost(TestCase):
    def setUp(self):
        self.resp = self.client.post('/', {})

    def test_post(self):
        """
        INVALID POST SHOULD NOT REDIRECT
        """
        self.assertEqual(200, self.resp.status_code)

    def test_form_has_errors(self):
        """
        Form must have errors
        """
        form = self.resp.context['form']
        self.assertTrue(form.errors)