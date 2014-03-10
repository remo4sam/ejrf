from datetime import date
from questionnaire.forms.questionnaires import QuestionnaireFilterForm, PublishQuestionnaireForm
from questionnaire.models import Questionnaire, Region, Organization
from questionnaire.tests.base_test import BaseTest


class QuestionnaireFilterFormTest(BaseTest):

    def setUp(self):
        self.questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English", status=Questionnaire.FINALIZED, year=2013)

        self.form_data = {
            'questionnaire': self.questionnaire.id,
            'year': date.today().year + 1,
            'name': 'New JRF'
        }

    def test_valid(self):
        questionnaire_filter = QuestionnaireFilterForm(self.form_data)
        self.assertTrue(questionnaire_filter.is_valid())

    def test_has_years_of_existing_questionnaires(self):
        questionnaire_filter = QuestionnaireFilterForm(self.form_data)
        self.assertIn(('', 'Choose a year'), questionnaire_filter.fields['year'].choices)
        for count in range(0, 10):
            year_option = date.today().year + count
            self.assertIn((year_option, year_option), questionnaire_filter.fields['year'].choices)

    def test_invalid_when_questionniare_is_blank(self):
        form_data = self.form_data.copy()
        form_data['questionnaire'] = ''
        questionnaire_filter = QuestionnaireFilterForm(form_data)
        self.assertFalse(questionnaire_filter.is_valid())
        self.assertIn("This field is required.", questionnaire_filter.errors['questionnaire'])

    def test_invalid_when_year_is_blank(self):
        form_data = self.form_data.copy()
        form_data['year'] = ''
        questionnaire_filter = QuestionnaireFilterForm(form_data)
        self.assertFalse(questionnaire_filter.is_valid())
        self.assertIn("This field is required.", questionnaire_filter.errors['year'])

    def test_valid_when_name_is_blank(self):
        form_data = self.form_data.copy()
        form_data['name'] = ''
        questionnaire_filter = QuestionnaireFilterForm(form_data)
        self.assertFalse(questionnaire_filter.is_valid())
        self.assertIn("This field is required.", questionnaire_filter.errors['name'])

    def test_clean_year(self):
        questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English", status=Questionnaire.FINALIZED, year=date.today().year + 1)
        form_data = self.form_data.copy()
        form_data['year'] = questionnaire.year
        questionnaire_filter = QuestionnaireFilterForm(form_data)
        self.assertFalse(questionnaire_filter.is_valid())
        message = "Select a valid choice. %d is not one of the available choices." % questionnaire.year
        self.assertIn(message, questionnaire_filter.errors['year'])

    def test_has_years_choices_exclude_existing_questionnaires_years(self):
        Questionnaire.objects.create(name="JRF 2013 Core English", status=Questionnaire.FINALIZED, year=date.today().year + 1)
        questionnaire_filter = QuestionnaireFilterForm(self.form_data)
        self.assertIn(('', 'Choose a year'), questionnaire_filter.fields['year'].choices)
        for count in range(2, 9):
            year_option = date.today().year + count
            self.assertIn((year_option, year_option), questionnaire_filter.fields['year'].choices)
        self.assertNotIn((date.today().year + 1, date.today().year + 1), questionnaire_filter.fields['year'].choices)


class PublishQuestionnaireFormTest(BaseTest):

    def setUp(self):
        self.questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English", status=Questionnaire.FINALIZED, year=2013)
        self.who = Organization.objects.create(name="WHO")
        self.afro = Region.objects.create(name="The Afro", organization=self.who)
        self.paho = Region.objects.create(name="The Paho", organization=self.who)

        self.form_data = {
            'questionnaire': self.questionnaire.id,
            'regions':[self.paho.id, self.afro.id]}

    def test_valid(self):
        publish_questionnaire_form = PublishQuestionnaireForm(initial={'questionnaire': self.questionnaire}, data=self.form_data)
        self.assertTrue(publish_questionnaire_form.is_valid())
        self.assertIn((self.paho.id, self.paho.name), publish_questionnaire_form.fields['regions'].choices)
        self.assertIn((self.afro.id, self.afro.name), publish_questionnaire_form.fields['regions'].choices)

    def test_choices_only_has_regions_that_do_not_have_published_questionnaires(self):
        questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English", status=Questionnaire.PUBLISHED, year=2013, region=self.afro)
        data = {'questionnaire': self.questionnaire, 'regions': [self.paho.id]}
        publish_questionnaire_form = PublishQuestionnaireForm(initial={'questionnaire': self.questionnaire}, data=data)
        self.assertTrue(publish_questionnaire_form.is_valid())
        region_choices = [choice for choice in publish_questionnaire_form.fields['regions'].choices]
        self.assertIn((self.paho.id, self.paho.name), region_choices)
        self.assertNotIn((self.afro.id, self.afro.name), region_choices)

    def test_creates_copies_for_regions_on_save(self):
        Questionnaire.objects.create(name="JRF 2013 Core English", status=Questionnaire.PUBLISHED, year=2013, region=self.afro)
        pacific = Region.objects.create(name="haha", organization=self.who)
        asia = Region.objects.create(name="hehe", organization=self.who)

        data = {'questionnaire': self.questionnaire, 'regions': [self.paho.id, pacific.id, asia.id]}

        publish_questionnaire_form = PublishQuestionnaireForm(initial={'questionnaire': self.questionnaire}, data=data)
        self.assertTrue(publish_questionnaire_form.is_valid())
        publish_questionnaire_form.save()
        questionnaires = Questionnaire.objects.filter(year=self.questionnaire.year)
        self.assertEqual(5, questionnaires.count())
        [self.assertEqual(1, region.questionnaire.all().count()) for region in [self.paho, pacific, asia]]
        self.assertEqual(1, self.afro.questionnaire.all().count())
        questionnaire = Questionnaire.objects.filter(id=self.questionnaire.id)[0]
        self.assertEqual(questionnaire.status, Questionnaire.PUBLISHED)