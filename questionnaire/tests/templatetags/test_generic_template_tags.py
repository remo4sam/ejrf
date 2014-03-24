from questionnaire.forms.theme import ThemeForm
from questionnaire.models import Question, QuestionOption, Theme
from questionnaire.templatetags.generic_tags import display_list, bootstrap_message, get_url_with_ids, divide_to_paginate, ASSIGN_QUESTION_PAGINATION_SIZE, add_string, get_questionnaire_from, \
    bootstrap_class, packaged_options, custom_options, get_theme_form_with_instance
from questionnaire.tests.base_test import BaseTest


class GeneralTemplateTagTest(BaseTest):

    def test_display_list_tag(self):
        sample_list = ['Global', 'Regional', 'Epi Manager']
        self.assertEqual(', '.join(sample_list), display_list(sample_list))

    def test_message(self):
        self.assertEqual('success', bootstrap_message('success'))
        self.assertEqual('danger', bootstrap_message('error'))
        self.assertEqual('warning', bootstrap_message('warning'))

    def test_should_return_url_given_url_name_and_ids(self):
        self.assertEqual('/questionnaire/document/1/delete/', get_url_with_ids(1, 'delete_document'))
        self.assertEqual('/questionnaire/entry/1/section/2/', get_url_with_ids("1, 2", 'questionnaire_entry_page'))

    def test_should_divide_questions_per_30(self):
        arbitrary_number = 220
        original_list = range(arbitrary_number)
        for i in range(1 + arbitrary_number / ASSIGN_QUESTION_PAGINATION_SIZE):
            paginated_list = range(i* ASSIGN_QUESTION_PAGINATION_SIZE, min((i+1)* ASSIGN_QUESTION_PAGINATION_SIZE, len(original_list)))
            self.assertEqual(paginated_list, divide_to_paginate(original_list)[i])

    def test_should_return_concatenated_ints_in_a_single_string(self):
        self.assertEqual('1, 2', add_string(1,2))
        self.assertEqual('1, 2', add_string('1','2'))

    def test_should_get_alist_of_questionnaires_given_a_dict_of_region_and_questionnaires(self):
        expected_input = {'region': {'drafts': ["Questuinnaire 1"], 'finalized': ["Questionnaire 2"]}}
        self.assertEqual(["Questionnaire 2"], get_questionnaire_from('region', regions_questionnaire_map=expected_input, status='finalized'))

    def test_gets_bootstrap_color_class_for_status(self):
        self.assertEqual('text-success', bootstrap_class('Submitted'))
        self.assertEqual('text-warning', bootstrap_class('In Progress'))
        self.assertEqual('text-danger', bootstrap_class('Not Started'))

    def test_question_knows_which_packaged_option_he_has(self):
        question = Question.objects.create(UID="0001", text="haha", answer_type='MultiChoice')
        QuestionOption.objects.create(text="Yes", question=question)
        QuestionOption.objects.create(text="No", question=question)

        self.assertEqual('checked', packaged_options(question, "Yes, No"))

    def test_question_knows_it_has_custom_options(self):
        question = Question.objects.create(UID="0001", text="haha", answer_type='MultiChoice')
        QuestionOption.objects.create(text="ha", question=question)
        QuestionOption.objects.create(text="ho", question=question)

        self.assertEqual('checked', custom_options(question))

    def test_gets_theme_form_for_given_instance_of_theme(self):
        theme = Theme.objects.create(name="haha")

        self.assertIsInstance(get_theme_form_with_instance(theme), ThemeForm)
        self.assertEqual(get_theme_form_with_instance(theme).instance, theme)