import urllib
from django.http.request import QueryDict
from questionnaire.forms.answers import NumericalAnswerForm, TextAnswerForm, DateAnswerForm, MultiChoiceAnswerForm
from questionnaire.services.questionnaire_entry_form_service import QuestionnaireEntryFormService
from questionnaire.models import Questionnaire, Section, SubSection, QuestionGroup, Question, QuestionGroupOrder, NumericalAnswer, Answer, AnswerGroup, Country, TextAnswer, QuestionOption, MultiChoiceAnswer, DateAnswer
from questionnaire.tests.base_test import BaseTest


class QuestionnaireEntryAsServiceTest(BaseTest):
    def setUp(self):
        self.questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English",
                                                          description="From dropbox as given by Rouslan")

        self.section1 = Section.objects.create(title="Reported Cases of Selected Vaccine Preventable Diseases (VPDs)",
                                               order=1,
                                               questionnaire=self.questionnaire, name="Reported Cases")

        self.sub_section = SubSection.objects.create(title="subsection 1", order=1, section=self.section1)
        self.sub_section2 = SubSection.objects.create(title="subsection 2", order=2, section=self.section1)

        self.question_group = QuestionGroup.objects.create(subsection=self.sub_section, order=1)
        self.question_group2 = QuestionGroup.objects.create(subsection=self.sub_section, order=2)
        self.question_group3 = QuestionGroup.objects.create(subsection=self.sub_section2, order=1)

        self.question1 = Question.objects.create(text='question 1', UID='C00001', answer_type='MultiChoice')
        self.question2 = Question.objects.create(text='question 2', instructions="instruction 2",
                                                 UID='C00002', answer_type='Text')

        self.question3 = Question.objects.create(text='question 3', instructions="instruction 3",
                                                 UID='C00003', answer_type='Number')

        self.question4 = Question.objects.create(text='question 4', UID='C00004', answer_type='MultiChoice')
        self.question5 = Question.objects.create(text='question 4', instructions="instruction 2",
                                                 UID='C00005', answer_type='Number')

        self.question6 = Question.objects.create(text='question 6', instructions="instruction 3",
                                                 UID='C00006', answer_type='Date')

        self.question_group.question.add(self.question1, self.question3, self.question2)
        self.question_group2.question.add(self.question4, self.question5)
        self.question_group3.question.add(self.question6)

        QuestionGroupOrder.objects.create(question=self.question1, question_group=self.question_group, order=1)
        QuestionGroupOrder.objects.create(question=self.question2, question_group=self.question_group, order=2)
        QuestionGroupOrder.objects.create(question=self.question3, question_group=self.question_group, order=3)
        QuestionGroupOrder.objects.create(question=self.question4, question_group=self.question_group2, order=1)
        QuestionGroupOrder.objects.create(question=self.question5, question_group=self.question_group2, order=2)
        QuestionGroupOrder.objects.create(question=self.question6, question_group=self.question_group3, order=1)

        self.country = Country.objects.create(name="Uganda")
        self.initial = {'status': 'Draft', 'country': self.country, 'version': 1, 'questionnaire': self.questionnaire}

    def test_questionnaire_entry_form_formset_size_per_answer_type_should_match_number_of_question_per_answer_type(
            self):
        questionnaire_entry_form = QuestionnaireEntryFormService(self.section1, initial=self.initial)
        formsets = questionnaire_entry_form._formsets()
        self.assertEqual(2, len(formsets['Number']))
        self.assertEqual(1, len(formsets['Text']))
        self.assertEqual(1, len(formsets['Date']))
        self.assertEqual(2, len(formsets['MultiChoice']))

    def test_questionnaire_entry_form_generates_all_answer_type_formsets(self):
        questionnaire_entry_form = QuestionnaireEntryFormService(self.section1, initial=self.initial)
        formsets = questionnaire_entry_form._formsets()
        self.assertIsInstance(formsets['Number'][0], NumericalAnswerForm)
        self.assertIsInstance(formsets['Text'][0], TextAnswerForm)
        self.assertIsInstance(formsets['Date'][0], DateAnswerForm)
        self.assertIsInstance(formsets['MultiChoice'][0], MultiChoiceAnswerForm)

    def test_should_order_forms(self):
        questionnaire_entry_form = QuestionnaireEntryFormService(self.section1, initial=self.initial)
        formsets = questionnaire_entry_form._formsets()

        self.assertEqual(self.question1, formsets['MultiChoice'][0].initial['question'])
        self.assertEqual(self.question2, formsets['Text'][0].initial['question'])
        self.assertEqual(self.question3, formsets['Number'][0].initial['question'])
        self.assertEqual(self.question4, formsets['MultiChoice'][1].initial['question'])
        self.assertEqual(self.question5, formsets['Number'][1].initial['question'])
        self.assertEqual(self.question6, formsets['Date'][0].initial['question'])

    def test_should_give_correct_form_for_question(self):
        questionnaire_entry_form = QuestionnaireEntryFormService(self.section1, initial=self.initial)

        question_form = questionnaire_entry_form.next_ordered_form(self.question1)
        self.assertIsInstance(question_form, MultiChoiceAnswerForm)
        self.assertEqual(self.question1, question_form.initial['question'])

        question_form = questionnaire_entry_form.next_ordered_form(self.question2)
        self.assertIsInstance(question_form, TextAnswerForm)
        self.assertEqual(self.question2, question_form.initial['question'])

        question_form = questionnaire_entry_form.next_ordered_form(self.question3)
        self.assertIsInstance(question_form, NumericalAnswerForm)
        self.assertEqual(self.question3, question_form.initial['question'])

        question_form = questionnaire_entry_form.next_ordered_form(self.question4)
        self.assertIsInstance(question_form, MultiChoiceAnswerForm)
        self.assertEqual(self.question4, question_form.initial['question'])

        question_form = questionnaire_entry_form.next_ordered_form(self.question5)
        self.assertIsInstance(question_form, NumericalAnswerForm)
        self.assertEqual(self.question5, question_form.initial['question'])

        question_form = questionnaire_entry_form.next_ordered_form(self.question6)
        self.assertIsInstance(question_form, DateAnswerForm)
        self.assertEqual(self.question6, question_form.initial['question'])

    def test_should_append_groups_in_initial(self):
        questionnaire_entry_form = QuestionnaireEntryFormService(self.section1, initial=self.initial)
        formsets = questionnaire_entry_form._formsets()

        self.assertEqual(self.question_group, formsets['MultiChoice'][0].initial['group'])
        self.assertEqual(self.question_group, formsets['Text'][0].initial['group'])
        self.assertEqual(self.question_group, formsets['Number'][0].initial['group'])
        self.assertEqual(self.question_group2, formsets['MultiChoice'][1].initial['group'])
        self.assertEqual(self.question_group2, formsets['Number'][1].initial['group'])
        self.assertEqual(self.question_group3, formsets['Date'][0].initial['group'])

    def test_initial_gets_response_if_there_is_draft_answer_for_country(self):
        question3_answer = NumericalAnswer.objects.create(question=self.question3, country=self.country,
                                                          status=Answer.DRAFT_STATUS, response=1,
                                                          questionnaire=self.questionnaire)
        question2_answer = TextAnswer.objects.create(question=self.question2, country=self.country,
                                                     status=Answer.DRAFT_STATUS, response="ayoyoyo",
                                                     questionnaire=self.questionnaire)
        answer_group1 = AnswerGroup.objects.create(grouped_question=self.question_group, row=1)
        answer_group1.answer.add(question2_answer, question3_answer)

        country_2 = Country.objects.create(name="Uganda 2")
        question1_answer_2 = NumericalAnswer.objects.create(question=self.question1, country=country_2,
                                                            status=Answer.DRAFT_STATUS, response=23,
                                                            questionnaire=self.questionnaire)
        question2_answer_2 = NumericalAnswer.objects.create(question=self.question2, country=country_2,
                                                            status=Answer.DRAFT_STATUS, response=1,
                                                            questionnaire=self.questionnaire)
        answer_group_2 = AnswerGroup.objects.create(grouped_question=self.question_group, row=2)
        answer_group_2.answer.add(question1_answer_2, question2_answer_2)

        questionnaire_entry_form = QuestionnaireEntryFormService(self.section1, initial=self.initial)
        formsets = questionnaire_entry_form._formsets()

        self.assertEqual(self.question1, formsets['MultiChoice'][0].initial['question'])
        self.assertEqual(self.question2, formsets['Text'][0].initial['question'])
        self.assertEqual(self.question3, formsets['Number'][0].initial['question'])
        self.assertEqual(self.question4, formsets['MultiChoice'][1].initial['question'])
        self.assertEqual(self.question5, formsets['Number'][1].initial['question'])
        self.assertEqual(self.question6, formsets['Date'][0].initial['question'])

        self.assertNotIn('response', formsets['MultiChoice'][0].initial.keys())
        self.assertEqual(question2_answer.response, formsets['Text'][0].initial['response'])
        self.assertEqual(question3_answer.response, formsets['Number'][0].initial['response'])

        self.assertNotIn('response', formsets['MultiChoice'][1].initial.keys())
        self.assertNotIn('response', formsets['Number'][1].initial.keys())
        self.assertNotIn('response', formsets['Date'][0].initial.keys())

        self.assertNotIn('answer', formsets['MultiChoice'][0].initial.keys())
        self.assertEqual(question2_answer, formsets['Text'][0].initial['answer'])
        self.assertEqual(question3_answer, formsets['Number'][0].initial['answer'])
        self.assertNotIn('answer', formsets['MultiChoice'][1].initial.keys())
        self.assertNotIn('answer', formsets['Number'][1].initial.keys())
        self.assertNotIn('answer', formsets['Date'][0].initial.keys())

    def test_initial_gets_response_if_the_latest_answer_is_SUMBITTED_for_country(self):
        question3_answer = NumericalAnswer.objects.create(question=self.question3, country=self.country,
                                                          status=Answer.SUBMITTED_STATUS, response=1,
                                                          questionnaire=self.questionnaire)
        question2_answer = TextAnswer.objects.create(question=self.question2, country=self.country,
                                                     status=Answer.SUBMITTED_STATUS, response="ayoyoyo",
                                                     questionnaire=self.questionnaire)
        answer_group1 = AnswerGroup.objects.create(grouped_question=self.question_group, row=1)
        answer_group1.answer.add(question2_answer, question3_answer)

        country_2 = Country.objects.create(name="Uganda 2")
        question1_answer_2 = NumericalAnswer.objects.create(question=self.question1, country=country_2,
                                                            status=Answer.SUBMITTED_STATUS, response=23,
                                                            questionnaire=self.questionnaire)
        question2_answer_2 = NumericalAnswer.objects.create(question=self.question2, country=country_2,
                                                            status=Answer.SUBMITTED_STATUS, response=1,
                                                            questionnaire=self.questionnaire)
        answer_group_2 = AnswerGroup.objects.create(grouped_question=self.question_group, row=2)
        answer_group_2.answer.add(question1_answer_2, question2_answer_2)

        questionnaire_entry_form = QuestionnaireEntryFormService(self.section1, initial=self.initial)
        formsets = questionnaire_entry_form._formsets()

        self.assertEqual(self.question1, formsets['MultiChoice'][0].initial['question'])
        self.assertEqual(self.question2, formsets['Text'][0].initial['question'])
        self.assertEqual(self.question3, formsets['Number'][0].initial['question'])
        self.assertEqual(self.question4, formsets['MultiChoice'][1].initial['question'])
        self.assertEqual(self.question5, formsets['Number'][1].initial['question'])
        self.assertEqual(self.question6, formsets['Date'][0].initial['question'])

        self.assertNotIn('response', formsets['MultiChoice'][0].initial.keys())
        self.assertEqual(question2_answer.response, formsets['Text'][0].initial['response'])
        self.assertEqual(question3_answer.response, formsets['Number'][0].initial['response'])

        self.assertNotIn('response', formsets['MultiChoice'][1].initial.keys())
        self.assertNotIn('response', formsets['Number'][1].initial.keys())
        self.assertNotIn('response', formsets['Date'][0].initial.keys())

        self.assertNotIn('answer', formsets['MultiChoice'][0].initial.keys())
        self.assertNotIn('answer', formsets['Text'][0].initial.keys())
        self.assertNotIn('answer', formsets['Number'][0].initial.keys())
        self.assertNotIn('answer', formsets['MultiChoice'][1].initial.keys())
        self.assertNotIn('answer', formsets['Number'][1].initial.keys())
        self.assertNotIn('answer', formsets['Date'][0].initial.keys())


class QuestionnaireEntryAsFormTest(BaseTest):
    def setUp(self):
        self.questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English",
                                                          description="From dropbox as given by Rouslan")

        self.section_1 = Section.objects.create(title="Reported Cases of Selected Vaccine Preventable Diseases (VPDs)",
                                                order=1,
                                                questionnaire=self.questionnaire, name="Reported Cases")

        self.sub_section = SubSection.objects.create(title="Reported cases for the year 2013", order=1,
                                                     section=self.section_1)

        self.question1 = Question.objects.create(text='Disease', UID='C00001', answer_type='MultiChoice')
        self.question2 = Question.objects.create(text='B. Number of cases tested',
                                                 instructions="Enter the total number of cases for which specimens were collected, and tested in laboratory",
                                                 UID='C00003', answer_type='Number')

        self.question3 = Question.objects.create(text='C. Number of cases positive',
                                                 instructions="Include only those cases found positive for the infectious agent.",
                                                 UID='C00004', answer_type='Number')

        self.option1 = QuestionOption.objects.create(text='tusker lager', question=self.question1)
        self.option2 = QuestionOption.objects.create(text='tusker lager1', question=self.question1)
        self.option3 = QuestionOption.objects.create(text='tusker lager2', question=self.question1)

        self.question_group = QuestionGroup.objects.create(subsection=self.sub_section, order=1)
        self.question_group.question.add(self.question1, self.question3, self.question2)

        QuestionGroupOrder.objects.create(question_group=self.question_group, question=self.question1, order=1)
        QuestionGroupOrder.objects.create(question_group=self.question_group, question=self.question2, order=2)
        QuestionGroupOrder.objects.create(question_group=self.question_group, question=self.question3, order=3)

        self.data = {u'MultiChoice-MAX_NUM_FORMS': u'1', u'MultiChoice-TOTAL_FORMS': u'1',
                     u'MultiChoice-INITIAL_FORMS': u'1', u'MultiChoice-0-response': self.option1.id,
                     u'Number-INITIAL_FORMS': u'2', u'Number-TOTAL_FORMS': u'2', u'Number-MAX_NUM_FORMS': u'2',
                     u'Number-0-response': u'2', u'Number-1-response': u'33'}

        self.country = Country.objects.create(name="Uganda")

        self.initial = {'country': self.country, 'status': 'Draft', 'version': 1, 'code': 'ABC123',
                        'questionnaire': self.questionnaire}

    def test_section_form_is_valid_if_all_form_in_all_formsets_are_valid(self):
        questionnaire_entry_form = QuestionnaireEntryFormService(self.section_1, initial=self.initial, data=self.data)

        self.assertTrue(questionnaire_entry_form.is_valid())

    def test_section_form_is_invalid_if_any_form_in_any_formsets_are_invalid(self):
        invalid_data = self.data.copy()
        invalid_data[u'MultiChoice-0-response'] = -1

        questionnaire_entry_form = QuestionnaireEntryFormService(self.section_1, initial=self.initial,
                                                                 data=invalid_data)

        question1_form = questionnaire_entry_form.next_ordered_form(self.question1)

        self.assertFalse(questionnaire_entry_form.is_valid())
        error_message = 'Select a valid choice. That choice is not one of the available choices.'
        self.assertEqual([error_message], question1_form.errors['response'])

    def test_save_create_answer_objects(self):
        data = self.data
        self.failIf(MultiChoiceAnswer.objects.filter(response__id=int(data['MultiChoice-0-response'])))
        self.failIf(NumericalAnswer.objects.filter(response=int(data['Number-0-response'])))
        self.failIf(NumericalAnswer.objects.filter(response=int(data['Number-1-response'])))

        questionnaire_entry_form = QuestionnaireEntryFormService(self.section_1, initial=self.initial, data=data)
        questionnaire_entry_form.save()

        self.failUnless(
            MultiChoiceAnswer.objects.filter(response__id=int(data['MultiChoice-0-response']), question=self.question1))
        self.failUnless(
            NumericalAnswer.objects.filter(response=int(data['Number-0-response']), question=self.question2))
        self.failUnless(
            NumericalAnswer.objects.filter(response=int(data['Number-1-response']), question=self.question3))

    def test_save_groups_rows_into_answer_groups(self):
        data = self.data
        self.failIf(MultiChoiceAnswer.objects.filter(response__id=int(data['MultiChoice-0-response'])))
        self.failIf(NumericalAnswer.objects.filter(response=int(data['Number-0-response'])))
        self.failIf(NumericalAnswer.objects.filter(response=int(data['Number-1-response'])))
        self.failIf(AnswerGroup.objects.filter(grouped_question=self.question_group))

        questionnaire_entry_form = QuestionnaireEntryFormService(self.section_1, initial=self.initial, data=data)
        questionnaire_entry_form.save()

        primary = MultiChoiceAnswer.objects.get(response__id=int(data['MultiChoice-0-response']),
                                                question=self.question1)
        answer_1 = NumericalAnswer.objects.get(response=int(data['Number-0-response']), question=self.question2)
        answer_2 = NumericalAnswer.objects.get(response=int(data['Number-1-response']), question=self.question3)

        answer_group = AnswerGroup.objects.filter(grouped_question=self.question_group)

        self.assertEqual(3, answer_group.count())
        self.assertEqual(3, Answer.objects.select_subclasses().count())
        answer_group_answers = answer_group[0].answer.all().select_subclasses()
        self.assertEqual(1, answer_group_answers.count())
        self.assertNotIn(primary, answer_group_answers)
        self.assertNotIn(answer_1, answer_group_answers)
        self.assertIn(answer_2, answer_group_answers)
        [self.assertIn(answer.id, answer_group.values_list('answer', flat=True)) for answer in
         Answer.objects.select_subclasses()]

    def test_save_on_already_existing_draft_answers_modify_original_draft_answers_and_not_create_new_instance(self):
        data = self.data

        old_primary = MultiChoiceAnswer.objects.create(response=self.option1, question=self.question1, **self.initial)
        old_answer_1 = NumericalAnswer.objects.create(response=int(data['Number-0-response']), question=self.question2,
                                                      **self.initial)
        old_answer_2 = NumericalAnswer.objects.create(response=int(data['Number-1-response']), question=self.question3,
                                                      **self.initial)

        answer_group = AnswerGroup.objects.create(grouped_question=self.question_group)
        answer_group.answer.add(old_primary, old_answer_1, old_answer_2)

        data_modified = data.copy()
        data_modified['MultiChoice-0-response'] = self.option2.id
        data_modified['Number-1-response'] = '3'

        questionnaire_entry_form = QuestionnaireEntryFormService(self.section_1, initial=self.initial,
                                                                 data=data_modified)
        questionnaire_entry_form.is_valid()
        questionnaire_entry_form.save()

        primary = MultiChoiceAnswer.objects.get(response__id=int(data_modified['MultiChoice-0-response']),
                                                question=self.question1)
        answer_1 = NumericalAnswer.objects.get(response=int(data_modified['Number-0-response']),
                                               question=self.question2)
        answer_2 = NumericalAnswer.objects.get(response=int(data_modified['Number-1-response']),
                                               question=self.question3)

        self.assertEqual(old_primary.id, primary.id)
        self.assertEqual(old_answer_1.id, answer_1.id)
        self.assertEqual(old_answer_2.id, answer_2.id)

        answer_group = AnswerGroup.objects.filter(grouped_question=self.question_group)
        self.assertEqual(1, answer_group.count())

    def test_submit_changes_draft_answers_to_submitted_and_not_create_new_instances(self):
        data = self.data

        old_primary = MultiChoiceAnswer.objects.create(response=self.option1, question=self.question1, **self.initial)
        old_answer_1 = NumericalAnswer.objects.create(response=int(data['Number-0-response']), question=self.question2,
                                                      **self.initial)
        old_answer_2 = NumericalAnswer.objects.create(response=int(data['Number-1-response']), question=self.question3,
                                                      **self.initial)

        answer_group = AnswerGroup.objects.create(grouped_question=self.question_group)
        answer_group.answer.add(old_primary, old_answer_1, old_answer_2)

        data_modified = data.copy()
        data_modified['MultiChoice-0-response'] = self.option2.id
        data_modified['Number-1-response'] = '3'

        questionnaire_entry_form = QuestionnaireEntryFormService(self.section_1, initial=self.initial,
                                                                 data=data_modified)
        questionnaire_entry_form.save()

        primary = MultiChoiceAnswer.objects.get(response__id=int(data_modified['MultiChoice-0-response']),
                                                question=self.question1)
        answer_1 = NumericalAnswer.objects.get(response=int(data_modified['Number-0-response']),
                                               question=self.question2)
        answer_2 = NumericalAnswer.objects.get(response=int(data_modified['Number-1-response']),
                                               question=self.question3)

        self.assertEqual(old_primary.id, primary.id)
        self.assertEqual(old_answer_1.id, answer_1.id)
        self.assertEqual(old_answer_2.id, answer_2.id)

        answer_group = AnswerGroup.objects.filter(grouped_question=self.question_group)
        self.assertEqual(1, answer_group.count())

    def test_integer_casting_of_numeric_responses(self):
        question5 = Question.objects.create(text='C. Number of cases positive', UID='C00333', answer_type='Text')
        self.question_group.question.add(question5)
        QuestionGroupOrder.objects.create(question_group=self.question_group, question=question5, order=4)
        self.data.update({u'Text-MAX_NUM_FORMS': u'1', u'Text-TOTAL_FORMS': u'1', u'Text-INITIAL_FORMS': u'1'})

        data = self.data
        data_modified = data.copy()
        data_modified['MultiChoice-0-response'] = self.option2.id
        data_modified['Number-0-response'] = 3.0
        data_modified['Number-1-response'] = 3.05
        data_modified['Text-0-response'] = 'haha'

        questionnaire_entry_form = QuestionnaireEntryFormService(self.section_1, initial=self.initial,
                                                                 data=data_modified)
        questionnaire_entry_form.save()

        question1_form = questionnaire_entry_form.next_ordered_form(self.question1)
        question2_form = questionnaire_entry_form.next_ordered_form(self.question2)
        question3_form = questionnaire_entry_form.next_ordered_form(self.question3)
        question5_form = questionnaire_entry_form.next_ordered_form(question5)

        self.assertEqual(self.option2.id, question1_form['response'].value())
        self.assertEqual(3, question2_form['response'].value())
        self.assertEqual(3.05, question3_form['response'].value())
        self.assertEqual("haha", question5_form['response'].value())


class GridQuestionGroupEntryServiceTest(BaseTest):
    def setUp(self):
        self.questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English")

        self.section1 = Section.objects.create(title="Reported Cases of Selected Vaccine", order=1,
                                               questionnaire=self.questionnaire, name="Reported Cases")

        self.sub_section = SubSection.objects.create(title="subsection 1", order=1, section=self.section1)
        self.sub_section2 = SubSection.objects.create(title="subsection 2", order=2, section=self.section1)

        self.question_group = QuestionGroup.objects.create(subsection=self.sub_section, order=1, grid=True,
                                                           display_all=True)

        self.question1 = Question.objects.create(text='Favorite beer 1', UID='C00001', answer_type='MultiChoice',
                                                 is_primary=True)
        self.option1 = QuestionOption.objects.create(text='tusker lager', question=self.question1)
        self.option2 = QuestionOption.objects.create(text='tusker lager1', question=self.question1)
        self.option3 = QuestionOption.objects.create(text='tusker lager2', question=self.question1)

        self.question2 = Question.objects.create(text='question 2', instructions="instruction 2",
                                                 UID='C00002', answer_type='Text')

        self.question3 = Question.objects.create(text='question 3', instructions="instruction 3",
                                                 UID='C00003', answer_type='Number')

        self.question4 = Question.objects.create(text='question 4', instructions="instruction 2",
                                                 UID='C00005', answer_type='Date')
        self.question_group.question.add(self.question1, self.question3, self.question2, self.question4)

        QuestionGroupOrder.objects.create(question=self.question1, question_group=self.question_group, order=1)
        QuestionGroupOrder.objects.create(question=self.question2, question_group=self.question_group, order=2)
        QuestionGroupOrder.objects.create(question=self.question3, question_group=self.question_group, order=3)
        QuestionGroupOrder.objects.create(question=self.question4, question_group=self.question_group, order=4)
        self.country = Country.objects.create(name="Uganda")
        self.version = 1
        self.initial = {'country': self.country, 'status': 'Draft', 'version': self.version, 'code': 'ABC123',
                        'questionnaire': self.questionnaire}
        self.data = {u'MultiChoice-MAX_NUM_FORMS': u'3', u'MultiChoice-TOTAL_FORMS': u'3',
                     u'MultiChoice-INITIAL_FORMS': u'3', u'MultiChoice-0-response': self.option1.id,
                     u'MultiChoice-1-response': self.option2.id, u'MultiChoice-2-response': self.option3.id,
                     u'Number-MAX_NUM_FORMS': u'3', u'Number-TOTAL_FORMS': u'3',
                     u'Number-INITIAL_FORMS': u'3', u'Number-0-response': '22',
                     u'Number-1-response': '44', u'Number-2-response': '33',
                     u'Text-MAX_NUM_FORMS': u'3', u'Text-TOTAL_FORMS': u'3',
                     u'Text-INITIAL_FORMS': u'3', u'Text-0-response': 'Haha',
                     u'Text-1-response': 'Hehe', u'Text-2-response': 'hehehe',
                     u'Date-MAX_NUM_FORMS': u'3', u'Date-TOTAL_FORMS': u'3',
                     u'Date-INITIAL_FORMS': u'3', u'Date-0-response': '2014-2-2',
                     u'Date-1-response': '2014-2-2', u'Date-2-response': '2014-2-2',
        }

    def test_returns_multiple_forms_in_formsets_for_all_questions(self):
        questionnaire_entry_form = QuestionnaireEntryFormService(self.section1, initial=self.initial)
        formsets = questionnaire_entry_form._formsets()

        self.assertEqual(3, len(formsets['Number']))
        self.assertEqual(3, len(formsets['Text']))
        self.assertEqual(3, len(formsets['Date']))
        self.assertEqual(3, len(formsets['MultiChoice']))

    def test_returns_save_grid_with_display_all(self):
        data = self.data
        self.failIf(MultiChoiceAnswer.objects.filter(response__id=int(data['MultiChoice-0-response'])))
        self.failIf(MultiChoiceAnswer.objects.filter(response__id=int(data['MultiChoice-1-response'])))
        self.failIf(NumericalAnswer.objects.filter(response=int(data['Number-0-response'])))
        self.failIf(NumericalAnswer.objects.filter(response=int(data['Number-1-response'])))

        questionnaire_entry_form = QuestionnaireEntryFormService(self.section1, initial=self.initial, data=data)
        questionnaire_entry_form.is_valid()
        questionnaire_entry_form.save()

        self.failUnless(
            MultiChoiceAnswer.objects.filter(response__id=int(data['MultiChoice-0-response']), question=self.question1))
        self.failUnless(
            MultiChoiceAnswer.objects.filter(response__id=int(data['MultiChoice-1-response']), question=self.question1))
        self.failUnless(
            MultiChoiceAnswer.objects.filter(response__id=int(data['MultiChoice-2-response']), question=self.question1))

        self.failUnless(
            NumericalAnswer.objects.filter(response=int(data['Number-0-response']), question=self.question3))
        self.failUnless(
            NumericalAnswer.objects.filter(response=int(data['Number-1-response']), question=self.question3))
        self.failUnless(
            NumericalAnswer.objects.filter(response=int(data['Number-2-response']), question=self.question3))

        self.failUnless(TextAnswer.objects.filter(response=data['Text-0-response'], question=self.question2))
        self.failUnless(TextAnswer.objects.filter(response=data['Text-1-response'], question=self.question2))
        self.failUnless(TextAnswer.objects.filter(response=data['Text-2-response'], question=self.question2))

        self.failUnless(DateAnswer.objects.filter(response=data['Date-0-response'], question=self.question4))
        self.failUnless(DateAnswer.objects.filter(response=data['Date-1-response'], question=self.question4))
        self.failUnless(DateAnswer.objects.filter(response=data['Date-2-response'], question=self.question4))

    def test_returns_multiple_forms_in_formsets_for_all_questions_given_several_groups(self):
        question = Question.objects.create(text='Favorite beer 1', UID='C00033', answer_type='MultiChoice')
        yes = QuestionOption.objects.create(text='Yes', question=question)
        no = QuestionOption.objects.create(text='No', question=question)

        question_group = QuestionGroup.objects.create(subsection=self.sub_section, order=2)
        question_group.question.add(question)
        QuestionGroupOrder.objects.create(question=question, question_group=question_group, order=1)

        questionnaire_entry_form = QuestionnaireEntryFormService(self.section1, initial=self.initial)
        formsets = questionnaire_entry_form._formsets()

        self.assertEqual(3, len(formsets['Number']))
        self.assertEqual(3, len(formsets['Text']))
        self.assertEqual(3, len(formsets['Date']))
        self.assertEqual(4, len(formsets['MultiChoice']))

    def test_return_with_draft_answers_after_saving_drafts(self):
        question1_answer = MultiChoiceAnswer.objects.create(question=self.question1, country=self.country,
                                                            status=Answer.DRAFT_STATUS, response=self.option1,
                                                            questionnaire=self.questionnaire)
        question2_answer = TextAnswer.objects.create(question=self.question2, country=self.country,
                                                     status=Answer.DRAFT_STATUS, response="ayoyoyo",
                                                     questionnaire=self.questionnaire)
        question3_answer = NumericalAnswer.objects.create(question=self.question3, country=self.country,
                                                          status=Answer.DRAFT_STATUS, response=1,
                                                          questionnaire=self.questionnaire)
        answer_group1 = question1_answer.answergroup.create(grouped_question=self.question_group, row=1)
        answer_group1.answer.add(question2_answer, question3_answer)

        questionnaire_entry_form = QuestionnaireEntryFormService(self.section1, initial=self.initial)
        formsets = questionnaire_entry_form._formsets()

        self.assertEqual(self.question1, formsets['MultiChoice'][0].initial['question'])
        self.assertEqual(self.question2, formsets['Text'][0].initial['question'])
        self.assertEqual(self.question3, formsets['Number'][0].initial['question'])
        self.assertEqual(self.question4, formsets['Date'][0].initial['question'])

        self.assertEqual(question2_answer.response, formsets['Text'][0].initial['response'])
        self.assertEqual(question3_answer.response, formsets['Number'][0].initial['response'])

        self.assertIn('response', formsets['MultiChoice'][0].initial.keys())
        self.assertIn('response', formsets['Number'][0].initial.keys())
        self.assertIn('response', formsets['Text'][0].initial.keys())
        self.assertNotIn('response', formsets['Date'][0].initial.keys())

        self.assertEqual(question1_answer.response, formsets['MultiChoice'][0].initial['response'])
        self.assertEqual(question2_answer.response, formsets['Text'][0].initial['response'])
        self.assertEqual(question3_answer.response, formsets['Number'][0].initial['response'])

        self.assertIn('answer', formsets['MultiChoice'][0].initial.keys())
        self.assertIn('answer', formsets['Number'][0].initial.keys())
        self.assertIn('answer', formsets['Text'][0].initial.keys())
        self.assertNotIn('answer', formsets['Date'][0].initial.keys())

        self.assertEqual(question1_answer, formsets['MultiChoice'][0].initial['answer'])
        self.assertEqual(question2_answer, formsets['Text'][0].initial['answer'])
        self.assertEqual(question3_answer, formsets['Number'][0].initial['answer'])

    def test_return_with_multiple_row_draft_answers_after_saving_drafts(self):
        question1_answer = []
        question2_answer = []
        question3_answer = []
        answer_group1 = []

        for index, option in enumerate(self.question1.options.order_by('modified')):
            question1_answer.append(MultiChoiceAnswer.objects.create(question=self.question1, country=self.country,
                                                                     status=Answer.DRAFT_STATUS, response=option,
                                                                     questionnaire=self.questionnaire))
            question2_answer.append(TextAnswer.objects.create(question=self.question2, country=self.country,
                                                              status=Answer.DRAFT_STATUS, response="ayoyoyo %d" % index,
                                                              questionnaire=self.questionnaire))
            question3_answer.append(NumericalAnswer.objects.create(question=self.question3, country=self.country,
                                                                   status=Answer.DRAFT_STATUS, response=index,
                                                                   questionnaire=self.questionnaire))
            answer_group1.append(
                question1_answer[index].answergroup.create(grouped_question=self.question_group, row=1))
            answer_group1[index].answer.add(question2_answer[index], question3_answer[index])

        questionnaire_entry_form = QuestionnaireEntryFormService(self.section1, initial=self.initial)
        formsets = questionnaire_entry_form._formsets()

        for index, option in enumerate(self.question1.options.order_by('modified')):
            self.assertEqual(question1_answer[index].response,
                             formsets[self.question1.answer_type][index].initial['response'])
            self.assertEqual(question1_answer[index], formsets[self.question1.answer_type][index].initial['answer'])
            self.assertEqual(option, formsets[self.question1.answer_type][index].initial['option'])

            for index1, question in enumerate([self.question2, self.question3]):
                self.assertEqual(eval("question%d_answer[index].response" % (index1 + 2)),
                                 formsets[question.answer_type][index].initial['response'])
                self.assertEqual(eval("question%d_answer[index]" % (index1 + 2)),
                                 formsets[question.answer_type][index].initial['answer'])

    def test_initial_gets_answers_and_responses_after_draft_saved(self):
        question5 = Question.objects.create(text='question 5', instructions="instruction 5", UID='C00055',
                                            answer_type='Date')
        self.question_group.question.add(question5)

        QuestionGroupOrder.objects.create(question=question5, question_group=self.question_group, order=5)
        order = self.question_group.orders.order_by('order')

        question1_answer = []
        question2_answer = []
        question3_answer = []
        question4_answer = []
        question5_answer = []
        answer_group1 = []

        for index, option in enumerate(self.question1.options.order_by('modified')):
            question1_answer.append(MultiChoiceAnswer.objects.create(question=self.question1, country=self.country,
                                                                     status=Answer.DRAFT_STATUS, response=option,
                                                                     version=self.version,
                                                                     questionnaire=self.questionnaire))
            question2_answer.append(TextAnswer.objects.create(question=self.question2, country=self.country,
                                                              status=Answer.DRAFT_STATUS, response="ayoyoyo %d" % index,
                                                              version=self.version, questionnaire=self.questionnaire))
            question3_answer.append(NumericalAnswer.objects.create(question=self.question3, country=self.country,
                                                                   status=Answer.DRAFT_STATUS, response=index,
                                                                   version=self.version,
                                                                   questionnaire=self.questionnaire))
            question4_answer.append(DateAnswer.objects.create(question=self.question4, country=self.country,
                                                              status=Answer.DRAFT_STATUS,
                                                              response='2007-10-%d' % (index + 1),
                                                              version=self.version, questionnaire=self.questionnaire))
            question5_answer.append(DateAnswer.objects.create(question=question5, country=self.country,
                                                              status=Answer.DRAFT_STATUS,
                                                              response='2007-11-%d' % (index + 1),
                                                              version=self.version, questionnaire=self.questionnaire))
            answer_group1.append(
                question1_answer[index].answergroup.create(grouped_question=self.question_group, row=1))
            answer_group1[index].answer.add(question2_answer[index], question3_answer[index], question4_answer[index],
                                            question5_answer[index])

        questionnaire_entry_form = QuestionnaireEntryFormService(self.section1, initial=self.initial)

        for index, option in enumerate(self.question1.options.order_by('modified')):
            order_dict = {'option': option, 'order': order[0]}
            answer = answer_group1[index].answer.filter(question=self.question1).select_subclasses()[0]
            initial = {'question': self.question1, 'response': answer.response, 'answer': answer,
                       'version': self.version,
                       'group': self.question_group, 'country': self.country, 'option': option, 'code': 'ABC123',
                       'status': 'Draft', 'questionnaire': self.questionnaire}
            self.assertEqual(initial, questionnaire_entry_form._initial(order_dict))

            for index1, question in enumerate([self.question2, self.question3, self.question4, question5]):
                order_dict = {'option': option, 'order': order[index1 + 1]}
                answer = answer_group1[index].answer.filter(question=question).select_subclasses()[0]
                initial = {'question': question, 'response': answer.response, 'answer': answer, 'version': self.version,
                           'group': self.question_group, 'country': self.country, 'code': 'ABC123',
                           'status': 'Draft', 'questionnaire': self.questionnaire}
                self.assertEqual(initial, questionnaire_entry_form._initial(order_dict))

    def given_I_have_questions_and_corresponding_submitted_answers_in_a_section(self):
        section = Section.objects.create(title="another section", order=2, questionnaire=self.questionnaire,
                                         name="haha")
        sub_section = SubSection.objects.create(title="subsection in another section", order=1, section=section)
        question1 = Question.objects.create(text='q1', UID='C00011', answer_type='MultiChoice')
        question2 = Question.objects.create(text='q2', UID='C00033', answer_type='Number')
        question3 = Question.objects.create(text='q3', UID='C00034', answer_type='Number')

        option1 = QuestionOption.objects.create(text='tusker lager', question=question1)
        option2 = QuestionOption.objects.create(text='tusker lager1', question=question1)
        option3 = QuestionOption.objects.create(text='tusker lager2', question=question1)

        question_group = QuestionGroup.objects.create(subsection=sub_section, order=1)
        question_group.question.add(question1, question3, question2)

        QuestionGroupOrder.objects.create(question_group=question_group, question=question1, order=1)
        QuestionGroupOrder.objects.create(question_group=question_group, question=question2, order=2)
        QuestionGroupOrder.objects.create(question_group=question_group, question=question3, order=3)

        data = {u'MultiChoice-MAX_NUM_FORMS': u'1', u'MultiChoice-TOTAL_FORMS': u'1',
                u'MultiChoice-INITIAL_FORMS': u'1', u'MultiChoice-0-response': option1.id,
                u'Number-INITIAL_FORMS': u'2', u'Number-TOTAL_FORMS': u'2', u'Number-MAX_NUM_FORMS': u'2',
                u'Number-0-response': u'2', u'Number-1-response': u'33'}

        initial = self.initial.copy()
        initial['status'] = Answer.SUBMITTED_STATUS
        old_primary = MultiChoiceAnswer.objects.create(response=option1, question=question1, **initial)
        old_answer_1 = NumericalAnswer.objects.create(response=int(data['Number-0-response']), question=question2,
                                                      **initial)
        old_answer_2 = NumericalAnswer.objects.create(response=int(data['Number-1-response']), question=question3,
                                                      **initial)

        old_primary.answergroup.create(grouped_question=question_group)
        old_answer_1.answergroup.create(grouped_question=question_group)
        old_answer_2.answergroup.create(grouped_question=question_group)

        data_modified = data.copy()
        data_modified['MultiChoice-0-response'] = option2.id
        data_modified['Number-1-response'] = '3'

        old_answer = [old_primary, old_answer_1, old_answer_2]
        questions = [question1, question2, question3]

        return questions, question_group, old_answer, data_modified, section

    def and_given_I_have_other_questions_and_corresponding_answers_in_a_different_section(self):
        question1_answer = []
        question2_answer = []
        question3_answer = []
        answer_group1 = []

        for index, option in enumerate(self.question1.options.order_by('modified')):
            question1_answer.append(MultiChoiceAnswer.objects.create(question=self.question1, country=self.country,
                                                                     status=Answer.SUBMITTED_STATUS, response=option,
                                                                     version=self.version, questionnaire=self.questionnaire))
            question2_answer.append(TextAnswer.objects.create(question=self.question2, country=self.country,
                                                              status=Answer.SUBMITTED_STATUS, response="ayoyoyo %d" % index,
                                                              version=self.version, questionnaire=self.questionnaire))
            question3_answer.append(NumericalAnswer.objects.create(question=self.question3, country=self.country,
                                                                   status=Answer.SUBMITTED_STATUS, response=index,
                                                                   version=self.version, questionnaire=self.questionnaire))
            answer_group1.append(question1_answer[index].answergroup.create(grouped_question=self.question_group, row=index))
            answer_group1[index].answer.add(question2_answer[index], question3_answer[index])

    def test_submitted_answers_and_answer_groups_of_other_sections_are_duplicated_on_save_of_edit_submitted_answers(
            self):
        questions, question_group, old_answer, data_modified, section = self.given_I_have_questions_and_corresponding_submitted_answers_in_a_section()
        self.and_given_I_have_other_questions_and_corresponding_answers_in_a_different_section()

        initial = self.initial.copy()
        initial['version'] = self.version + 1
        questionnaire_entry_form = QuestionnaireEntryFormService(section, initial=initial, data=data_modified,
                                                                 edit_after_submit=True)
        questionnaire_entry_form.save()

        primary = MultiChoiceAnswer.objects.get(response__id=int(data_modified['MultiChoice-0-response']),
                                                question=questions[0], version=self.version + 1)
        answer_1 = NumericalAnswer.objects.get(response=int(data_modified['Number-0-response']), question=questions[1],
                                               version=self.version + 1)
        answer_2 = NumericalAnswer.objects.get(response=int(data_modified['Number-1-response']), question=questions[2],
                                               version=self.version + 1)

        self.assertNotEqual(old_answer[0].id, primary.id)
        self.assertNotEqual(old_answer[1].id, answer_1.id)
        self.assertNotEqual(old_answer[2].id, answer_2.id)

        self.assertEqual(primary.status, Answer.DRAFT_STATUS)
        self.assertEqual(answer_1.status, Answer.DRAFT_STATUS)
        self.assertEqual(answer_2.status, Answer.DRAFT_STATUS)

        self.failUnless(primary.answergroup.filter(grouped_question=question_group))
        self.failUnless(answer_1.answergroup.filter(grouped_question=question_group))
        self.failUnless(answer_2.answergroup.filter(grouped_question=question_group))

        for index, option in enumerate(self.question1.options.order_by('modified')):
            question1_answer = MultiChoiceAnswer.objects.filter(question=self.question1, country=self.country,
                                                                status=Answer.DRAFT_STATUS, response=option,
                                                                version=self.version + 1, questionnaire=self.questionnaire)
            question2_answer = TextAnswer.objects.filter(question=self.question2, country=self.country,
                                                         status=Answer.DRAFT_STATUS, response="ayoyoyo %d" % index,
                                                         version=self.version + 1, questionnaire=self.questionnaire)
            question3_answer = NumericalAnswer.objects.filter(question=self.question3, country=self.country,
                                                              status=Answer.DRAFT_STATUS, response=index,
                                                              version=self.version + 1, questionnaire=self.questionnaire)

            self.failUnless(question1_answer)
            self.assertEqual(1, question1_answer.count())
            self.failUnless(question2_answer)
            self.assertEqual(1, question2_answer.count())
            self.failUnless(question3_answer)
            self.assertEqual(1, question3_answer.count())

            answer_group1 = question1_answer[0].answergroup.filter(grouped_question=self.question_group, row=index)
            self.failUnless(answer_group1)
            answer_group_answers = answer_group1[0].answer.all().select_subclasses()
            self.assertEqual(3, answer_group_answers.count())
            self.assertIn(question2_answer[0], answer_group_answers)
            self.assertIn(question3_answer[0], answer_group_answers)


class AllowMultiplesGridEntryServiceTest(BaseTest):
    def setUp(self):
        self.questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English")

        self.section1 = Section.objects.create(title="Reported Cases of Selected Vaccine", order=1,
                                               questionnaire=self.questionnaire, name="Reported Cases")

        self.sub_section = SubSection.objects.create(title="subsection 1", order=1, section=self.section1)
        self.sub_section2 = SubSection.objects.create(title="subsection 2", order=2, section=self.section1)

        self.question_group = QuestionGroup.objects.create(subsection=self.sub_section, order=1, grid=True,
                                                           allow_multiples=True)

        self.question1 = Question.objects.create(text='Favorite beer 1', UID='C00001', answer_type='MultiChoice', is_primary=True)
        self.option1 = QuestionOption.objects.create(text='tusker lager', question=self.question1)
        self.option2 = QuestionOption.objects.create(text='tusker lager1', question=self.question1)
        self.option3 = QuestionOption.objects.create(text='tusker lager2', question=self.question1)

        self.question2 = Question.objects.create(text='question 2 - text', instructions="instruction 2",
                                                 UID='C00002', answer_type='Text')

        self.question3 = Question.objects.create(text='question 3 - number', instructions="instruction 3",
                                                 UID='C00003', answer_type='Number')

        self.question4 = Question.objects.create(text='question 4 - date', instructions="instruction 2",
                                                 UID='C00005', answer_type='Date')

        self.question_group.question.add(self.question1, self.question3, self.question2, self.question4)

        QuestionGroupOrder.objects.create(question=self.question1, question_group=self.question_group, order=1)
        QuestionGroupOrder.objects.create(question=self.question2, question_group=self.question_group, order=2)
        QuestionGroupOrder.objects.create(question=self.question3, question_group=self.question_group, order=3)
        QuestionGroupOrder.objects.create(question=self.question4, question_group=self.question_group, order=4)
        self.country = Country.objects.create(name="Uganda")
        self.version = 1
        self.initial = {'country': self.country, 'status': 'Draft', 'version': self.version, 'code': 'ABC123'}
        self.data = {u'MultiChoice-MAX_NUM_FORMS': u'3', u'MultiChoice-TOTAL_FORMS': u'3',
                u'MultiChoice-INITIAL_FORMS': u'3', u'MultiChoice-0-response': ['0,%d' % self.question_group.id, self.option1.id],
                u'MultiChoice-1-response': [ '1,%d' % self.question_group.id, self.option2.id], u'MultiChoice-2-response': ['2,%d' % self.question_group.id, self.option3.id],
                u'Number-MAX_NUM_FORMS': u'3', u'Number-TOTAL_FORMS': u'3',
                u'Number-INITIAL_FORMS': u'3', u'Number-0-response': ['0,%d' % self.question_group.id, '22'],
                u'Number-1-response': [ '1,%d' % self.question_group.id, '44'], u'Number-2-response': ['2,%d' % self.question_group.id, '33'],
                u'Text-MAX_NUM_FORMS': u'3', u'Text-TOTAL_FORMS': u'3',
                u'Text-INITIAL_FORMS': u'3', u'Text-0-response': ['0,%d' % self.question_group.id, 'Haha'],
                u'Text-1-response': [ '1,%d' % self.question_group.id, 'Hehe',], u'Text-2-response': ['2,%d' % self.question_group.id, 'hehehe'],
                u'Date-MAX_NUM_FORMS': u'3', u'Date-TOTAL_FORMS': u'3',
                u'Date-INITIAL_FORMS': u'3', u'Date-0-response': ['0,%d' % self.question_group.id, '2014-2-22', ],
                u'Date-1-response': [ '1,%d' % self.question_group.id, '2014-2-21'], u'Date-2-response': ['2,%d' % self.question_group.id, '2014-2-23'],
            }

    def test_returns_multiple_forms_in_formsets_for_all_questions(self):
        questionnaire_entry_form = QuestionnaireEntryFormService(self.section1, initial=self.initial, data=self.data)
        formsets = questionnaire_entry_form._formsets()

        self.assertEqual(3, len(formsets['Number']))
        self.assertEqual(3, len(formsets['Text']))
        self.assertEqual(3, len(formsets['Date']))
        self.assertEqual(3, len(formsets['MultiChoice']))

    def test__returns_multiple_forms_in_formsets__when_there_are_more_than_one_grid_of_the_same_type_and_get_initial(self):
        sub_section = SubSection.objects.create(title="subs", order=3, section=self.section1)

        question_group = QuestionGroup.objects.create(subsection=sub_section, order=1, grid=True,
                                                      allow_multiples=True)

        question1 = Question.objects.create(text='Favorite bar', UID='C00011', answer_type='MultiChoice', is_primary=True)
        option1 = QuestionOption.objects.create(text='bubles', question=question1)
        option2 = QuestionOption.objects.create(text='Iguana', question=question1)
        option3 = QuestionOption.objects.create(text='big mikes', question=question1)

        question2 = Question.objects.create(text='q2',  UID='C00012', answer_type='Text')

        question_group.question.add(question1, question2)

        QuestionGroupOrder.objects.create(question=question1, question_group=question_group, order=1)
        QuestionGroupOrder.objects.create(question=question2, question_group=question_group, order=2)

        sub_section1 = SubSection.objects.create(title="subs1", order=4, section=self.section1)

        question_group1 = QuestionGroup.objects.create(subsection=sub_section1, order=1)

        question11 = Question.objects.create(text='Favorite spirit', UID='C00111', answer_type='MultiChoice', is_primary=True)
        option11 = QuestionOption.objects.create(text='waragi', question=question11)
        option21 = QuestionOption.objects.create(text='bond7', question=question11)
        option31 = QuestionOption.objects.create(text='V&A', question=question11)

        question21 = Question.objects.create(text='q21',  UID='C00112', answer_type='Text')

        question_group1.question.add(question11, question21)

        QuestionGroupOrder.objects.create(question=question11, question_group=question_group1, order=1)
        QuestionGroupOrder.objects.create(question=question21, question_group=question_group1, order=2)

        data = {u'MultiChoice-MAX_NUM_FORMS': u'6', u'MultiChoice-TOTAL_FORMS': u'6',
             u'MultiChoice-INITIAL_FORMS': u'6', u'MultiChoice-0-response': ['0,%d'%self.question_group.id, option11.id],
             u'MultiChoice-1-response': ['1,%d'%self.question_group.id, 2,], u'MultiChoice-2-response': [ '2,%d'%self.question_group.id, 3],
             u'MultiChoice-3-response': ['0,%d'%question_group.id, option21.id,], u'MultiChoice-4-response': [ '1,%d'%question_group.id, 6,],
             u'MultiChoice-5-response': [2],
             u'Number-MAX_NUM_FORMS': u'3', u'Number-TOTAL_FORMS': u'3',
             u'Number-INITIAL_FORMS': u'3', u'Number-0-response': ['0,%d'%self.question_group.id, '22',],
             u'Number-1-response': ['1,%d'%self.question_group.id, '44',],  u'Number-2-response': ['2,%d'%self.question_group.id, '33', ],
             u'Text-MAX_NUM_FORMS': u'6', u'Text-TOTAL_FORMS': u'6',
             u'Text-INITIAL_FORMS': u'6', u'Text-0-response': ['0,%d'%self.question_group.id, 'Haha',],
             u'Text-1-response': ['1,%d'%self.question_group.id, 'Hehe',],  u'Text-2-response': ['2,%d'%self.question_group.id, 'hehehe', ],
             u'Text-3-response': ['0,%d'%question_group.id, 'Hehe1',], u'Text-4-response': ['1,%d'%question_group.id, 'Hehe',],
             u'Text-5-response': ['hehe2'],
             u'Date-MAX_NUM_FORMS': u'3', u'Date-TOTAL_FORMS': u'3',
             u'Date-INITIAL_FORMS': u'3', u'Date-0-response': ['0,%d'%self.question_group.id, '2014-2-2', ],
             u'Date-1-response': ['1,%d'%self.question_group.id, '2014-2-2',],  u'Date-2-response': ['2,%d'%self.question_group.id, '2014-2-2',],
             }

        questionnaire_entry_form = QuestionnaireEntryFormService(self.section1, initial=self.initial, data=data)
        formsets = questionnaire_entry_form._formsets()

        self.assertEqual(3, len(formsets['Number']))
        self.assertEqual(6, len(formsets['Text']))
        self.assertEqual(3, len(formsets['Date']))
        self.assertEqual(6, len(formsets['MultiChoice']))

        self.assertEqual(self.question3, formsets['Number'][0].initial['question'])
        self.assertEqual(self.question3, formsets['Number'][1].initial['question'])
        self.assertEqual(self.question3, formsets['Number'][2].initial['question'])

        self.assertEqual(self.question2, formsets['Text'][0].initial['question'])
        self.assertEqual(self.question2, formsets['Text'][1].initial['question'])
        self.assertEqual(self.question2, formsets['Text'][2].initial['question'])
        self.assertEqual(question2, formsets['Text'][3].initial['question'])
        self.assertEqual(question2, formsets['Text'][4].initial['question'])
        self.assertEqual(question21, formsets['Text'][5].initial['question'])

        self.assertEqual(self.question4, formsets['Date'][0].initial['question'])
        self.assertEqual(self.question4, formsets['Date'][1].initial['question'])
        self.assertEqual(self.question4, formsets['Date'][2].initial['question'])

        self.assertEqual(self.question1, formsets['MultiChoice'][0].initial['question'])
        self.assertEqual(self.question1, formsets['MultiChoice'][1].initial['question'])
        self.assertEqual(self.question1, formsets['MultiChoice'][2].initial['question'])
        self.assertEqual(question1, formsets['MultiChoice'][3].initial['question'])
        self.assertEqual(question1, formsets['MultiChoice'][4].initial['question'])
        self.assertEqual(question11, formsets['MultiChoice'][5].initial['question'])

    def test_save_answers_and_answer_groups(self):
        data=self.data
        query_dict_data = self.cast_to_queryDict(data)

        self.failIf(MultiChoiceAnswer.objects.filter(response__id=int(data['MultiChoice-0-response'][-1])))
        self.failIf(MultiChoiceAnswer.objects.filter(response__id=int(data['MultiChoice-1-response'][-1])))
        self.failIf(MultiChoiceAnswer.objects.filter(response__id=int(data['MultiChoice-2-response'][-1])))
        self.failIf(NumericalAnswer.objects.filter(response=int(data['Number-0-response'][-1])))
        self.failIf(NumericalAnswer.objects.filter(response=int(data['Number-1-response'][-1])))
        self.failIf(NumericalAnswer.objects.filter(response=int(data['Number-2-response'][-1])))
        self.failIf(TextAnswer.objects.filter(response=data['Text-0-response'][-1]))
        self.failIf(TextAnswer.objects.filter(response=data['Text-1-response'][-1]))
        self.failIf(TextAnswer.objects.filter(response=data['Text-2-response'][-1]))
        self.failIf(DateAnswer.objects.filter(response=data['Date-0-response'][-1]))
        self.failIf(DateAnswer.objects.filter(response=data['Date-1-response'][-1]))
        self.failIf(DateAnswer.objects.filter(response=data['Date-2-response'][-1]))

        questionnaire_entry_form = QuestionnaireEntryFormService(self.section1, initial=self.initial, data=query_dict_data)
        questionnaire_entry_form.is_valid()
        questionnaire_entry_form.save()

        question1_answer0 = MultiChoiceAnswer.objects.get(response__id=int(data['MultiChoice-0-response'][-1]),
                                                             question=self.question1)
        question1_answer1 = MultiChoiceAnswer.objects.get(response__id=int(data['MultiChoice-1-response'][-1]),
                                                          question=self.question1)
        question1_answer2 = MultiChoiceAnswer.objects.get(response__id=int(data['MultiChoice-2-response'][-1]),
                                                             question=self.question1)

        question3_answer0 = NumericalAnswer.objects.get(response=int(data['Number-0-response'][-1]),
                                                           question=self.question3)
        question3_answer1 = NumericalAnswer.objects.get(response=int(data['Number-1-response'][-1]),
                                                        question=self.question3)
        question3_answer2 = NumericalAnswer.objects.get(response=int(data['Number-2-response'][-1]),
                                                           question=self.question3)

        question2_answer0 = TextAnswer.objects.get(response=data['Text-0-response'][-1], question=self.question2)
        question2_answer1 = TextAnswer.objects.get(response=data['Text-1-response'][-1], question=self.question2)
        question2_answer2 = TextAnswer.objects.get(response=data['Text-2-response'][-1], question=self.question2)

        question4_answer0 = DateAnswer.objects.get(response=data['Date-0-response'][-1], question=self.question4)
        question4_answer1 = DateAnswer.objects.get(response=data['Date-1-response'][-1], question=self.question4)
        question4_answer2 = DateAnswer.objects.get(response=data['Date-2-response'][-1], question=self.question4)

        answer_group_row_0 = question1_answer0.answergroup.get(grouped_question=self.question_group)
        answer_group_row_0_answers = answer_group_row_0.answer.all().select_subclasses()
        self.assertEqual(4, answer_group_row_0_answers.count())
        self.assertIn(question2_answer0, answer_group_row_0_answers)
        self.assertIn(question3_answer0, answer_group_row_0_answers)
        self.assertIn(question4_answer0, answer_group_row_0_answers)

        answer_group_row_1 = question1_answer1.answergroup.get(grouped_question=self.question_group)
        answer_group_row_1_answers = answer_group_row_1.answer.all().select_subclasses()
        self.assertEqual(4, answer_group_row_1_answers.count())
        self.assertIn(question2_answer1, answer_group_row_1_answers)
        self.assertIn(question3_answer1, answer_group_row_1_answers)
        self.assertIn(question4_answer1, answer_group_row_1_answers)

        answer_group_row_2 = question1_answer2.answergroup.get(grouped_question=self.question_group)
        answer_group_row_2_answers = answer_group_row_2.answer.all().select_subclasses()
        self.assertEqual(4, answer_group_row_2_answers.count())
        self.assertIn(question2_answer2, answer_group_row_2_answers)
        self.assertIn(question3_answer2, answer_group_row_2_answers)
        self.assertIn(question4_answer2, answer_group_row_2_answers)

    def test_save_answers_and_answer_groups_when_there_are_more_than_one_grid_and_same_answer_type_in_the_same_grid(self):
        sub_section = SubSection.objects.create(title="subs", order=3, section=self.section1)

        question_group = QuestionGroup.objects.create(subsection=sub_section, order=1, grid=True,
                                                      allow_multiples=True)

        question1 = Question.objects.create(text='Favorite bar', UID='C00011', answer_type='MultiChoice', is_primary=True)
        option1 = QuestionOption.objects.create(text='bubles', question=question1)
        option2 = QuestionOption.objects.create(text='Iguana', question=question1)
        option3 = QuestionOption.objects.create(text='big mikes', question=question1)

        question2 = Question.objects.create(text='q2',  UID='C00012', answer_type='Text')
        question3 = Question.objects.create(text='another text q2',  UID='C00013', answer_type='Text')

        question_group.question.add(question1, question2, question3)

        QuestionGroupOrder.objects.create(question=question1, question_group=question_group, order=1)
        QuestionGroupOrder.objects.create(question=question2, question_group=question_group, order=2)
        QuestionGroupOrder.objects.create(question=question3, question_group=question_group, order=3)

        sub_section1 = SubSection.objects.create(title="subs1", order=4, section=self.section1)

        question_group1 = QuestionGroup.objects.create(subsection=sub_section1, order=1, name="not grid group")

        question11 = Question.objects.create(text='Favorite spirit', UID='C00111', answer_type='MultiChoice', is_primary=True)
        option11 = QuestionOption.objects.create(text='waragi', question=question11)
        option21 = QuestionOption.objects.create(text='bond7', question=question11)
        option31 = QuestionOption.objects.create(text='V&A', question=question11)

        question21 = Question.objects.create(text='q21',  UID='C00112', answer_type='Text')

        question_group1.question.add(question11, question21)

        QuestionGroupOrder.objects.create(question=question11, question_group=question_group1, order=1)
        QuestionGroupOrder.objects.create(question=question21, question_group=question_group1, order=2)

        data = {
            u'MultiChoice-MAX_NUM_FORMS': u'6', u'MultiChoice-TOTAL_FORMS': u'6', u'MultiChoice-INITIAL_FORMS': u'6',
            u'MultiChoice-0-response': ['0,%d' % self.question_group.id, self.option1.id],
            u'MultiChoice-1-response': ['1,%d' % self.question_group.id, self.option2.id],
            u'MultiChoice-2-response': ['2,%d' % self.question_group.id, self.option3.id],
            u'MultiChoice-3-response': ['0,%d' % question_group.id, option1.id],
            u'MultiChoice-4-response': ['1,%d' % question_group.id, option2.id],
            u'MultiChoice-5-response': [option11.id],
            u'Number-MAX_NUM_FORMS': u'3', u'Number-TOTAL_FORMS': u'3', u'Number-INITIAL_FORMS': u'3',
            u'Number-0-response': ['0,%d' % self.question_group.id, '22'],
            u'Number-1-response': ['1,%d' % self.question_group.id, '44'],
            u'Number-2-response': ['2,%d' % self.question_group.id, '33'],
            u'Text-MAX_NUM_FORMS': u'8', u'Text-TOTAL_FORMS': u'8', u'Text-INITIAL_FORMS': u'8',
            u'Text-0-response': ['0,%d' % self.question_group.id, 'row-0-self'],
            u'Text-1-response': ['1,%d' % self.question_group.id, 'row-1-self'],
            u'Text-2-response': ['2,%d' % self.question_group.id, 'row-2-self'],
            u'Text-3-response': ['0,%d' % question_group.id, 'row0-next-grid'],
            u'Text-4-response': ['0,%d' % question_group.id, 'second-text-row0-next-grid'],
            u'Text-5-response': ['1,%d' % question_group.id, 'row-1-next-grid'],
            u'Text-6-response': ['1,%d' % question_group.id, 'second-text-row1-next-grid'],
            u'Text-7-response': ['row-0-non-grid'],
            u'Date-MAX_NUM_FORMS': u'3', u'Date-TOTAL_FORMS': u'3', u'Date-INITIAL_FORMS': u'3',
            u'Date-0-response': ['0,%d' % self.question_group.id, '2014-2-21'],
            u'Date-1-response': ['1,%d' % self.question_group.id, '2014-2-22'],
            u'Date-2-response': ['2,%d' % self.question_group.id, '2014-2-23'],
            }

        for index in range(5):
            self.failIf(MultiChoiceAnswer.objects.filter(response__id=int(data['MultiChoice-%d-response'%index][-1])))
        for index in range(3):
            self.failIf(NumericalAnswer.objects.filter(response=int(data['Number-%d-response'%index][-1])))
            self.failIf(DateAnswer.objects.filter(response=data['Date-%d-response'%index][-1]))
        for index in range(8):
            self.failIf(TextAnswer.objects.filter(response=data['Text-%d-response'%index][-1]))

        query_dict_data = self.cast_to_queryDict(data)
        questionnaire_entry_form = QuestionnaireEntryFormService(self.section1, initial=self.initial, data=query_dict_data)
        questionnaire_entry_form.is_valid()
        questionnaire_entry_form.save()


        ordered_multichoice_question =[self.question1, self.question1, self.question1,  question1, question1, question11]
        multichoice_answers = []
        for index in range(6):
            multichoice_answers.append(MultiChoiceAnswer.objects.get(response__id=int(data['MultiChoice-%d-response'%index][-1]),
                                                             question=ordered_multichoice_question[index]))
        number_answers = []
        date_answers = []
        for index in range(3):
            number_answers.append(NumericalAnswer.objects.get(response=int(data['Number-%d-response'%index][-1]),
                                                               question=self.question3))
            date_answers.append(DateAnswer.objects.get(response=data['Date-%d-response' % index][-1], question=self.question4))

        ordered_text_question =[self.question2, self.question2, self.question2,  question2, question3, question2, question3, question21]
        text_answers = []
        for index in range(8):
            text_answers.append(TextAnswer.objects.get(response=data['Text-%d-response' % index][-1], question=ordered_text_question[index]))

        FIRST_GROUP_GRID = range(3)
        for index in FIRST_GROUP_GRID:
            answer_group_row= multichoice_answers[index].answergroup.get(grouped_question=self.question_group)
            answer_group_row_answers = answer_group_row.answer.all().select_subclasses()
            self.assertEqual(4, answer_group_row_answers.count())
            self.assertIn(number_answers[index], answer_group_row_answers)
            self.assertIn(text_answers[index], answer_group_row_answers)
            self.assertIn(date_answers[index], answer_group_row_answers)

        SECOND_GROUP_GRID = range(2)
        for index in SECOND_GROUP_GRID:
            answer_group_row= multichoice_answers[3+index].answergroup.get(grouped_question=question_group)
            answer_group_row_answers = answer_group_row.answer.all().select_subclasses()
            self.assertEqual(3, answer_group_row_answers.count())
            self.assertIn(text_answers[2*index+3], answer_group_row_answers)
            self.assertIn(text_answers[2*(index+1)+2], answer_group_row_answers)

        LAST_GROUP_NOT_GRID = range(1)
        for index in LAST_GROUP_NOT_GRID:
            non_grid_multichoice_answer_group = multichoice_answers[-1].answergroup.get(grouped_question=question_group1)
            non_grid_text_answer_group = text_answers[-1].answergroup.get(grouped_question=question_group1)
            self.assertEqual(1, non_grid_multichoice_answer_group.answer.count())
            self.assertEqual(1, non_grid_text_answer_group.answer.count())