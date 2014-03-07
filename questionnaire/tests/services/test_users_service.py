from django.contrib.auth.models import User
from questionnaire.models import Questionnaire, Section, SubSection, QuestionGroup, Question, QuestionGroupOrder, Country, QuestionOption, MultiChoiceAnswer, NumericalAnswer, AnswerGroup, UserProfile, Answer
from questionnaire.services.questionnaire_entry_form_service import QuestionnaireEntryFormService
from questionnaire.services.users import UserQuestionnaireService
from questionnaire.tests.base_test import BaseTest


class UserServiceTest(BaseTest):

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

        self.country = Country.objects.create(name="Uganda", code="UGA")
        self.user = User.objects.create(username="rajni")
        UserProfile.objects.create(user=self.user, country=self.country)

        self.initial = {'country': self.country, 'status': 'Draft', 'version':1, 'code': 'ABC123'}

    def test_user_knows_its_country_answers(self):
        data = self.data

        old_primary = MultiChoiceAnswer.objects.create(response=self.option1, question=self.question1, **self.initial)
        old_answer_1 = NumericalAnswer.objects.create(response=int(data['Number-0-response']), question=self.question2, **self.initial)
        old_answer_2 = NumericalAnswer.objects.create(response=int(data['Number-1-response']), question=self.question3, **self.initial)

        answer_group = AnswerGroup.objects.create(grouped_question=self.question_group)
        answer_group.answer.add(old_primary, old_answer_1, old_answer_2)

        user_service = UserQuestionnaireService(self.user, self.questionnaire)
        user_answers = user_service.all_answers()

        self.assertEqual(3, len(user_answers))

        self.assertIn(old_primary, user_answers)
        self.assertIn(old_answer_1, user_answers)
        self.assertIn(old_answer_2, user_answers)

    def test_user_knows_answers_given_questionnaire(self):
        data = self.data
        old_primary = MultiChoiceAnswer.objects.create(response=self.option1, question=self.question1, **self.initial)
        old_answer_1 = NumericalAnswer.objects.create(response=int(data['Number-0-response']), question=self.question2, **self.initial)
        old_answer_2 = NumericalAnswer.objects.create(response=int(data['Number-1-response']), question=self.question3, **self.initial)

        answer_group = AnswerGroup.objects.create(grouped_question=self.question_group)
        answer_group.answer.add(old_primary, old_answer_1, old_answer_2)

        other_questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English",
                                                            description="From dropbox as given by Rouslan")
        other_section_1 = Section.objects.create(title="Reported Cases of Selected Vaccine Preventable Diseases (VPDs)",
                                                order=1, questionnaire=other_questionnaire, name="Reported Cases")
        other_sub_section = SubSection.objects.create(title="Reported cases for the year 2013", order=1,
                                                        section=other_section_1)
        other_question1 = Question.objects.create(text='Disease', UID='C00011', answer_type='Number')
        other_question_group = QuestionGroup.objects.create(subsection=other_sub_section, order=1)
        other_question_group.question.add(other_question1)
        other_answer_1 = NumericalAnswer.objects.create(response=1, question=other_question1)

        section_2 = Section.objects.create(title="Section 2", order=2, questionnaire=self.questionnaire, name="section2")
        sub_section2 = SubSection.objects.create(title="subsection 2", order=1, section=section_2)
        question1 = Question.objects.create(text='question 1', UID='C00013', answer_type='Number')
        question2 = Question.objects.create(text='question 2', UID='C00014', answer_type='Number')

        question_group = QuestionGroup.objects.create(subsection=sub_section2, order=1)
        question_group.question.add(question1, question2)

        QuestionGroupOrder.objects.create(question=question1, order=1, question_group=question_group)
        QuestionGroupOrder.objects.create(question=question2, order=2, question_group=question_group)

        answer_1 = NumericalAnswer.objects.create(response=1, question=question1, status=Answer.DRAFT_STATUS, country=self.country)
        answer_2 = NumericalAnswer.objects.create(response=2, question=question2, status=Answer.DRAFT_STATUS, country=self.country)

        answer_group = AnswerGroup.objects.create(grouped_question=question_group)
        answer_group.answer.add(answer_1, answer_2)

        user_service = UserQuestionnaireService(self.user, self.questionnaire)
        user_answers = user_service.questionnaire_answers()

        self.assertEqual(5, len(user_answers))

        self.assertIn(old_primary, user_answers)
        self.assertIn(old_answer_1, user_answers)
        self.assertIn(old_answer_2, user_answers)
        self.assertNotIn(other_answer_1, user_answers)

        self.assertIn(answer_1, user_answers)
        self.assertIn(answer_2, user_answers)

    def test_submit_changes_draft_answers_to_submitted_and_not_create_new_instances(self):
        data = self.data

        old_primary = MultiChoiceAnswer.objects.create(response=self.option1, question=self.question1, **self.initial)
        old_answer_1 = NumericalAnswer.objects.create(response=int(data['Number-0-response']), question=self.question2, **self.initial)
        old_answer_2 = NumericalAnswer.objects.create(response=int(data['Number-1-response']), question=self.question3, **self.initial)

        answer_group = AnswerGroup.objects.create(grouped_question=self.question_group)
        answer_group.answer.add(old_primary, old_answer_1, old_answer_2)

        user_service = UserQuestionnaireService(self.user, self.questionnaire)
        user_service.submit()

        primary = MultiChoiceAnswer.objects.get(response__id=int(data['MultiChoice-0-response']), question=self.question1)
        answer_1 = NumericalAnswer.objects.get(response=int(data['Number-0-response']), question=self.question2)
        answer_2 = NumericalAnswer.objects.get(response=int(data['Number-1-response']), question=self.question3)

        self.assertEqual(old_primary.id, primary.id)
        self.assertEqual(Answer.SUBMITTED_STATUS, primary.status)

        self.assertEqual(old_answer_1.id, answer_1.id)
        self.assertEqual(Answer.SUBMITTED_STATUS, answer_1.status)

        self.assertEqual(old_answer_2.id, answer_2.id)
        self.assertEqual(Answer.SUBMITTED_STATUS, answer_2.status)

        answer_group = AnswerGroup.objects.filter(grouped_question=self.question_group)
        self.assertEqual(1, answer_group.count())

    def test_user_knows_answer_version_of_questionnaire_is_1_if_no_answer_exist_yet(self):
        user_service = UserQuestionnaireService(self.user, self.questionnaire)
        self.assertEqual(1, user_service.answer_version())
        self.assertEqual(1, user_service.POST_version)
        self.assertEqual(1, user_service.GET_version)

    def test_user_knows_answer_version_of_questionnaire_is_the_same_as_draft_if_draft_exists(self):
        data = self.data

        old_primary = MultiChoiceAnswer.objects.create(response=self.option1, question=self.question1, **self.initial)
        old_answer_1 = NumericalAnswer.objects.create(response=int(data['Number-0-response']), question=self.question2, **self.initial)
        old_answer_2 = NumericalAnswer.objects.create(response=int(data['Number-1-response']), question=self.question3, **self.initial)

        answer_group = AnswerGroup.objects.create(grouped_question=self.question_group)
        answer_group.answer.add(old_primary, old_answer_1, old_answer_2)

        user_service = UserQuestionnaireService(self.user, self.questionnaire)
        self.assertEqual(self.initial['version'], user_service.answer_version())
        self.assertEqual(self.initial['version'], user_service.POST_version)
        self.assertEqual(self.initial['version'], user_service.GET_version)

    def test_user_knows_answer_version_of_questionnaire_is_plus_1_of_the_latest_submitted_answers(self):
        data = self.data.copy()

        old_primary = MultiChoiceAnswer.objects.create(response=self.option1, question=self.question1, **self.initial)
        old_answer_1 = NumericalAnswer.objects.create(response=int(data['Number-0-response']), question=self.question2, **self.initial)
        old_answer_2 = NumericalAnswer.objects.create(response=int(data['Number-1-response']), question=self.question3, **self.initial)

        answer_group = AnswerGroup.objects.create(grouped_question=self.question_group)
        answer_group.answer.add(old_primary, old_answer_1, old_answer_2)

        user_service = UserQuestionnaireService(self.user, self.questionnaire)
        user_service.submit()

        self.assertEqual(self.initial['version']+1, user_service.answer_version())
        user_service.set_versions()
        self.assertEqual(self.initial['version']+1, user_service.POST_version)
        self.assertEqual(self.initial['version'], user_service.GET_version)

    def test_knows_unanswered_required_question_in_section(self):
        data = self.data.copy()

        old_primary = MultiChoiceAnswer.objects.create(response=self.option1, question=self.question1, **self.initial)
        old_answer_1 = NumericalAnswer.objects.create(response=int(data['Number-0-response']), question=self.question2, **self.initial)
        old_answer_2 = NumericalAnswer.objects.create(response=int(data['Number-1-response']), question=self.question3, **self.initial)

        answer_group = AnswerGroup.objects.create(grouped_question=self.question_group)
        answer_group.answer.add(old_primary, old_answer_1, old_answer_2)

        required_question = Question.objects.create(text='required', UID='C00330', answer_type='Number', is_required=True)
        self.question_group.question.add(required_question)
        QuestionGroupOrder.objects.create(question_group=self.question_group, question=required_question, order=4)

        user_service = UserQuestionnaireService(self.user, self.questionnaire)

        self.assertFalse(user_service.answered_required_questions_in(self.section_1))

    def test_should_return_invalid_section_answers_and_the_corresponding_formset(self):
        data = self.data.copy()

        old_primary = MultiChoiceAnswer.objects.create(response=self.option1, question=self.question1, **self.initial)
        old_answer_1 = NumericalAnswer.objects.create(response=int(data['Number-0-response']), question=self.question2, **self.initial)
        old_answer_2 = NumericalAnswer.objects.create(response=int(data['Number-1-response']), question=self.question3, **self.initial)

        answer_group = AnswerGroup.objects.create(grouped_question=self.question_group)
        answer_group.answer.add(old_primary, old_answer_1, old_answer_2)

        required_question = Question.objects.create(text='required', UID='C00330', answer_type='Number', is_required=True)
        self.question_group.question.add(required_question)
        QuestionGroupOrder.objects.create(question_group=self.question_group, question=required_question, order=4)

        user_service = UserQuestionnaireService(self.user, self.questionnaire)

        self.assertFalse(user_service.required_sections_answered())
        self.assertEqual(self.section_1, user_service.unanswered_section)

    def test_knows_all_sections_questionnaire_entry_services(self):
        section_2 = Section.objects.create(title="section 2", order=2, questionnaire=self.questionnaire, name="section 2")
        section_3 = Section.objects.create(title="section 3", order=3, questionnaire=self.questionnaire, name="section 3")

        user_service = UserQuestionnaireService(self.user, self.questionnaire)
        all_section_questionnaires = user_service.all_sections_questionnaires()

        self.assertEqual(3, len(all_section_questionnaires))
        self.assertIsInstance(all_section_questionnaires[self.section_1], QuestionnaireEntryFormService)
        self.assertEqual(self.section_1, all_section_questionnaires[self.section_1].section)
        self.assertIsInstance(all_section_questionnaires[section_2], QuestionnaireEntryFormService)
        self.assertEqual(section_2, all_section_questionnaires[section_2].section)
        self.assertIsInstance(all_section_questionnaires[section_3], QuestionnaireEntryFormService)
        self.assertEqual(section_3, all_section_questionnaires[section_3].section)

    def test_user_knows_if_he_should_see_preview_when_status_is_submitted(self):
        data = self.data
        old_primary = MultiChoiceAnswer.objects.create(response=self.option1, question=self.question1, **self.initial)
        old_answer_1 = NumericalAnswer.objects.create(response=int(data['Number-0-response']), question=self.question2, **self.initial)
        old_answer_2 = NumericalAnswer.objects.create(response=int(data['Number-1-response']), question=self.question3, **self.initial)

        answer_group = AnswerGroup.objects.create(grouped_question=self.question_group)
        answer_group.answer.add(old_primary, old_answer_1, old_answer_2)

        user_service = UserQuestionnaireService(self.user, self.questionnaire)

        self.assertFalse(user_service.preview())

        old_primary.status="Submitted"
        old_primary.save()
        old_answer_1.status="Submitted"
        old_answer_1.save()
        old_answer_2.status="Submitted"
        old_answer_2.save()

        self.assertTrue(user_service.preview())

