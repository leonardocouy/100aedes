from django.test import TestCase


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
        self.assertTemplateUsed(self.resp, 'index.html')

    def test_compile_scss_to_css(self):
        """
        css/main.scss needs compile in runtime to css/main.css
        """
        self.assertContains(self.resp, '.css', 1)

