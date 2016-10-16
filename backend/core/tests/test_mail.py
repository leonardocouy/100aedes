from django.test import TestCase
from django.core import mail
from ..utils import _send_mail


class ContactMailTest(TestCase):
    def setUp(self):
        data = dict(name='Leonardo Flores', email='leo@leo.com', subject='Suggestion', message='None message')
        _send_mail(data['subject'], 'contato@100aedes.com.br', 'contato@100aedes.com.br', 'contact_email.txt',
                   {'contact': data})
        self.mail = mail.outbox[0]

    def test_send(self):
        """
        Check if email has been sent
        """
        self.assertEqual(len(mail.outbox), 1)

    def test_contact_email(self):
        """
        Check if email fields have been filled
        """
        self.assertEqual(self.mail.subject, 'Suggestion')
        self.assertEqual(self.mail.from_email , 'contato@100aedes.com.br')
        self.assertEqual(self.mail.to, ['contato@100aedes.com.br', 'contato@100aedes.com.br'])

    def test_template_renderized(self):
        """
        Check if email template have been renderized the data
        """

        contents = [
            'Leonardo Flores',
            'leo@leo.com',
            'Suggestion',
            'None message'
        ]

        for content in contents:
            with self.subTest():
                self.assertIn(content, self.mail.body)
