import os
from django.core.files import File
from django.test import Client
from mock import mock_open, patch
from questionnaire.models import Questionnaire, Section, SubSection, Question, QuestionGroup, QuestionOption, QuestionGroupOrder, NumericalAnswer, MultiChoiceAnswer, AnswerGroup, \
    SupportDocument
from questionnaire.services.questionnaire_entry_form_service import QuestionnaireEntryFormService
from questionnaire.tests.base_test import BaseTest


class QuestionnairePreviewTest(BaseTest):
    def setUp(self):
        self.user, self.country, self.region = self.create_user_with_no_permissions()
        self.questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English", status=Questionnaire.PUBLISHED,
                                                          description="From dropbox as given by Rouslan", region=self.region)

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

        self.url = '/questionnaire/%s/preview/' % self.questionnaire.id

        self.client = Client()

        self.assign('can_submit_responses', self.user)
        self.client.login(username=self.user.username, password='pass')

        self.data = {u'MultiChoice-MAX_NUM_FORMS': u'1', u'MultiChoice-TOTAL_FORMS': u'1',
                u'MultiChoice-INITIAL_FORMS': u'1', u'MultiChoice-0-response': self.option1.id,
                u'Number-INITIAL_FORMS': u'2', u'Number-TOTAL_FORMS': u'2', u'Number-MAX_NUM_FORMS': u'2',
                u'Number-0-response': u'2', u'Number-1-response': u'33'}

        m = mock_open()
        self.filename="haha.pdf"
        with patch('__main__.open', m, create=True):
            with open(self.filename, 'w') as document:
                document.write("Some stuff")
            self.document = open(self.filename, 'rb')

    def test_get_questionnaire_preview(self):
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
        templates = [template.name for template in response.templates]
        self.assertIn('questionnaires/entry/preview.html', templates)

    def test_gets_ordered_sections_for_menu_breadcrumps_wizzard_for_published_questionnaire(self):
        section2 = Section.objects.create(title="section 2", order=2, questionnaire=self.questionnaire)
        section3 = Section.objects.create(title="section 3", order=3, questionnaire=self.questionnaire)
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
        self.assertEqual(3, response.context['ordered_sections'].count())
        self.assertEqual(self.section_1, response.context['ordered_sections'][0])
        self.assertEqual(section2, response.context['ordered_sections'][1])
        self.assertEqual(section3, response.context['ordered_sections'][2])
        self.assertEqual(self.questionnaire, response.context['questionnaire'])

    def test_upload_view_has_all_documents_for_questionnaire(self):
        document_in = SupportDocument.objects.create(path=File(self.document), country=self.country,
                                                   questionnaire=self.questionnaire)
        questionnaire_2 = Questionnaire.objects.create(name="haha", year=2013)
        document_not_in = SupportDocument.objects.create(path=File(self.document), country=self.country,
                                                   questionnaire=questionnaire_2)

        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
        documents = response.context['documents']
        self.assertEqual(1, documents.count())
        self.assertIn(document_in, documents)
        self.assertNotIn(document_not_in, documents)
        os.system("rm -rf %s" % self.filename)

    def test_gets_all_section_forms(self):
        section_2 = Section.objects.create(title="section 2", order=2, questionnaire=self.questionnaire, name="section 2")
        section_3 = Section.objects.create(title="section 3", order=3, questionnaire=self.questionnaire, name="section 3")

        response = self.client.get(self.url)
        all_section_questionnaires = response.context['all_sections_questionnaires']

        self.assertEqual(3, len(all_section_questionnaires))
        self.assertIsInstance(all_section_questionnaires[self.section_1], QuestionnaireEntryFormService)
        self.assertEqual(self.section_1, all_section_questionnaires[self.section_1].section)
        self.assertIsInstance(all_section_questionnaires[section_2], QuestionnaireEntryFormService)
        self.assertEqual(section_2, all_section_questionnaires[section_2].section)
        self.assertIsInstance(all_section_questionnaires[section_3], QuestionnaireEntryFormService)
        self.assertEqual(section_3, all_section_questionnaires[section_3].section)

    def test_login_required(self):
        self.assert_login_required('/questionnaire/%s/preview/' % self.questionnaire.id)

    def test_permission_required(self):
        self.assert_permission_required('/questionnaire/%s/preview/' % self.questionnaire.id)

    def test_gets_ordered_sections_for_menu_breadcrumps_wizzard_for_specified_questionnaire(self):
        questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English copy", status=Questionnaire.DRAFT, region=self.region)
        section2 = Section.objects.create(title="section 2", order=2, questionnaire=questionnaire)
        section3 = Section.objects.create(title="section 3", order=3, questionnaire=questionnaire)
        url = '/questionnaire/%s/preview/' % questionnaire.id
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)
        self.assertEqual(2, response.context['ordered_sections'].count())
        self.assertNotIn(self.section_1, response.context['ordered_sections'])
        self.assertEqual(section2, response.context['ordered_sections'][0])
        self.assertEqual(section3, response.context['ordered_sections'][1])

    def test_get_preview_for_version(self):
        version = 1

        url = '/questionnaire/%s/preview/?country=%s&version=%s' % (self.questionnaire.id, self.country.id, version)
        section_2 = Section.objects.create(title="section 2", order=2, questionnaire=self.questionnaire, name="section 2")
        section_3 = Section.objects.create(title="section 3", order=3, questionnaire=self.questionnaire, name="section 3")

        self.initial = {'country': self.country, 'status': 'Draft', 'version': 1, 'code': 'ABC123', 'questionnaire': self.questionnaire}

        version_1_primary_answer = MultiChoiceAnswer.objects.create(response=self.option1, question=self.question1, **self.initial)
        version_1_answer_1 = NumericalAnswer.objects.create(response=4, question=self.question2, **self.initial)
        version_1_answer_2 = NumericalAnswer.objects.create(response=2, question=self.question3, **self.initial)

        answer_group = AnswerGroup.objects.create(grouped_question=self.question_group)
        answer_group.answer.add(version_1_answer_1, version_1_answer_2, version_1_primary_answer)

        response = self.client.get(url)
        all_section_questionnaires = response.context['all_sections_questionnaires']

        self.assertEqual(3, len(all_section_questionnaires))
        self.assertIsInstance(all_section_questionnaires[self.section_1], QuestionnaireEntryFormService)
        self.assertEqual(self.section_1, all_section_questionnaires[self.section_1].section)
        self.assertIsInstance(all_section_questionnaires[section_2], QuestionnaireEntryFormService)
        self.assertEqual(section_2, all_section_questionnaires[section_2].section)
        self.assertIsInstance(all_section_questionnaires[section_3], QuestionnaireEntryFormService)
        self.assertEqual(section_3, all_section_questionnaires[section_3].section)
        section1_formsets =  all_section_questionnaires[self.section_1]._formsets()

        self.assertEqual(self.question1, section1_formsets['MultiChoice'][0].initial['question'])
        self.assertEqual(self.question2, section1_formsets['Number'][0].initial['question'])
        self.assertEqual(self.question3, section1_formsets['Number'][1].initial['question'])

        self.assertEqual(version_1_primary_answer.response, section1_formsets['MultiChoice'][0].initial['response'])
        self.assertEqual(version_1_answer_1.response, section1_formsets['Number'][0].initial['response'])
        self.assertEqual(version_1_answer_2.response, section1_formsets['Number'][1].initial['response'])

        self.assertEqual(version_1_answer_1, section1_formsets['Number'][0].initial['answer'])
        self.assertEqual(version_1_answer_2, section1_formsets['Number'][1].initial['answer'])
        self.assertEqual(version_1_primary_answer, section1_formsets['MultiChoice'][0].initial['answer'])

        self.assertIn('answer', section1_formsets['MultiChoice'][0].initial.keys())
        self.assertIn('answer', section1_formsets['Number'][0].initial.keys())
        self.assertIn('answer', section1_formsets['Number'][1].initial.keys())