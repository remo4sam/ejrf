from questionnaire.forms.answers import NumericalAnswerForm, TextAnswerForm, DateAnswerForm, MultiChoiceAnswerForm, MultiChoiceAnswerSelectWidget
from questionnaire.models import Question, Country, QuestionOption, QuestionGroup, Section, Questionnaire, SubSection
from questionnaire.tests.base_test import BaseTest


class NumericalAnswerFormTest(BaseTest):
    def setUp(self):
        self.country = Country.objects.create(name="Peru")
        self.question = Question.objects.create(text='C. Number of cases positive',
                                            instructions="Include only those cases found positive for the infectious agent.",
                                            UID='C00001', answer_type='Number')

        self.questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English", description="From dropbox as given by Rouslan")

        self.section = Section.objects.create(title="Reported Cases of Selected Vaccine Preventable Diseases (VPDs)", order=1,
                                                      questionnaire=self.questionnaire, name="Reported Cases")

        self.sub_section = SubSection.objects.create(title="Reported cases for the year 2013", order=1, section=self.section)
        self.question_group = QuestionGroup.objects.create(subsection=self.sub_section, order=1, allow_multiples=True)
        self.question_group.question.add(self.question)

        self.form_data = {
            'response': 100,
        }

        self.initial = {
            'question': self.question,
            'country': self.country.id,
            'status': 'DRAFT',
            'version': 1,
            'code':'HAHA123',
            'group': self.question_group
        }

    def test_valid(self):
        answer_form = NumericalAnswerForm(self.form_data, initial=self.initial)
        self.assertTrue(answer_form.is_valid())

    def test_text_response_is_invalid(self):
        form_data = self.form_data.copy()
        form_data['response'] = 'some text which is not number'
        answer_form = NumericalAnswerForm(form_data, initial=self.initial)
        self.assertFalse(answer_form.is_valid())
        message = 'Enter a number.'
        self.assertEqual([message], answer_form.errors['response'])


    def test_required_question_shows_field_required_error_when_no_data_is_posted_and_no_initial_passed_in(self):
        self.question.is_required = True
        self.question.save()
        answer_form_without_data = NumericalAnswerForm(initial=self.initial)
        answer_form_without_data.show_is_required_errors()
        self.assertEqual(['This field is required.'], answer_form_without_data.errors['response'])

        answer_form_with_data = NumericalAnswerForm(data={'response': 1},initial=self.initial)
        answer_form_with_data.show_is_required_errors()
        self.assertEqual({}, answer_form_with_data.errors)

        _initial=self.initial.copy()
        _initial['response'] = '1'
        answer_form_with_initial = NumericalAnswerForm(initial=_initial)
        answer_form_with_initial.show_is_required_errors()
        self.assertEqual({}, answer_form_with_initial.errors)


class TextAnswerFormTest(BaseTest):
    def setUp(self):
        self.country = Country.objects.create(name="Peru")
        self.question = Question.objects.create(text='C. Number of cases positive',
                                            instructions="Include only those cases found positive for the infectious agent.",
                                            UID='C00001', answer_type='Text')


        self.questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English", description="From dropbox as given by Rouslan")

        self.section = Section.objects.create(title="Reported Cases of Selected Vaccine Preventable Diseases (VPDs)", order=1,
                                                      questionnaire=self.questionnaire, name="Reported Cases")

        self.sub_section = SubSection.objects.create(title="Reported cases for the year 2013", order=1, section=self.section)
        self.question_group = QuestionGroup.objects.create(subsection=self.sub_section, order=1, allow_multiples=True)
        self.question_group.question.add(self.question)

        self.form_data = {
            'response':'some answer',
        }
        self.initial = {
            'question': self.question,
            'country': self.country.id,
            'status': 'DRAFT',
            'version':1,
            'code':'HAHA123',
            'group': self.question_group
        }

    def test_valid(self):
        answer_form = TextAnswerForm(self.form_data, initial=self.initial)
        self.assertTrue(answer_form.is_valid())


class DateAnswerFormTest(BaseTest):
    def setUp(self):
        self.country = Country.objects.create(name="Peru")
        self.question = Question.objects.create(text='C. Number of cases positive',
                                            instructions="Include only those cases found positive for the infectious agent.",
                                            UID='C00001', answer_type='Date')

        self.questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English", description="From dropbox as given by Rouslan")

        self.section = Section.objects.create(title="Reported Cases of Selected Vaccine Preventable Diseases (VPDs)", order=1,
                                                      questionnaire=self.questionnaire, name="Reported Cases")

        self.sub_section = SubSection.objects.create(title="Reported cases for the year 2013", order=1, section=self.section)
        self.question_group = QuestionGroup.objects.create(subsection=self.sub_section, order=1, allow_multiples=True)
        self.question_group.question.add(self.question)

        self.form_data = {
            'response':'2014-01-01',
        }

        self.initial = {
            'question': self.question,
            'country': self.country.id,
            'status': 'DRAFT',
            'version':1,
            'code':'HAHA123',
            'group': self.question_group,
            'questionnaire': self.questionnaire.id
        }

    def test_valid(self):
        answer_form = DateAnswerForm(self.form_data, initial=self.initial)
        self.assertTrue(answer_form.is_valid())

    def test_response_cannot_be_text(self):
        form_data = self.form_data.copy()
        form_data['response'] = 'some text which is not a date'
        answer_form = DateAnswerForm(form_data, initial=self.initial)
        self.assertFalse(answer_form.is_valid())
        message = 'Enter a valid date.'
        self.assertEqual([message], answer_form.errors['response'])


class MultiChoiceAnswerFormTest(BaseTest):
    def setUp(self):
        self.country = Country.objects.create(name="Peru")
        self.question = Question.objects.create(text='C. Number of cases positive',
                                            instructions="Include only those cases found positive for the infectious agent.",
                                            UID='C00001', answer_type='MultiChoice')
        self.question_option_one = QuestionOption.objects.create(text='Option One', question=self.question)

        self.questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English", description="From dropbox as given by Rouslan")

        self.section = Section.objects.create(title="Reported Cases of Selected Vaccine Preventable Diseases (VPDs)", order=1,
                                                      questionnaire=self.questionnaire, name="Reported Cases")

        self.sub_section = SubSection.objects.create(title="Reported cases for the year 2013", order=1, section=self.section)
        self.question_group = QuestionGroup.objects.create(subsection=self.sub_section, order=1, allow_multiples=True)
        self.question_group.question.add(self.question)

        self.form_data = {
            'response': self.question_option_one.id,
        }

        self.initial = {
            'question': self.question,
            'country': self.country,
            'status': 'DRAFT',
            'version': 1,
            'code':'HAHA123',
            'group': self.question_group,
            'questionnaire': self.questionnaire.id
        }

    def test_valid(self):
        answer_form = MultiChoiceAnswerForm(self.form_data, initial=self.initial)
        self.assertTrue(answer_form.is_valid())
        self.assertIsNone(answer_form.fields['response'].empty_label)

    def test_id_of_a_non_option(self):
        form_data = self.form_data.copy()
        form_data['response'] = -1
        answer_form = MultiChoiceAnswerForm(form_data, initial=self.initial)
        self.assertFalse(answer_form.is_valid())
        message = 'Select a valid choice. That choice is not one of the available choices.'
        self.assertEqual([message], answer_form.errors['response'])

    def test_multiple_form_choice_form_adds_data_instruction_attributes_for_question_options(self):
        question_option_two = QuestionOption.objects.create(text='Option 2', question=self.question, instructions="Some stuff")
        question_option_3 = QuestionOption.objects.create(text='Option 3', question=self.question, instructions="Some stuff")
        question_option_4 = QuestionOption.objects.create(text='Option 4', question=self.question, instructions="Some stuff")

        answer_form = MultiChoiceAnswerForm(initial=self.initial)
        query_set = answer_form._get_response_choices(self.initial)
        widget = answer_form._get_response_widget(query_set)
        self.assertIsInstance(widget, MultiChoiceAnswerSelectWidget)
        self.assertEqual(4, widget.question_options.count())
        self.assertIn(self.question_option_one, widget.question_options)
        self.assertIn(question_option_two, widget.question_options)
        self.assertIn(question_option_3, widget.question_options)
        self.assertIn(question_option_4, widget.question_options)

        self.assertEqual("Choose One", answer_form.fields['response'].empty_label)


class MultiChoiceAnswerSelectWidgetTest(BaseTest):

    def test_option_has_data_attributes_on_top_of_normal_attributes(self):
        question = Question.objects.create(text='what do you drink?', UID='C_2013', answer_type='MultiChoice')
        option1 = QuestionOption.objects.create(text='tusker lager', question=question, instructions="yeah yeah")
        option2 = QuestionOption.objects.create(text='club', question=question, instructions="Are you crazy?")

        choices =((option1.id, option1.text), (option2.id, option2.text))

        widget = MultiChoiceAnswerSelectWidget(choices=choices, question_options=question.options.all())

        expected_option_1 = '<option value="%d" selected="selected" data-instructions="%s">%s</option>' % (option1.id, option1.instructions, option1.text)
        expected_option_2 = '<option value="%d" data-instructions="%s">%s</option>' % (option2.id, option2.instructions, option2.text)

        self.assertEqual(expected_option_1,
                         widget.render_option(selected_choices=[str(option1.id)], option_value=option1.id, option_label=option1.text))
        self.assertEqual(expected_option_2,
                         widget.render_option(selected_choices=[str(option1.id)], option_value=option2.id, option_label=option2.text))