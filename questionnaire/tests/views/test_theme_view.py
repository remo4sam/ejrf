from django.core.urlresolvers import reverse
from django.test import Client
from questionnaire.forms.theme import ThemeForm

from questionnaire.models import Theme, Question
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

    def test_permissions_required(self):
        self.assert_login_required(self.url)
        self.assert_permission_required(self.url)


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

    def test_permissions_required(self):
        self.assert_login_required(self.url)
        self.assert_permission_required(self.url)


class DeleteThemeViewTest(BaseTest):

    def setUp(self):
        self.client = Client()
        self.user, self.country, self.region = self.create_user_with_no_permissions()
        self.assign('can_edit_questionnaire', self.user)
        self.client.login(username=self.user.username, password='pass')

        self.theme = Theme.objects.create(name="Beer theme", description="some description")
        self.url = '/themes/%d/delete/' % self.theme.id

    def test_post_delete(self):
        self.failUnless(Theme.objects.get(id=self.theme.id))
        response = self.client.post(self.url, {})
        self.assertRedirects(response, reverse("theme_list_page"))
        self.failIf(Theme.objects.filter(name=getattr(self.theme, 'name'), description=getattr(self.theme, 'description')))
        message = "Theme successfully deleted."
        self.assertIn(message, response.cookies['messages'].value)

    def test_post_delete_de_associates_the_questions_from_it(self):
        beer_question = Question.objects.create(text="How many beers do you drink?", UID='BR01',
                                                answer_type=Question.NUMBER, theme=self.theme)
        beer_question1 = Question.objects.create(text="When did you last drink beer?", UID='BR02',
                                                 answer_type=Question.DATE, theme=self.theme)

        response = self.client.post(self.url, {})
        self.assertEqual(Question.objects.all().count(), 2)
        self.failUnless(Question.objects.get(id=beer_question1.id))
        self.failUnless(Question.objects.get(id=beer_question.id))
        self.failIf(Theme.objects.filter(name=getattr(self.theme, 'name'), description=getattr(self.theme, 'description')))
        message = "Theme successfully deleted."
        self.assertIn(message, response.cookies['messages'].value)

    def test_permissions_required(self):
        self.assert_login_required(self.url)
        self.assert_permission_required(self.url)