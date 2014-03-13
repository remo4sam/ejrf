from urllib import quote
from questionnaire.forms.assign_question import AssignQuestionForm
from questionnaire.models import Questionnaire, Section, SubSection, Question
from questionnaire.tests.base_test import BaseTest
from django.test import Client


class AssignQuestionViewTest(BaseTest):

    def setUp(self):
        self.client = Client()
        self.user, self.country, self.region = self.create_user_with_no_permissions()

        self.assign('can_edit_questionnaire', self.user)
        self.client.login(username=self.user.username, password='pass')

        self.questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English", year=2013, region=self.region)
        self.section = Section.objects.create(name="section", questionnaire=self.questionnaire, order=1)

        self.subsection = SubSection.objects.create(title="subsection 1", section=self.section, order=1)
        self.question1 = Question.objects.create(text='Q1', UID='C00003', answer_type='Number', region=self.region)
        self.question2 = Question.objects.create(text='Q2', UID='C00002', answer_type='Number', region=self.region)
        self.form_data = {'questions': [self.question1.id, self.question2.id]}
        self.url = '/subsection/%d/assign_questions/' % self.subsection.id

    def test_get_assign_question_page(self):
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
        templates = [template.name for template in response.templates]
        self.assertIn('questionnaires/assign_questions.html', templates)

    def test_gets_assign_questions_form_and_subsection_in_context(self):
        question_not_in_region = Question.objects.create(text='not in Region Q', UID='C000R3', answer_type='Number')

        response = self.client.get(self.url)
        self.assertIsInstance(response.context['assign_question_form'], AssignQuestionForm)
        self.assertEqual(2, response.context['questions'].count())
        questions_texts = [question.text for question in list(response.context['questions'])]
        self.assertIn(self.question1.text, questions_texts)
        self.assertIn(self.question2.text, questions_texts)
        self.assertNotIn(question_not_in_region.text, questions_texts)
        self.assertEqual('Done', response.context['btn_label'])

    def test_GET_puts_list_of_already_used_questions_in_context(self):
        question1 = Question.objects.create(text='USed question', UID='C00033', answer_type='Number', region=self.region)
        question1.question_group.create(subsection=self.subsection)

        response = self.client.get(self.url)

        self.assertEqual(1, len(response.context['active_questions']))
        self.assertIn(question1, response.context['active_questions'])

    def test_post_questions_assigns_them_to_subsections_and_get_or_create_group(self):
        self.failIf(self.question1.question_group.all())
        self.failIf(self.question2.question_group.all())

        meta = {'HTTP_REFERER': self.url}
        response = self.client.post(self.url, data={'questions':[self.question1.id, self.question2.id]}, **meta)

        question_group = self.question1.question_group.all()
        self.assertEqual(1, question_group.count())
        self.assertEqual(question_group[0], self.question2.question_group.all()[0])
        self.assertEqual(self.subsection, question_group[0].subsection)

    def test_successful_post_redirect_to_referer_url(self):
        meta = {'HTTP_REFERER': self.url}
        response = self.client.post(self.url, data={'questions':[self.question1.id, self.question2.id]}, **meta)
        self.assertRedirects(response, self.url)

    def test_successful_post_display_success_message(self):
        referer_url = '/questionnaire/entry/%d/section/%d/' % (self.questionnaire.id, self.section.id)
        meta = {'HTTP_REFERER': referer_url}
        response = self.client.post(self.url, data={'questions': [self.question1.id, self.question2.id]}, **meta)
        message = "Questions successfully assigned to questionnaire."
        self.assertIn(message, response.cookies['messages'].value)

    def test_with_errors_returns_the_form_with_error(self):
        referer_url = '/questionnaire/entry/%d/section/%d/' % (self.questionnaire.id, self.section.id)
        meta = {'HTTP_REFERER': referer_url}
        response = self.client.post(self.url, data={'questions': []}, **meta)

        self.assertIsInstance(response.context['assign_question_form'], AssignQuestionForm)
        self.assertIn("This field is required.", response.context['assign_question_form'].errors['questions'])
        self.assertEqual(2, response.context['questions'].count())
        questions_texts = [question.text for question in list(response.context['questions'])]
        self.assertIn(self.question1.text, questions_texts)
        self.assertIn(self.question2.text, questions_texts)
        self.assertEqual('Done', response.context['btn_label'])

    def test_login_required(self):
        self.assert_login_required(self.url)

    def test_permission_required_for_create_section(self):
        self.assert_permission_required(self.url)

        user_not_in_same_region, country, region = self.create_user_with_no_permissions(username="asian_chic",
                                                                                        country_name="China",
                                                                                        region_name="ASEAN")
        self.assign('can_edit_questionnaire', user_not_in_same_region)

        self.client.logout()
        self.client.login(username='asian_chic', password='pass')
        response = self.client.get(self.url)
        self.assertRedirects(response, expected_url='/accounts/login/?next=%s' % quote(self.url))
        response = self.client.post(self.url)
        self.assertRedirects(response, expected_url='/accounts/login/?next=%s' % quote(self.url))


class UnAssignQuestionViewTest(BaseTest):

    def setUp(self):
        self.client = Client()
        self.user, self.country, self.region = self.create_user_with_no_permissions()

        self.assign('can_edit_questionnaire', self.user)
        self.client.login(username=self.user.username, password='pass')

        self.questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English", year=2013, region=self.region)
        self.section = Section.objects.create(name="section", questionnaire=self.questionnaire, order=1)

        self.subsection = SubSection.objects.create(title="subsection 1", section=self.section, order=1)
        self.question1 = Question.objects.create(text='Q1', UID='C00003', answer_type='Number', region=self.region)
        self.question2 = Question.objects.create(text='Q2', UID='C00002', answer_type='Number', region=self.region)
        self.question_group = self.question1.question_group.create(subsection=self.subsection)
        self.question1.orders.create(question_group=self.question_group, order=1)
        self.question_group.question.add(self.question2)
        self.question2.orders.create(question_group=self.question_group, order=2)

        self.url = '/subsection/%d/question/%d/unassign/'%(self.subsection.id, self.question1.id)

    def test_post_unassign_question_to_group_and_removes_question_order(self):
        meta = {'HTTP_REFERER': '/questionnaire/entry/%d/section/%d/' % (self.questionnaire.id, self.section.id)}
        response = self.client.post(self.url, {}, **meta)
        group_questions = self.question_group.question.all()

        self.assertNotIn(self.question1, group_questions)
        self.assertEqual(0, self.question1.orders.all().count())

    def test_successful_post_redirect_to_referer_url(self):
        referer_url = '/questionnaire/entry/%d/section/%d/' % (self.questionnaire.id, self.section.id)
        meta = {'HTTP_REFERER': referer_url}
        response = self.client.post(self.url, data={}, **meta)
        self.assertRedirects(response, referer_url)

    def test_successful_post_display_success_message(self):
        referer_url = '/questionnaire/entry/%d/section/%d/'%(self.questionnaire.id, self.section.id)
        meta = {'HTTP_REFERER': referer_url}
        response = self.client.post(self.url, data={}, **meta)
        message = "Question successfully unassigned from questionnaire."
        self.assertIn(message, response.cookies['messages'].value)

    def test_login_required(self):
        self.assert_login_required(self.url)

    def test_permission_required_for_create_section(self):
        self.assert_permission_required(self.url)

        user_not_in_same_region, country, region = self.create_user_with_no_permissions(username="asian_chic",
                                                                                        country_name="China",
                                                                                        region_name="ASEAN")
        self.assign('can_edit_questionnaire', user_not_in_same_region)

        self.client.logout()
        self.client.login(username='asian_chic', password='pass')
        response = self.client.post(self.url)
        self.assertRedirects(response, expected_url='/accounts/login/?next=%s' % quote(self.url))

    def test_permission_denied_if_subsection_belongs_to_a_user_but_question_to_another_user(self):
        core_question = Question.objects.create(text='core Q', UID='C000C2', answer_type='Number', region=None)
        self.question_group.question.add(core_question)

        url = '/subsection/%d/question/%d/unassign/'%(self.subsection.id, core_question.id)

        response = self.client.post(url)
        self.assertRedirects(response, expected_url='/accounts/login/?next=%s' % quote(url))