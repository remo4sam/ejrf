from django.core.urlresolvers import reverse
from django.test import Client
from questionnaire.forms.sections import SectionForm, SubSectionForm
from questionnaire.models import Questionnaire, Section, SubSection, Question, QuestionGroup, QuestionOption, MultiChoiceAnswer, NumericalAnswer, QuestionGroupOrder, AnswerGroup, Answer, Country, TextAnswer, DateAnswer
from questionnaire.services.questionnaire_entry_form_service import QuestionnaireEntryFormService
from questionnaire.tests.base_test import BaseTest


class QuestionnaireEntrySaveDraftTest(BaseTest):
    def setUp(self):
        self.questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English", status=Questionnaire.PUBLISHED,
                                                          description="From dropbox as given by Rouslan")

        self.section_1 = Section.objects.create(title="Reported Cases of Selected Vaccine Preventable Diseases (VPDs)",
                                                order=1,
                                                questionnaire=self.questionnaire, name="Reported Cases")

        self.sub_section = SubSection.objects.create(title="Reported cases for the year 2013", order=1,
                                                     section=self.section_1)

        self.question1 = Question.objects.create(text='Disease', UID='C00001', answer_type='MultiChoice', is_primary=True)
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

        self.url = '/questionnaire/entry/%d/section/%d/' % (self.questionnaire.id, self.section_1.id)

        self.client = Client()
        self.user, self.country = self.create_user_with_no_permissions()

        self.assign('can_submit_responses', self.user)
        self.client.login(username=self.user.username, password='pass')

        self.data = {u'MultiChoice-MAX_NUM_FORMS': u'1', u'MultiChoice-TOTAL_FORMS': u'1',
                u'MultiChoice-INITIAL_FORMS': u'1', u'MultiChoice-0-response': self.option1.id,
                u'Number-INITIAL_FORMS': u'2', u'Number-TOTAL_FORMS': u'2', u'Number-MAX_NUM_FORMS': u'2',
                u'Number-0-response': u'2', u'Number-1-response': u'33'}

    def test_get_questionnaire_entry_view(self):
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
        templates = [template.name for template in response.templates]
        self.assertIn('questionnaires/entry/index.html', templates)
        self.assertEqual(self.questionnaire, response.context['questionnaire'])
        self.assertEqual(self.section_1, response.context['section'])
        self.assertIsInstance(response.context['formsets'], QuestionnaireEntryFormService)

    def test_gets_ordered_sections_for_menu_breadcrumps_wizzard(self):
        section2 = Section.objects.create(title="section 2", order=2, questionnaire=self.questionnaire)
        section3 = Section.objects.create(title="section 3", order=3, questionnaire=self.questionnaire)
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
        self.assertEqual(3, response.context['ordered_sections'].count())
        self.assertEqual(self.section_1, response.context['ordered_sections'][0])
        self.assertEqual(section2, response.context['ordered_sections'][1])
        self.assertEqual(section3, response.context['ordered_sections'][2])
        self.assertEqual(False, response.context['printable'])
        self.assertEqual(False, response.context['preview'])
        self.assertEqual(False, response.context['preview'])
        self.assertIsInstance(response.context['form'], SectionForm)
        self.assertEqual(response.context['action'], '/questionnaire/entry/%s/section/new/' % self.questionnaire.id)
        self.assertIsInstance(response.context['subsection_form'], SubSectionForm)
        self.assertEqual(response.context['subsection_action'], '/questionnaire/entry/%s/section/%s/subsection/new/' %
                                                                (self.questionnaire.id, self.section_1.id))

    def test_gets_ordered_sections_for_only_the_questionnaire_in_get_params(self):
        questionnaire_2 = Questionnaire.objects.create(name="JRF 2013 Core English", status=Questionnaire.FINALIZED,
                                                       description="From dropbox as given by Rouslan")
        questionnaire_2_section = Section.objects.create(title="section 3", order=3, questionnaire=questionnaire_2)

        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
        self.assertEqual(self.section_1, response.context['ordered_sections'][0])
        self.assertNotIn(questionnaire_2_section, response.context['ordered_sections'])

    def test_gets_printable_as_true_if_set_in_request(self):
        url = '/questionnaire/entry/%d/section/%d/?printable=true&preview=1' % (self.questionnaire.id, self.section_1.id)
        response = self.client.get(url)
        self.assertEqual(True, response.context['printable'])
        self.assertEqual(True, response.context['preview'])

    def test_login_required(self):
        self.assert_login_required('/questionnaire/entry/%d/section/%d/' % (self.questionnaire.id, self.section_1.id))

    def test_permission_required(self):
        self.assert_permission_required('/questionnaire/entry/%d/section/%d/' % (self.questionnaire.id, self.section_1.id))

    def test_post_saves_answers(self):
        data = self.data
        self.failIf(MultiChoiceAnswer.objects.filter(response__id=int(data['MultiChoice-0-response'])))
        self.failIf(NumericalAnswer.objects.filter(response=int(data['Number-0-response'])))
        self.failIf(NumericalAnswer.objects.filter(response=int(data['Number-1-response'])))

        response = self.client.post(self.url, data=data)
        self.assertEqual(200, response.status_code)
        templates = [template.name for template in response.templates]
        self.assertIn('questionnaires/entry/index.html', templates)

        self.failUnless(MultiChoiceAnswer.objects.filter(response__id=int(data['MultiChoice-0-response']), question=self.question1))
        self.failUnless(NumericalAnswer.objects.filter(response=int(data['Number-0-response']), question=self.question2))
        self.failUnless(NumericalAnswer.objects.filter(response=int(data['Number-1-response']), question=self.question3))

    def test_post_groups_rows_into_answer_groups(self):
        data = self.data
        self.failIf(MultiChoiceAnswer.objects.filter(response__id=int(data['MultiChoice-0-response'])))
        self.failIf(NumericalAnswer.objects.filter(response=int(data['Number-0-response'])))
        self.failIf(NumericalAnswer.objects.filter(response=int(data['Number-1-response'])))

        response = self.client.post(self.url, data=data)
        self.assertEqual(200, response.status_code)

        primary = MultiChoiceAnswer.objects.get(response__id=int(data['MultiChoice-0-response']), question=self.question1)
        answer_1 = NumericalAnswer.objects.get(response=int(data['Number-0-response']), question=self.question2)
        answer_2 = NumericalAnswer.objects.get(response=int(data['Number-1-response']), question=self.question3)

        answer_group = AnswerGroup.objects.filter(grouped_question=self.question_group)
        self.assertEqual(1, answer_group.count())
        answer_group_answers = answer_group[0].answer.all().select_subclasses()
        self.assertEqual(3, answer_group_answers.count())
        self.assertIn(primary, answer_group_answers)
        self.assertIn(answer_1, answer_group_answers)
        self.assertIn(answer_2, answer_group_answers)

    def test_successful_post_shows_success_message(self):
        data = self.data
        self.failIf(MultiChoiceAnswer.objects.filter(response__id=int(data['MultiChoice-0-response'])))
        self.failIf(NumericalAnswer.objects.filter(response=int(data['Number-0-response'])))
        self.failIf(NumericalAnswer.objects.filter(response=int(data['Number-1-response'])))

        response = self.client.post(self.url, data=data)
        self.assertEqual(200, response.status_code)
        expected_message = 'Draft saved.'
        self.assertIn(expected_message, response.content)

    def test_post_failure_does_not_save_answers_and_does_not_redirect(self):
        data = self.data
        data[u'MultiChoice-0-response'] = -1

        self.failIf(MultiChoiceAnswer.objects.filter(response__id=int(data['MultiChoice-0-response'])))
        self.failIf(NumericalAnswer.objects.filter(response=int(data['Number-0-response'])))
        self.failIf(NumericalAnswer.objects.filter(response=int(data['Number-1-response'])))

        response = self.client.post(self.url, data=data)
        self.assertEqual(200, response.status_code)
        templates = [template.name for template in response.templates]
        self.assertIn('questionnaires/entry/index.html', templates)

        self.failIf(MultiChoiceAnswer.objects.filter(response__id=int(data['MultiChoice-0-response'])))
        self.failIf(NumericalAnswer.objects.filter(response=int(data['Number-0-response'])))
        self.failIf(NumericalAnswer.objects.filter(response=int(data['Number-1-response'])))

        self.failIf(AnswerGroup.objects.filter(grouped_question=self.question_group))

        expected_message = 'Draft NOT saved. See errors below.'
        self.assertIn(expected_message, response.content)

    def test_post_on_section_with_draft_answers_modify_original_draft_answers_and_not_create_new_instance(self):
        data = self.data
        self.client.post(self.url, data=data)

        old_primary = MultiChoiceAnswer.objects.get(response__id=int(data['MultiChoice-0-response']), question=self.question1)
        old_answer_1 = NumericalAnswer.objects.get(response=int(data['Number-0-response']), question=self.question2)
        old_answer_2 = NumericalAnswer.objects.get(response=int(data['Number-1-response']), question=self.question3)

        data_modified = data.copy()
        data_modified['MultiChoice-0-response'] = self.option2.id
        data_modified['Number-1-response'] = '3'
        response = self.client.post(self.url, data=data_modified)
        self.assertEqual(200, response.status_code)

        primary = MultiChoiceAnswer.objects.get(response__id=int(data_modified['MultiChoice-0-response']), question=self.question1, version=0)
        answer_1 = NumericalAnswer.objects.get(response=int(data_modified['Number-0-response']), question=self.question2, version=0)
        answer_2 = NumericalAnswer.objects.get(response=int(data_modified['Number-1-response']), question=self.question3, version=0)

        self.assertEqual(old_primary.id, primary.id)
        self.assertEqual(old_answer_1.id, answer_1.id)
        self.assertEqual(old_answer_2.id, answer_2.id)

        answer_group = AnswerGroup.objects.filter(grouped_question=self.question_group)
        self.assertEqual(1, answer_group.count())

    def test_post_after_submit_save_new_draft_version(self):
        data = self.data.copy()
        self.client.post(self.url, data=data)

        self.client.post('/submit/')

        old_primary = MultiChoiceAnswer.objects.get(response__id=int(data['MultiChoice-0-response']), question=self.question1, version=0)
        old_answer_1 = NumericalAnswer.objects.get(response=int(data['Number-0-response']), question=self.question2, version=0)
        old_answer_2 = NumericalAnswer.objects.get(response=int(data['Number-1-response']), question=self.question3, version=0)

        self.assertEqual(Answer.SUBMITTED_STATUS, old_primary.status)
        self.assertEqual(Answer.SUBMITTED_STATUS, old_answer_1.status)
        self.assertEqual(Answer.SUBMITTED_STATUS, old_answer_2.status)

        answer_group = AnswerGroup.objects.filter(grouped_question=self.question_group)
        self.assertEqual(1, answer_group.count())

        data = self.data
        self.client.post(self.url, data=data)

        primary = MultiChoiceAnswer.objects.filter(response__id=int(data['MultiChoice-0-response']), question=self.question1, version=1)
        answer_1 = NumericalAnswer.objects.filter(response=int(data['Number-0-response']), question=self.question2, version=1)
        answer_2 = NumericalAnswer.objects.filter(response=int(data['Number-1-response']), question=self.question3, version=1)

        self.assertEqual(1, primary.count())
        self.assertEqual(Answer.DRAFT_STATUS, primary[0].status)
        self.assertEqual(1, primary[0].version)

        self.assertEqual(1, answer_1.count())
        self.assertEqual(Answer.DRAFT_STATUS, answer_1[0].status)
        self.assertEqual(1, answer_1[0].version)

        self.assertEqual(1, answer_2.count())
        self.assertEqual(Answer.DRAFT_STATUS, answer_2[0].status)
        self.assertEqual(1, answer_2[0].version)

    def test_post_saves_answers_and_redirect_to_no_preview_if_given_redirect_url(self):
        data = self.data
        self.failIf(MultiChoiceAnswer.objects.filter(response__id=int(data['MultiChoice-0-response'])))
        self.failIf(NumericalAnswer.objects.filter(response=int(data['Number-0-response'])))
        self.failIf(NumericalAnswer.objects.filter(response=int(data['Number-1-response'])))

        section_2 = Section.objects.create(name="haha", questionnaire=self.questionnaire, order=2)
        data['redirect_url'] = '/questionnaire/entry/%d/section/%d/' % (self.questionnaire.id, section_2.id)

        response = self.client.post(self.url + "?preview=1", data=data)

        self.failUnless(MultiChoiceAnswer.objects.filter(response__id=int(data['MultiChoice-0-response']), question=self.question1))
        self.failUnless(NumericalAnswer.objects.filter(response=int(data['Number-0-response']), question=self.question2))
        self.failUnless(NumericalAnswer.objects.filter(response=int(data['Number-1-response']), question=self.question3))

        self.assertRedirects(response, data['redirect_url'])


class SaveGridDraftQuestionGroupEntryTest(BaseTest):

    def setUp(self):
        self.questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English")

        self.section1 = Section.objects.create(title="Reported Cases of Selected Vaccine", order=1,
                                               questionnaire=self.questionnaire, name="Reported Cases")

        self.sub_section = SubSection.objects.create(title="subsection 1", order=1, section=self.section1)
        self.sub_section2 = SubSection.objects.create(title="subsection 2", order=2, section=self.section1)

        self.question_group = QuestionGroup.objects.create(subsection=self.sub_section, order=1, grid=True, display_all=True)

        self.question1 = Question.objects.create(text='Favorite beer 1', UID='C00001', answer_type='MultiChoice', is_primary=True)
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
        self.initial = {'country': self.country, 'status': 'Draft', 'version': 1, 'code': 'ABC123'}
        self.data = {u'MultiChoice-MAX_NUM_FORMS': u'3', u'MultiChoice-TOTAL_FORMS': u'3',
                     u'MultiChoice-INITIAL_FORMS': u'3', u'MultiChoice-0-response': self.option1.id,
                     u'MultiChoice-1-response': self.option2.id,  u'MultiChoice-2-response': self.option3.id,
                     u'Number-MAX_NUM_FORMS': u'3', u'Number-TOTAL_FORMS': u'3',
                     u'Number-INITIAL_FORMS': u'3', u'Number-0-response': '22',
                     u'Number-1-response': '44',  u'Number-2-response': '33',
                     u'Text-MAX_NUM_FORMS': u'3', u'Text-TOTAL_FORMS': u'3',
                     u'Text-INITIAL_FORMS': u'3', u'Text-0-response': 'Haha',
                     u'Text-1-response': 'Hehe',  u'Text-2-response': 'hehehe',
                     u'Date-MAX_NUM_FORMS': u'3', u'Date-TOTAL_FORMS': u'3',
                     u'Date-INITIAL_FORMS': u'3', u'Date-0-response': '2014-2-2',
                     u'Date-1-response': '2014-2-2',  u'Date-2-response': '2014-2-2',
                     }
        self.url = '/questionnaire/entry/%d/section/%d/' % (self.questionnaire.id, self.section1.id)
        self.client = Client()
        self.user, self.country = self.create_user_with_no_permissions()

        self.assign('can_submit_responses', self.user)
        self.client.login(username=self.user.username, password='pass')

    def test_post_grid_view_saves_drafts(self):
        data = self.data
        self.failIf(MultiChoiceAnswer.objects.filter(response__id=int(data['MultiChoice-0-response']), question=self.question1))
        self.failIf(MultiChoiceAnswer.objects.filter(response__id=int(data['MultiChoice-1-response']), question=self.question1))
        self.failIf(MultiChoiceAnswer.objects.filter(response__id=int(data['MultiChoice-2-response']), question=self.question1))

        self.failIf(NumericalAnswer.objects.filter(response=int(data['Number-0-response']), question=self.question3))
        self.failIf(NumericalAnswer.objects.filter(response=int(data['Number-1-response']), question=self.question3))
        self.failIf(NumericalAnswer.objects.filter(response=int(data['Number-2-response']), question=self.question3))

        self.failIf(TextAnswer.objects.filter(response=data['Text-0-response'], question=self.question2))
        self.failIf(TextAnswer.objects.filter(response=data['Text-1-response'], question=self.question2))
        self.failIf(TextAnswer.objects.filter(response=data['Text-2-response'], question=self.question2))

        self.failIf(DateAnswer.objects.filter(response=data['Date-0-response'], question=self.question4))
        self.failIf(DateAnswer.objects.filter(response=data['Date-1-response'], question=self.question4))
        self.failIf(DateAnswer.objects.filter(response=data['Date-2-response'], question=self.question4))

        response = self.client.post(self.url, data=data)

        self.failUnless(MultiChoiceAnswer.objects.filter(response__id=int(data['MultiChoice-0-response']), question=self.question1))
        self.failUnless(MultiChoiceAnswer.objects.filter(response__id=int(data['MultiChoice-1-response']), question=self.question1))
        self.failUnless(MultiChoiceAnswer.objects.filter(response__id=int(data['MultiChoice-2-response']), question=self.question1))

        self.failUnless(NumericalAnswer.objects.filter(response=int(data['Number-0-response']), question=self.question3))
        self.failUnless(NumericalAnswer.objects.filter(response=int(data['Number-1-response']), question=self.question3))
        self.failUnless(NumericalAnswer.objects.filter(response=int(data['Number-2-response']), question=self.question3))

        self.failUnless(TextAnswer.objects.filter(response=data['Text-0-response'], question=self.question2))
        self.failUnless(TextAnswer.objects.filter(response=data['Text-1-response'], question=self.question2))
        self.failUnless(TextAnswer.objects.filter(response=data['Text-2-response'], question=self.question2))

        self.failUnless(DateAnswer.objects.filter(response=data['Date-0-response'], question=self.question4))
        self.failUnless(DateAnswer.objects.filter(response=data['Date-1-response'], question=self.question4))
        self.failUnless(DateAnswer.objects.filter(response=data['Date-2-response'], question=self.question4))

        self.assertEqual(200, response.status_code)
        expected_message = 'Draft saved.'
        self.assertIn(expected_message, response.content)


class QuestionnaireEntrySubmitTest(BaseTest):
    def setUp(self):
        self.questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English", status=Questionnaire.PUBLISHED,
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

        self.url = '/submit/'

        self.client = Client()
        self.user, self.country = self.create_user_with_no_permissions()

        self.assign('can_submit_responses', self.user)
        self.client.login(username=self.user.username, password='pass')

        self.data = {u'MultiChoice-MAX_NUM_FORMS': u'1', u'MultiChoice-TOTAL_FORMS': u'1',
                u'MultiChoice-INITIAL_FORMS': u'1', u'MultiChoice-0-response': self.option1.id,
                u'Number-INITIAL_FORMS': u'2', u'Number-TOTAL_FORMS': u'2', u'Number-MAX_NUM_FORMS': u'2',
                u'Number-0-response': u'2', u'Number-1-response': u'33'}

    def test_login_required(self):
        self.assert_login_required(self.url)

    def test_submit_changes_all_answers_statuses_to_submitted(self):
        other_section_1 = Section.objects.create(title="Reported Cases of Selected Vaccine Preventable Diseases (VPDs)",
                                                 order=2, questionnaire=self.questionnaire, name="Reported Cases")
        other_sub_section = SubSection.objects.create(title="Reported cases for the year 2013", order=1,
                                                      section=other_section_1)
        other_question1 = Question.objects.create(text='other question 1', UID='C00011', answer_type='Number')
        other_question2 = Question.objects.create(text='other question 2', UID='C00012', answer_type='Number')

        other_question_group = QuestionGroup.objects.create(subsection=other_sub_section, order=1)
        other_question_group.question.add(other_question1, other_question2)

        QuestionGroupOrder.objects.create(question=other_question1, order=1, question_group=other_question_group)
        QuestionGroupOrder.objects.create(question=other_question2, order=2, question_group=other_question_group)

        other_answer_1 = NumericalAnswer.objects.create(response=1, question=other_question1, status=Answer.DRAFT_STATUS, country=self.country, version=0)
        other_answer_2 = NumericalAnswer.objects.create(response=2, question=other_question2, status=Answer.DRAFT_STATUS, country=self.country, version=0)

        answer_group = AnswerGroup.objects.create(grouped_question=other_question_group)
        answer_group.answer.add(other_answer_1, other_answer_2)

        self.client.post(self.url)

        other_answer_1 = NumericalAnswer.objects.get(response=1, question=other_question1, country=self.country, version=0)
        other_answer_2 = NumericalAnswer.objects.get(response=2, question=other_question2, country=self.country, version=0)

        self.assertEqual(Answer.SUBMITTED_STATUS, other_answer_1.status)
        self.assertEqual(Answer.SUBMITTED_STATUS, other_answer_2.status)

        answer_group = AnswerGroup.objects.filter(grouped_question=other_question_group)
        self.assertEqual(1, answer_group.count())

    def test_submit_on_success_redirect_to_referer_if_given(self):
        referer_url = '/questionnaire/entry/%d/section/%d/' % (self.questionnaire.id, self.section_1.id)
        meta ={'HTTP_REFERER': referer_url}
        response = self.client.post(self.url, **meta)
        self.assertRedirects(response, referer_url + "?preview=1")

    def test_submit_on_success_redirect_to_referer__does_not_highlight_errors_and_shows_preview(self):
        referer_url = '/questionnaire/entry/%d/section/%d/?show=errors' % (self.questionnaire.id, self.section_1.id)
        referer_url_no_error_yes_preview= '/questionnaire/entry/%d/section/%d/?preview=1' % (self.questionnaire.id, self.section_1.id)
        meta = {'HTTP_REFERER': referer_url}
        response = self.client.post(self.url, **meta)
        self.assertRedirects(response, referer_url_no_error_yes_preview)

    def test_submit_on_success_redirect_to_homepage_if_referer_not_given(self):
        response = self.client.post(self.url)
        self.assertRedirects(response, '/?preview=1', target_status_code=302)

    def test_submit_success_message(self):
        response = self.client.post(self.url)
        success_message = 'Questionnaire Submitted.'
        self.assertIn(success_message, response.cookies['messages'].value)

    def test_submit_fails_and_shows_sections_with_error_message_and_error_fields_when_a_section_has_unanswered_required_questions(self):
        data = self.data.copy()
        initial = {'country': self.country, 'status': 'Draft', 'version':1, 'code': 'ABC123'}
        old_primary = MultiChoiceAnswer.objects.create(response=self.option1, question=self.question1, **initial)
        old_answer_1 = NumericalAnswer.objects.create(response=int(data['Number-0-response']), question=self.question2, **initial)
        old_answer_2 = NumericalAnswer.objects.create(response=int(data['Number-1-response']), question=self.question3, **initial)

        answer_group = AnswerGroup.objects.create(grouped_question=self.question_group)
        answer_group.answer.add(old_primary, old_answer_1, old_answer_2)

        required_question = Question.objects.create(text='required', UID='C00330', answer_type='Number', is_required=True)
        self.question_group.question.add(required_question)
        QuestionGroupOrder.objects.create(question_group=self.question_group, question=required_question, order=4)

        response = self.client.post(self.url)
        section_with_errrors_url = '/questionnaire/entry/%d/section/%d/?show=errors' % (self.questionnaire.id, self.section_1.id)

        self.assertRedirects(response, section_with_errrors_url)
        error_message = 'Questionnaire NOT submitted. See errors below.'
        self.assertIn(error_message, response.cookies['messages'].value)

        submitted_attributes = initial.copy()
        submitted_attributes['status'] = 'Submitted'

        primary = MultiChoiceAnswer.objects.filter(response=self.option1, question=self.question1, **submitted_attributes)
        answer_1 = NumericalAnswer.objects.filter(response=int(data['Number-0-response']), question=self.question2, **submitted_attributes)
        answer_2 = NumericalAnswer.objects.filter(response=int(data['Number-1-response']), question=self.question3, **submitted_attributes)

        self.failIf(primary)
        self.failIf(answer_1)
        self.failIf(answer_2)


class QuestionnaireCloneViewTest(BaseTest):
    def setUp(self):
        self.questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English", status=Questionnaire.FINALIZED, year=2013)
        self.section_1 = Section.objects.create(title="Reported Cases of Selected Vaccine Preventable Diseases (VPDs)", order=1,
                                                      questionnaire=self.questionnaire, name="Reported Cases")
        self.section_2 = Section.objects.create(title="Cured Cases of Measles", order=1,
                                                questionnaire=self.questionnaire, name="Cured Cases")

        self.sub_section1 = SubSection.objects.create(title="Reported cases for the year 2013", order=1, section=self.section_1)
        self.sub_section2 = SubSection.objects.create(title="Reported cases for the year", order=2, section=self.section_1)
        self.sub_section3 = SubSection.objects.create(title="Reported cures 2014", order=1, section=self.section_2)
        self.sub_section4 = SubSection.objects.create(title="Reported cures", order=2, section=self.section_2)
        self.primary_question = Question.objects.create(text='Disease', UID='C00003', answer_type='MultiChoice',
                                                        is_primary=True)
        self.option = QuestionOption.objects.create(text="Measles", question=self.primary_question, UID="QO1")
        self.option2 = QuestionOption.objects.create(text="TB", question=self.primary_question, UID="QO2")

        self.question1 = Question.objects.create(text='B. Number of cases tested', UID='C00004', answer_type='Number')

        self.question2 = Question.objects.create(text='C. Number of cases positive',
                                                 instructions="""
                                                 Include only those cases found positive for the infectious agent.
                                                 """,
                                                 UID='C00005', answer_type='Number')
        self.parent10 = QuestionGroup.objects.create(subsection=self.sub_section1, order=1)
        self.parent12 = QuestionGroup.objects.create(subsection=self.sub_section1, order=2)
        self.question3 = Question.objects.create(text='B. Number of cases tested', UID=Question.next_uid(), answer_type='Number')
        self.question4 = Question.objects.create(text='C. Number of cases positive', UID=Question.next_uid(), answer_type='Number')
        QuestionGroupOrder.objects.create(order=1, question_group=self.parent10, question=self.primary_question)
        QuestionGroupOrder.objects.create(order=2, question_group=self.parent10, question=self.question1)
        QuestionGroupOrder.objects.create(order=3, question_group=self.parent10, question=self.question2)
        QuestionGroupOrder.objects.create(order=4, question_group=self.parent12, question=self.question3)
        QuestionGroupOrder.objects.create(order=5, question_group=self.parent12, question=self.question4)
        self.parent10.question.add(self.question3, self.question4, self.question2, self.question1, self.primary_question)
        self.client = Client()
        self.user, self.country = self.create_user_with_no_permissions()

        self.assign('can_edit_questionnaire', self.user)
        self.client.login(username=self.user.username, password='pass')

    def test_post_clone_questionnaire(self):
        form_data = {
            'questionnaire': self.questionnaire.id,
            'year': 2014,
            'name': 'New name'
        }
        self.assertEqual(1, Questionnaire.objects.all().count())
        self.assertEqual(2, Section.objects.all().count())
        self.assertEqual(4, SubSection.objects.all().count())
        self.assertEqual(2, QuestionGroup.objects.all().count())
        self.assertEqual(5, Question.objects.all().count())

        response = self.client.post('/questionnaire/entry/duplicate/', data=form_data)
        self.assertEqual(2, Questionnaire.objects.all().count())
        self.assertEqual(4, Section.objects.all().count())
        self.assertEqual(8, SubSection.objects.all().count())
        self.assertEqual(4, QuestionGroup.objects.all().count())
        self.assertEqual(5, Question.objects.all().count())
        questionnaire = Questionnaire.objects.all().exclude(id=self.questionnaire.id)[0]
        section = questionnaire.sections.all()[0]
        url = '/questionnaire/entry/%d/section/%d/' % (questionnaire.id, section.id)
        self.assertRedirects(response, url)
        messages = "The questionnaire has been duplicated successfully, You can now go ahead and edit it"
        self.assertIn(messages, response.cookies['messages'].value)

    def test_post_clone_questionnaire_with_invalid_form(self):
        form_data = {
            'questionnaire': self.questionnaire.id,
            'year': 2030
        }
        self.assertEqual(1, Questionnaire.objects.all().count())
        self.assertEqual(2, Section.objects.all().count())
        self.assertEqual(4, SubSection.objects.all().count())
        self.assertEqual(2, QuestionGroup.objects.all().count())
        self.assertEqual(5, Question.objects.all().count())

        response = self.client.post('/questionnaire/entry/duplicate/', data=form_data)
        self.assertEqual(1, Questionnaire.objects.all().count())
        self.assertEqual(2, Section.objects.all().count())
        self.assertEqual(4, SubSection.objects.all().count())
        self.assertEqual(2, QuestionGroup.objects.all().count())
        self.assertEqual(5, Question.objects.all().count())
        url = '/manage/'
        self.assertRedirects(response, url)
        messages = "Questionnaire could not be duplicated see errors below"
        self.assertIn(messages, response.cookies['messages'].value)
