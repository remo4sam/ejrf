from questionnaire.forms.theme import ThemeForm
from questionnaire.models import Theme
from questionnaire.tests.base_test import BaseTest


class CoreSectionFormTest(BaseTest):

    def setUp(self):
        self.form_data = {'name': 'New theme',
                          'description': 'funny theme'}

    def test_valid(self):
        theme_form = ThemeForm(data=self.form_data)
        self.assertTrue(theme_form.is_valid())

    def test_creates_new_theme_if_valid(self):
        theme_form = ThemeForm(data=self.form_data)
        self.assertTrue(theme_form.is_valid())
        theme_form.save()
        self.failUnless(Theme.objects.filter(**self.form_data))

    def test_invalid_if_name_is_empty(self):
        data = self.form_data.copy()
        data['name'] = ''
        theme_form = ThemeForm(data=data)
        self.assertFalse(theme_form.is_valid())

    def test_valid_even_if_description_is_empty(self):
        data = self.form_data.copy()
        data['description'] = ''
        theme_form = ThemeForm(data=data)
        self.assertTrue(theme_form.is_valid())