from urllib import quote
from django.core.urlresolvers import reverse
from django.test import Client
from questionnaire.forms.questions import QuestionForm
from questionnaire.models import Question, Questionnaire, Section, SubSection, Country, Answer, Region, QuestionGroup, \
    Theme, QuestionOption
from questionnaire.tests.base_test import BaseTest


class QuestionViewTest(BaseTest):

    def setUp(self):
        self.client = Client()
        self.user, self.country, self.region = self.create_user_with_no_permissions(region_name=None)

        self.assign('can_edit_questionnaire', self.user)
        self.client.login(username=self.user.username, password='pass')

        self.url = '/questions/'
        self.theme = Theme.objects.create(name="Another theme")
        self.form_data = {'text': 'How many kids were immunised this year?',
                          'instructions': 'Some instructions',
                          'answer_type': 'Number',
                          'export_label': 'Some export text',
                          'options': ['', ],
                          'theme': self.theme.id}

    def test_get_list_question(self):
        questions = Question.objects.create(text='B. Number of cases tested',
                                            instructions="Enter the total number of cases", UID='00001',
                                            answer_type='Number')

        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
        templates = [template.name for template in response.templates]
        self.assertIn('questions/index.html', templates)
        self.assertIn(questions, response.context['questions'])
        self.assertIsNone(response.context['active_questions'])

    def test_get_list_returns_questions_that_do_not_belong_regions_if_user_is_global_admin(self):
        user = self.assign('can_view_users', self.user)
        region = Region.objects.create(name="some region")
        question1 = Question.objects.create(text='question 1', UID='00001', answer_type='Number', region=region)
        question2 = Question.objects.create(text='question 2', UID='00002', answer_type='Number')
        question3 = Question.objects.create(text='question 3', UID='00003', answer_type='Number')
        self.client.logout()

        client = Client()
        client.login(username=user.username, password="pass")

        response = client.get(self.url)
        self.assertEqual(200, response.status_code)
        templates = [template.name for template in response.templates]
        self.assertIn('questions/index.html', templates)
        self.assertNotIn(question1, response.context['questions'])
        self.assertIn(question2, response.context['questions'])
        self.assertIn(question3, response.context['questions'])

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

    def test_get_list_questions_and_active_questions_do_not_contain_parent_questions(self):
        parent_question = Question.objects.create(text='parent q', UID='00001', answer_type='Number')
        questions = Question.objects.create(text='child q', UID='00001', answer_type='Number', parent=parent_question)

        finalized_questionnaire = Questionnaire.objects.create(status=Questionnaire.FINALIZED, name="finalized")
        section = Section.objects.create(name="section", questionnaire=finalized_questionnaire, order=1)
        subsection = SubSection.objects.create(title="subsection 1", section=section, order=1)
        question1 = Question.objects.create(text='Q1', UID='C00003', answer_type='Number', parent=parent_question)
        question1.question_group.create(subsection=subsection)

        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
        templates = [template.name for template in response.templates]
        self.assertIn('questions/index.html', templates)
        self.assertEqual(2, len(response.context['questions']))
        self.assertIn(questions, response.context['questions'])
        self.assertIn(question1, response.context['questions'])
        self.assertNotIn(parent_question, response.context['questions'])

        self.assertEqual(1, len(response.context['active_questions']))
        self.assertIn(question1, response.context['active_questions'])
        self.assertNotIn(parent_question, response.context['active_questions'])

    def test_get_create_question(self):
        response = self.client.get(self.url + 'new/')
        self.assertEqual(200, response.status_code)
        templates = [template.name for template in response.templates]
        self.assertIn('questions/new.html', templates)
        self.assertIsNotNone(response.context['form'])
        self.assertEqual('CREATE', response.context['btn_label'])
        self.assertEqual("id-new-question-form", response.context['id'])
        self.assertEqual(reverse('list_questions_page'), response.context['cancel_url'])
        self.assertEqual('New Question', response.context['title'])

    def test_post_create_question(self):
        data = self.form_data.copy()
        del data['options']
        self.assertRaises(Question.DoesNotExist, Question.objects.get, **data)
        response = self.client.post(self.url + 'new/', data=self.form_data)
        self.assertRedirects(response, self.url)
        self.failUnless(Question.objects.get(**data))
        self.assertIn("Question successfully created.", response.cookies['messages'].value)

    def test_post_create_with_invalid_form_returns_errors(self):
        form_data = self.form_data.copy()
        form_data['text'] = ''
        del form_data['options']

        self.assertRaises(Question.DoesNotExist, Question.objects.get, **form_data)
        response = self.client.post(self.url + 'new/', data=form_data)
        self.assertRaises(Question.DoesNotExist, Question.objects.get, **form_data)
        self.assertIn('Question NOT created. See errors below.', response.content)
        self.assertIsInstance(response.context['form'], QuestionForm)
        self.assertEqual("CREATE", response.context['btn_label'])
        self.assertEqual(reverse('list_questions_page'), response.context['cancel_url'])
        self.assertEqual("id-new-question-form", response.context['id'])
        self.assertEqual('New Question', response.context['title'])

    def test_post_multichoice_question_with_options(self):
        form_data = self.form_data.copy()
        form_data['answer_type'] = 'MultiChoice'
        question_options = ['yes, No, Maybe, Nr, Chill']
        del form_data['options']
        self.assertRaises(Question.DoesNotExist, Question.objects.get, **form_data)

        form_data.update({'options': question_options})

        response = self.client.post(self.url + 'new/', data=form_data)
        self.assertRedirects(response, self.url)
        questions = Question.objects.filter(text=form_data['text'], instructions=form_data['instructions'],
                                            answer_type=form_data['answer_type'])
        self.assertEqual(1, len(questions))
        options = questions[0].options.all()

        self.assertEqual(5, options.count())
        [self.assertIn(option.text, ['yes', 'No', 'Maybe', 'Nr', 'Chill']) for option in options]

    def test_post_multichoice_question_with_options_with_form_errors(self):
        form_data = self.form_data.copy()
        form_data['answer_type'] = 'MultiChoice'
        del form_data['options']

        self.assertRaises(Question.DoesNotExist, Question.objects.get, **form_data)
        form_data.update({'options': []})

        response = self.client.post(self.url + 'new/', data=form_data)
        self.assertRaises(Question.DoesNotExist, Question.objects.get, text=form_data['text'], instructions=form_data['instructions'], answer_type=form_data['answer_type'])
        self.assertIn('Question NOT created. See errors below.', response.content)
        self.assertIsInstance(response.context['form'], QuestionForm)
        self.assertEqual("CREATE", response.context['btn_label'])
        self.assertEqual("id-new-question-form", response.context['id'])

    def test_delete_question(self):
        data = {'text': 'B. Number of cases tested',
                'instructions': "Enter the total number of cases",
                'UID': '00001', 'answer_type': 'Number',
                'theme': self.theme.id}
        query_data = data.copy()
        del query_data['theme']
        question = Question.objects.create(**query_data)
        response = self.client.post('/questions/%s/delete/' % question.id, {})
        self.assertRedirects(response, self.url)
        self.assertRaises(Question.DoesNotExist, Question.objects.get, **data)
        message = "Question was deleted successfully"
        self.assertIn(message, response.cookies['messages'].value)

    def test_does_not_delete_question_when_it_belongs_to_others(self):
        data = {'text': 'B. Number of cases tested',
                'instructions': "Enter the total number of cases",
                'UID': '00001', 'answer_type': 'Number',
                'theme': self.theme.id}
        query_data = data.copy()
        del query_data['theme']
        question = Question.objects.create(region=Region.objects.create(name="AFR"), **query_data)
        delete_url = '/questions/%s/delete/' % question.id
        response = self.client.post(delete_url, {})
        self.assertRedirects(response, expected_url='/accounts/login/?next=%s' % quote(delete_url))

    def test_does_not_delete_question_when_it_has_answers(self):
        data = {'text': 'B. Number of cases tested',
                'instructions': "Enter the total number of cases",
                'UID': '00001', 'answer_type': 'Number',
                'theme': self.theme}
        question = Question.objects.create(**data)
        country = Country.objects.create(name="Peru")
        Answer.objects.create(question=question, country=country, status="Submitted")

        response = self.client.post('/questions/%s/delete/' % question.id, {})
        self.assertRedirects(response, self.url)
        self.failUnless(Question.objects.get(**data))
        message = "Question was not deleted because it has responses"
        self.assertIn(message, response.cookies['messages'].value)

    def test_questions_list_in_particular_theme(self):
        data = {'text': 'B. Number of cases tested',
                'instructions': "Enter the total number of cases",
                'UID': '00001', 'answer_type': 'Number',
                'theme': self.theme}
        question = Question.objects.create(**data)
        response = self.client.get('/questions/?theme=%d' % self.theme.id)
        self.failUnless(Question.objects.get(**data))
        self.assertIn(question, response.context['questions'])


class RegionalQuestionsViewTest(BaseTest):

    def setUp(self):

        self.client = Client()
        self.user, self.country, self.region = self.create_user_with_no_permissions()

        self.questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English", year=2013, region=self.region)
        self.section = Section.objects.create(name="section", questionnaire=self.questionnaire, order=1, region=self.region)
        self.subsection = SubSection.objects.create(title="subsection 1", section=self.section, order=1, region=self.region)
        self.assign('can_edit_questionnaire', self.user)
        self.client.login(username=self.user.username, password='pass')

        self.url = '/questions/'
        self.theme = Theme.objects.create(name="Another theme")
        self.form_data = {'text': 'How many kids were immunised this year?',
                          'instructions': 'Some instructions',
                          'export_label': 'blah',
                          'answer_type': 'Number',
                          'theme': self.theme.id}

    def test_get_regional_questions(self):
        question1 = Question.objects.create(text='Q1', UID='C00003', answer_type='Number', region=self.region)
        question2 = Question.objects.create(text='Q2', UID='C00002', answer_type='Number', region=self.region)
        question3 = Question.objects.create(text='Q3', UID='C00001', answer_type='Number')
        question_group = question1.question_group.create(subsection=self.subsection)
        question_group.question.add(question2, question3)

        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
        templates = [template.name for template in response.templates]
        self.assertIn('questions/index.html', templates)
        self.assertIn(question1, response.context['questions'])
        self.assertIn(question2, response.context['questions'])
        self.assertNotIn(question3, response.context['questions'])
        self.assertIsNone(response.context['active_questions'])

    def test_post_create_question_for_region(self):
        self.assertRaises(Question.DoesNotExist, Question.objects.get, **self.form_data)
        response = self.client.post(self.url + 'new/', data=self.form_data)
        self.assertRedirects(response, self.url)
        self.failUnless(Question.objects.get(region=self.user.user_profile.region, **self.form_data))
        self.assertIn("Question successfully created.", response.cookies['messages'].value)

    def test_delete_question(self):
        data = {'text': 'B. Number of cases tested',
                'instructions': "Enter the total number of cases",
                'UID': '00001', 'answer_type': 'Number',
                'theme': self.theme}
        question = Question.objects.create(region=self.region, **data)
        response = self.client.post('/questions/%s/delete/' % question.id, {})
        self.assertRedirects(response, self.url)
        self.assertRaises(Question.DoesNotExist, Question.objects.get, **data)
        message = "Question was deleted successfully"
        self.assertIn(message, response.cookies['messages'].value)

    def test_delete_question_question_not_belonging_to_their_region_shows_error(self):
        user_not_in_same_region, country, region = self.create_user_with_no_permissions(username="asian_chic",
                                                                                        country_name="China",
                                                                                        region_name="ASEAN")
        data = {'text': 'B. Number of cases tested',
                'instructions': "Enter the total number of cases",
                'UID': '00001', 'answer_type': 'Number',
                'theme': self.theme}
        paho = Region.objects.create(name="paho")
        question = Question.objects.create(region=paho, **data)
        self.assert_permission_required(self.url)
        self.assign('can_edit_questionnaire', user_not_in_same_region)
        self.client.logout()
        self.client.login(username='asian_chic', password='pass')

        url = '/questions/%s/delete/' % question.id
        response = self.client.post(url)

        self.failUnless(Question.objects.filter(id=question.id))
        self.assertRedirects(response, expected_url='/accounts/login/?next=%s' % quote(url))


class DoesNotExistExceptionViewTest(BaseTest):
    def setUp(self):
        self.client = Client()
        self.user, self.country, self.region = self.create_user_with_no_permissions()

        self.questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English", year=2013, region=self.region)
        self.section = Section.objects.create(name="section", questionnaire=self.questionnaire, order=1, region=self.region)
        self.subsection = SubSection.objects.create(title="subsection 1", section=self.section, order=1, region=self.region)
        self.assign('can_edit_questionnaire', self.user)
        self.client.login(username=self.user.username, password='pass')

        self.url = '/questions/'
        self.theme = Theme.objects.create(name="Another theme")
        self.form_data = {'text': 'How many kids were immunised this year?',
                          'instructions': 'Some instructions',
                          'export_label': 'blah',
                          'answer_type': 'Number',
                          'theme': self.theme.id}

    def test_get_regional_questions(self):
        unexisting_id_question = 123
        url = '/questions/%d/delete/' % unexisting_id_question
        response = self.client.post(url)
        message = "Sorry, You tried to delete a question does not exist"
        self.assertRedirects(response, expected_url=reverse('list_questions_page'))
        self.assertIn(message, response.cookies['messages'].value)


class EditQuestionViewTest(BaseTest):

    def setUp(self):
        self.client = Client()
        self.user, self.country, self.region = self.create_user_with_no_permissions(region_name=None)

        self.assign('can_edit_questionnaire', self.user)
        self.client.login(username=self.user.username, password='pass')

        self.questionnaire = Questionnaire.objects.create(name="2014", description="some description")
        self.section = Section.objects.create(title="section", order=1, questionnaire=self.questionnaire)
        self.sub_section = SubSection.objects.create(title="subsection", order=1, section=self.section)
        self.question1 = Question.objects.create(text='q1', UID='C00003', answer_type='Number')
        self.parent_group = QuestionGroup.objects.create(subsection=self.sub_section, name="group1")
        self.parent_group.question.add(self.question1)
        self.theme = Theme.objects.create(name="Another theme")
        self.url = '/questions/%d/edit/'%self.question1.id
        self.form_data = {'text': 'How many kids were immunised this year?',
                          'instructions': 'Some instructions',
                          'export_label': 'blah',
                          'answer_type': 'Number',
                          'theme': self.theme.id}

    def test_get_edit_question(self):
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
        templates = [template.name for template in response.templates]
        self.assertIn('questions/new.html', templates)
        self.assertIsInstance(response.context['form'], QuestionForm)
        self.assertEqual(self.question1, response.context['form'].instance)
        self.assertEqual("SAVE", response.context['btn_label'])
        self.assertEqual("id-new-question-form", response.context['id'])
        self.assertEqual(reverse('list_questions_page'), response.context['cancel_url'])
        self.assertEqual('Edit Question', response.context['title'])

    def test_post_edit_question_when_questionnaire_is_not_published(self):
        response = self.client.post(self.url, data=self.form_data)
        self.assertRedirects(response, reverse('list_questions_page'))
        self.failUnless(Question.objects.get(**self.form_data))
        self.assertIn("Question successfully updated.", response.cookies['messages'].value)

    def test_post_edit_with_invalid_form_returns_errors(self):
        form_data = self.form_data.copy()
        form_data['text'] = ''

        response = self.client.post(self.url, data=form_data)
        self.assertRaises(Question.DoesNotExist, Question.objects.get, **form_data)
        self.assertIn('Question NOT updated. See errors below.', response.content)
        self.assertIsInstance(response.context['form'], QuestionForm)
        self.assertEqual("SAVE", response.context['btn_label'])
        self.assertEqual(reverse('list_questions_page'), response.context['cancel_url'])
        self.assertEqual("id-new-question-form", response.context['id'])
        self.assertEqual('Edit Question', response.context['title'])

    def test_post_edit_to_multichoice_question_with_options(self):
        form_data = self.form_data.copy()
        form_data['answer_type'] = 'MultiChoice'
        question_options = ['yes, No, Maybe, Nr, Chill']
        self.assertRaises(Question.DoesNotExist, Question.objects.get, **form_data)
        form_data['options'] = question_options
        response = self.client.post(self.url, data=form_data)
        self.assertRedirects(response, reverse('list_questions_page'))
        questions = Question.objects.filter(text=form_data['text'], instructions=form_data['instructions'],
                                            answer_type=form_data['answer_type'])
        self.assertEqual(1, len(questions))
        options = questions[0].options.all()

        self.assertEqual(5, options.count())
        [self.assertIn(option.text, ['yes', 'No', 'Maybe', 'Nr', 'Chill']) for option in options]

    def test_post_edit_to_multichoice_question_with_options_with_form_errors(self):
        form_data = self.form_data.copy()
        form_data['answer_type'] = 'MultiChoice'
        self.assertRaises(Question.DoesNotExist, Question.objects.get, **form_data)
        form_data['options'] = []
        response = self.client.post(self.url, data=form_data)
        self.assertRaises(Question.DoesNotExist, Question.objects.get, text=form_data['text'], instructions=form_data['instructions'], answer_type=form_data['answer_type'])
        self.assertIn('Question NOT updated. See errors below.', response.content)
        self.assertIsInstance(response.context['form'], QuestionForm)
        self.assertEqual("SAVE", response.context['btn_label'])
        self.assertEqual("id-new-question-form", response.context['id'])

    def test_post_edit_when_question_is_in_published_questionnaire_duplicates_question_and_assign_new_question_to_all_unpublished_questionnaires(self):
        self.questionnaire.status = Questionnaire.PUBLISHED
        self.questionnaire.save()
        self.question1.orders.create(order=1, question_group=self.parent_group)

        draft_questionnaire = Questionnaire.objects.create(name="draft qnaire",description="haha",
                                                           status=Questionnaire.DRAFT)
        section_1 = Section.objects.create(title="section 1", order=1, questionnaire=draft_questionnaire, name="ha")
        sub_section_1 = SubSection.objects.create(title="subs1", order=1, section=section_1)
        parent_group_d = QuestionGroup.objects.create(subsection=sub_section_1, name="group")
        parent_group_d.question.add(self.question1)
        self.question1.orders.create(order=2, question_group=parent_group_d)

        finalized_questionnaire = Questionnaire.objects.create(name="finalized qnaire",description="haha",
                                                           status=Questionnaire.FINALIZED)
        section_1_f = Section.objects.create(title="section 1", order=1, questionnaire=finalized_questionnaire, name="ha")
        sub_section_1_f = SubSection.objects.create(title="subs1", order=1, section=section_1_f)
        parent_group_f = QuestionGroup.objects.create(subsection=sub_section_1_f, name="group")
        parent_group_f.question.add(self.question1)
        self.question1.orders.create(order=3, question_group=parent_group_f)

        response = self.client.post(self.url, data=self.form_data)

        duplicate_question = Question.objects.get(UID=self.question1.UID, **self.form_data)

        parent_group_questions = self.parent_group.question.all()
        self.assertEqual(1, parent_group_questions.count())
        self.assertIn(self.question1, parent_group_questions)

        parent_group_d_questions = parent_group_d.question.all()
        self.assertEqual(1, parent_group_d_questions.count())
        self.assertIn(duplicate_question, parent_group_d_questions)

        parent_group_f_questions = parent_group_f.question.all()
        self.assertEqual(1, parent_group_f_questions.count())
        self.assertIn(duplicate_question, parent_group_f_questions)

        self.assertEqual(1, self.question1.orders.get(question_group=self.parent_group).order)
        self.assertEqual(0, duplicate_question.orders.filter(question_group=self.parent_group).count())

        self.assertEqual(2, duplicate_question.orders.get(question_group=parent_group_d).order)
        self.assertEqual(0, self.question1.orders.filter(question_group=parent_group_d).count())

        self.assertEqual(3, duplicate_question.orders.get(question_group=parent_group_f).order)
        self.assertEqual(0, self.question1.orders.filter(question_group=parent_group_f).count())

    def test_post_edit_multichoice_options_are_only_edited_in_the_duplicate_questions(self):
        self.questionnaire.status = Questionnaire.PUBLISHED
        self.questionnaire.save()
        self.question1.orders.create(order=1, question_group=self.parent_group)
        self.question1.answer_type = 'MultiChoice'
        self.question1.save()
        question1_options_texts = ["Yes", "No", "DK"]
        for text in question1_options_texts:
            self.question1.options.create(text=text)

        draft_questionnaire = Questionnaire.objects.create(name="draft qnaire",description="haha",
                                                           status=Questionnaire.DRAFT)
        section_1 = Section.objects.create(title="section 1", order=1, questionnaire=draft_questionnaire, name="ha")
        sub_section_1 = SubSection.objects.create(title="subs1", order=1, section=section_1)
        parent_group_d = QuestionGroup.objects.create(subsection=sub_section_1, name="group")
        parent_group_d.question.add(self.question1)
        self.question1.orders.create(order=2, question_group=parent_group_d)

        finalized_questionnaire = Questionnaire.objects.create(name="finalized qnaire",description="haha",
                                                           status=Questionnaire.FINALIZED)
        section_1_f = Section.objects.create(title="section 1", order=1, questionnaire=finalized_questionnaire, name="ha")
        sub_section_1_f = SubSection.objects.create(title="subs1", order=1, section=section_1_f)
        parent_group_f = QuestionGroup.objects.create(subsection=sub_section_1_f, name="group")
        parent_group_f.question.add(self.question1)
        self.question1.orders.create(order=3, question_group=parent_group_f)

        changed_options = ['', 'haha', 'hehe', 'hihi']
        data = {'text': 'changed text',
                'instructions': 'Some instructions',
                'export_label': 'blah',
                'answer_type': 'MultiChoice',
                'options': changed_options,
                'theme': self.theme.id}

        response = self.client.post(self.url, data=data)

        data.pop('options')
        duplicate_question = Question.objects.get(UID=self.question1.UID, **data)

        question1_options = self.question1.options.all()
        self.assertEqual(3, question1_options.count())
        [self.assertIn(question_option.text, question1_options_texts) for question_option in question1_options]

        duplicate_question_options = duplicate_question.options.all()
        self.assertEqual(3, duplicate_question_options.count())
        [self.assertIn(question_option.text, changed_options) for question_option in duplicate_question_options]
