from questionnaire.forms.questions import QuestionForm, QuestionHistoryForm
from questionnaire.models import Question, QuestionOption, Questionnaire, Section, SubSection, QuestionGroup
from questionnaire.tests.base_test import BaseTest


class QuestionsFormTest(BaseTest):

    def setUp(self):
        self.form_data = {'text': 'How many kids were immunised this year?',
                          'instructions': 'Some instructions',
                          'short_instruction': 'short version',
                          'answer_type': 'Number',
                          'export_label': 'Some export text',
                          'options': ['', ]}

    def test_valid(self):
        section_form = QuestionForm(data=self.form_data)
        self.assertTrue(section_form.is_valid())

    def test_increments_uid_of_existing_question_by_one_upon_save_given_instance(self):
        Question.objects.create(text='B. Number of cases tested',
                                instructions="Enter the total number of cases", UID='00001', answer_type='Number')
        question_form = QuestionForm(data=self.form_data)
        question = question_form.save(commit=True)
        self.assertEqual('00002', question.UID)

    def test_invalid_if_question_text_is_blank(self):
        data = self.form_data.copy()
        data['text'] = ''
        question_form = QuestionForm(data=data)
        self.assertFalse(question_form.is_valid())
        self.assertIn("This field is required.", question_form.errors['text'])

    def test_clean_answer_type(self):
        data = self.form_data.copy()
        data['answer_type'] = ''
        question_form = QuestionForm(data=data)
        self.assertFalse(question_form.is_valid())
        self.assertIn("This field is required.", question_form.errors['answer_type'])

    def test_clean_export_label(self):
        data = self.form_data.copy()
        data['export_label'] = ''
        question_form = QuestionForm(data=data)
        self.assertFalse(question_form.is_valid())
        self.assertIn("All questions must have export label.", question_form.errors['export_label'])

    def test_answer_type_choices_has_empty_label(self):
        question_form = QuestionForm()
        self.assertIn(('', 'Response type'), question_form.fields['answer_type'].choices)

    def test_save_multichoice_question_saves_options(self):
        options = ['Yes, No, Maybe']
        form = {'text': 'How many kids were immunised this year?',
                'instructions': 'Some instructions',
                'short_instruction': 'short version',
                'export_label': 'blah',
                'answer_type': 'MultiChoice',
                'options': options}

        question_form = QuestionForm(data=form)
        question = question_form.save(commit=True)
        question_options = QuestionOption.objects.filter(question=question)

        self.assertEqual(3, question_options.count())
        [self.assertIn(question_option.text, options[0].split(',')) for question_option in question_options]

    def test_assigns_region_on_save_if_region_is_given(self):
        global_admin, country, region = self.create_user_with_no_permissions()
        form = {'text': 'How many kids were immunised this year?',
                'instructions': 'Some instructions',
                'short_instruction': 'short version',
                'export_label': 'blah',
                'answer_type': 'Text'}
        question_form = QuestionForm(region=region, data=form)
        question = question_form.save(commit=True)
        self.assertEqual(region, question.region)

    def test_form_invalid_if_multichoice_question_and_no_options_in_data_options(self):
        form = {'text': 'How many kids were immunised this year?',
                'instructions': 'Some instructions',
                'short_instruction': 'short version',
                'export_label': 'blah',
                'answer_type': 'MultiChoice',
                'options': ['', '']}
        question_form = QuestionForm(data=form)

        self.assertFalse(question_form.is_valid())
        message = "MultiChoice questions must have at least one option"
        self.assertIn(message, question_form.errors['answer_type'][0])


class QuestionHistoryTestForm(BaseTest):

    def setUp(self):
        self.questionnaire = Questionnaire.objects.create(name="Uganda Revision 2014", description="some description")
        self.section = Section.objects.create(title="Immunisation Coverage", order=1, questionnaire=self.questionnaire)
        self.sub_section = SubSection.objects.create(title="Immunisation Extra Coverage", order=1, section=self.section)
        self.question1 = Question.objects.create(text='B. Number of cases tested',
                                                 UID='C00003', answer_type='Number')
        self.parent_group = QuestionGroup.objects.create(subsection=self.sub_section, name="Laboratory Investigation")
        self.parent_group.question.add(self.question1)

        self.form_data = {'text': 'How many kids were immunised this year?',
                          'export_label': 'Some export text',
                          'questionnaire': self.questionnaire.id,
                          'question': self.question1.id}

    def test_valid(self):
        history_form = QuestionHistoryForm(data=self.form_data)
        self.assertTrue(history_form.is_valid())

    def test_question_must_be_in_selected_questionnaire(self):
        question1 = Question.objects.create(text='B. Number of cases tested', UID='00033', answer_type='Number')
        data = self.form_data.copy()
        data['question'] = question1.id
        history_form = QuestionHistoryForm(data=data)
        self.assertFalse(history_form.is_valid())
        message = "The selected question should belong to a the selected questionnaire"
        self.assertIn(message, history_form.errors['question'])