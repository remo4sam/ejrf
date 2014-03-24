from django.core.urlresolvers import reverse
from django.test import Client
from questionnaire.forms.theme import ThemeForm

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

    def test_get_create_theme(self):
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
        templates = [template.name for template in response.templates]
        self.assertIn("themes/index.html", templates)
        self.assertEqual(1, response.context['theme_list'].count())
        self.assertIn(self.theme, response.context['theme_list'])
        self.assertIsInstance(response.context['theme_form'], ThemeForm)
        self.assertEqual("/themes/new/", response.context['theme_form_action'])

    def test_post_save_theme(self):
        url = '/themes/new/'
        self.assertRaises(Theme.DoesNotExist, Theme.objects.get, **self.form_data)
        response = self.client.post(url, self.form_data)
        self.assertRedirects(response, reverse("theme_list_page"))
        self.failUnless(Theme.objects.filter(**self.form_data))
        message = "Theme successfully created."
        self.assertIn(message, response.cookies['messages'].value)

    def test_post_with_form_errors(self):
        url = '/themes/new/'
        data = self.form_data.copy()
        data['name'] = ''
        self.assertRaises(Theme.DoesNotExist, Theme.objects.get, **self.form_data)
        response = self.client.post(url, data=data)
        self.assertRaises(Theme.DoesNotExist, Theme.objects.get, **self.form_data)
        message = "Theme was not created, see Errors below"
        self.assertIn(message, str(response.content))


class EditThemeViewTest(BaseTest):

    def setUp(self):
        self.client = Client()
        self.user, self.country, self.region = self.create_user_with_no_permissions()
        self.assign('can_edit_questionnaire', self.user)
        self.client.login(username=self.user.username, password='pass')

        self.theme = Theme.objects.create(name="Some theme", description="some description")
        self.url = '/themes/%d/edit/' % self.theme.id
        self.form_data = {'name': 'Edited Theme',
                          'description': self.theme.description}

    def test_post_save_theme(self):
        self.assertRaises(Theme.DoesNotExist, Theme.objects.get, **self.form_data)
        response = self.client.post(self.url, self.form_data)
        self.assertRedirects(response, reverse("theme_list_page"))
        self.failIf(Theme.objects.filter(name=getattr(self.theme, 'name'), description=getattr(self.theme, 'description')))
        self.failUnless(Theme.objects.filter(**self.form_data))
        message = "Theme successfully updated."
        self.assertIn(message, response.cookies['messages'].value)

    def test_post_with_form_errors(self):
        data = self.form_data.copy()
        data['name'] = ''
        self.assertRaises(Theme.DoesNotExist, Theme.objects.get, **self.form_data)
        response = self.client.post(self.url, data=data)
        self.assertRaises(Theme.DoesNotExist, Theme.objects.get, **self.form_data)
        message = "Theme was not updated, see Errors below"
        self.assertIn(message, str(response.content))