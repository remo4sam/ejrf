from django.test import Client
from questionnaire.forms.questions import QuestionForm
from questionnaire.models import Question, QuestionGroup, Questionnaire, Section, SubSection, Country, Answer
from questionnaire.tests.base_test import BaseTest


class SectionsViewTest(BaseTest):

    def setUp(self):
        self.client = Client()
        self.user, self.country, self.region = self.create_user_with_no_permissions()

        self.assign('can_edit_questionnaire', self.user)
        self.client.login(username=self.user.username, password='pass')

        self.url = '/questions/'
        self.form_data = {'text': 'How many kids were immunised this year?',
                          'instructions': 'Some instructions',
                          'export_label': 'blah',
                          'answer_type': 'Number'}

    def test_get_list_question(self):
        questions = Question.objects.create(text='B. Number of cases tested',
                                            instructions="Enter the total number of cases", UID='00001', answer_type='Number')

        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
        templates = [template.name for template in response.templates]
        self.assertIn('questions/index.html', templates)
        self.assertIn(questions, response.context['questions'])
        self.assertIsNone(response.context['active_questions'])

    def test_get_list_question_has_active_questions_from_finalized_questionnaire_in_context(self):
        questions = Question.objects.create(text='B. Number of cases tested', UID='00001', answer_type='Number')

        finalized_questionnaire = Questionnaire.objects.create(status=Questionnaire.FINALIZED, name="finalized")
        section = Section.objects.create(name="section", questionnaire=finalized_questionnaire, order=1)
        subsection = SubSection.objects.create(title="subsection 1", section=section, order=1)
        question1 = Question.objects.create(text='Q1', UID='C00003', answer_type='Number')
        question1.question_group.create(subsection=subsection)

        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
        templates = [template.name for template in response.templates]
        self.assertIn('questions/index.html', templates)
        self.assertEqual(2, len(response.context['questions']))
        self.assertIn(questions, response.context['questions'])
        self.assertIn(question1, response.context['questions'])

        self.assertEqual(1, len(response.context['active_questions']))
        self.assertIn(question1, response.context['active_questions'])

    def test_get_create_question(self):
        response = self.client.get(self.url + 'new/')
        self.assertEqual(200, response.status_code)
        templates = [template.name for template in response.templates]
        self.assertIn('questions/new.html', templates)
        self.assertIsNotNone(response.context['form'])
        self.assertEqual('CREATE', response.context['btn_label'])
        self.assertEqual("id-new-question-form", response.context['id'])

    def test_post_create_question(self):
        self.assertRaises(Question.DoesNotExist, Question.objects.get, **self.form_data)
        response = self.client.post(self.url + 'new/', data=self.form_data)
        self.assertRedirects(response, self.url)
        self.failUnless(Question.objects.get(**self.form_data))
        self.assertIn("Question successfully created.", response.cookies['messages'].value)

    def test_post_create_with_invalid_form_returns_errors(self):
        form_data = self.form_data.copy()
        form_data['text'] = ''

        self.assertRaises(Question.DoesNotExist, Question.objects.get, **form_data)
        response = self.client.post(self.url + 'new/', data=form_data)
        self.assertRaises(Question.DoesNotExist, Question.objects.get, **form_data)
        self.assertIn('Question NOT created. See errors below.', response.content)
        self.assertIsInstance(response.context['form'], QuestionForm)
        self.assertEqual("CREATE", response.context['btn_label'])
        self.assertEqual("id-new-question-form", response.context['id'])

    def test_post_multichoice_question_with_options(self):
        form_data = self.form_data.copy()
        form_data['answer_type'] = 'MultiChoice'
        question_options = ['yes, No, Maybe, Nr, Chill']
        self.assertRaises(Question.DoesNotExist, Question.objects.get, **form_data)
        form_data['options'] = question_options
        response = self.client.post(self.url + 'new/', data=form_data)
        self.assertRedirects(response, self.url)
        questions = Question.objects.filter(text=form_data['text'], instructions=form_data['instructions'],
                                            answer_type=form_data['answer_type'])
        self.assertEqual(1, len(questions))
        options = questions[0].options.all()

        self.assertEqual(5, options.count())
        [self.assertIn(option.text, question_options[0].split(',')) for option in options]

    def test_post_multichoice_question_with_options_with_form_errors(self):
        form_data = self.form_data.copy()
        form_data['answer_type'] = 'MultiChoice'
        self.assertRaises(Question.DoesNotExist, Question.objects.get, **form_data)
        form_data['options'] = []
        response = self.client.post(self.url + 'new/', data=form_data)
        self.assertRaises(Question.DoesNotExist, Question.objects.get, text=form_data['text'], instructions=form_data['instructions'], answer_type=form_data['answer_type'])
        self.assertIn('Question NOT created. See errors below.', response.content)
        self.assertIsInstance(response.context['form'], QuestionForm)
        self.assertEqual("CREATE", response.context['btn_label'])
        self.assertEqual("id-new-question-form", response.context['id'])

    def test_delete_question(self):
        data = {'text': 'B. Number of cases tested',
                'instructions': "Enter the total number of cases",
                'UID': '00001', 'answer_type': 'Number'}
        question = Question.objects.create(**data)
        response = self.client.post('/questions/%s/delete/' % question.id, {})
        self.assertRedirects(response, self.url)
        self.assertRaises(Question.DoesNotExist, Question.objects.get, **data)
        message = "Question was deleted successfully"
        self.assertIn(message, response.cookies['messages'].value)

    def test_does_not_delete_question_when_it_has_answers(self):
        data = {'text': 'B. Number of cases tested',
                'instructions': "Enter the total number of cases",
                'UID': '00001', 'answer_type': 'Number'}
        question = Question.objects.create(**data)
        country = Country.objects.create(name="Peru")
        Answer.objects.create(question=question, country=country, status="Submitted")

        response = self.client.post('/questions/%s/delete/' % question.id, {})
        self.assertRedirects(response, self.url)
        self.failUnless(Question.objects.get(**data))
        message = "Question was not deleted because it has responses"
        self.assertIn(message, response.cookies['messages'].value)