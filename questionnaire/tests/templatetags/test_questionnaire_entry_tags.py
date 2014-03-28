from mock import patch, MagicMock
from questionnaire.models import Questionnaire, Section

from questionnaire.services.questionnaire_entry_form_service import QuestionnaireEntryFormService
from questionnaire.templatetags.questionnaire_entry_tags import get_form, _filename, get_value
from questionnaire.tests.base_test import BaseTest


class QuestionnaireEntryTagTest(BaseTest):

    def test_get_form(self):
        fake_question = 'fake question'
        questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English", description="From dropbox as given by Rouslan")
        section = Section.objects.create(title="Immunisation Coverage", order=1, description='section description',
                                                      questionnaire=questionnaire, name="im cover")

        fake_formsets = QuestionnaireEntryFormService(section)
        expected_visible_field = 'mocked visible fields'
        mock_form= MagicMock()
        mock_form.visible_fields.return_value = [expected_visible_field, 'some useless element']
        with patch.object(QuestionnaireEntryFormService, 'next_ordered_form', return_value=mock_form) as mock_next_ordered_form:
            obtained_visible_fields = get_form(fake_question, fake_formsets)
            self.assertEqual([expected_visible_field], obtained_visible_fields)
            mock_next_ordered_form.assert_called_once_with(fake_question)

    def test_gets_filename_from_path(self):
        filename = _filename('user_uploads/TechRadar_Jan_2014_V1_1.pdf')
        self.assertEqual('TechRadar_Jan_2014_V1_1.pdf', filename)

    def test_gets_value_from_dictionary(self):
        a_dict = {'key': 'value'}
        self.assertEqual('value', get_value('key', a_dict))