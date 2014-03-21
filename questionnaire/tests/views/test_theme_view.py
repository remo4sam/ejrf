from django.test import Client

from questionnaire.models import Theme
from questionnaire.tests.base_test import BaseTest


class ThemeViewTest(BaseTest):
    def setUp(self):
        self.client = Client()
        self.user, self.country, self.region = self.create_user_with_no_permissions()
        self.assign('can_edit_questionnaire', self.user)
        self.client.login(username=self.user.username, password='pass')

        self.theme = Theme.objects.create(name="Some theme", description="some description")
        self.url = '/themes/'
        self.form_data = {'name': 'New Theme',
                          'description': 'funny theme'}

    def test_get_create_section(self):
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
        templates = [template.name for template in response.templates]
        self.assertIn("themes/index.html", templates)
        self.assertEqual(1, response.context['theme_list'].count())
        self.assertIn(self.theme, response.context['theme_list'])