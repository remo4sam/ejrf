from django.core.urlresolvers import reverse
from django.test import Client

from questionnaire.forms.sections import SectionForm, SubSectionForm
from questionnaire.models import Questionnaire, Section, SubSection
from questionnaire.tests.base_test import BaseTest
 

class SectionsViewTest(BaseTest):

    def setUp(self):
        self.client = Client()
        self.user, self.country = self.create_user_with_no_permissions()

        self.assign('can_edit_questionnaire', self.user)
        self.client.login(username=self.user.username, password='pass')

        self.questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English", year=2013)
        self.url = '/questionnaire/entry/%s/section/new/' % self.questionnaire.id
        self.form_data = {'name': 'New section',
                          'description': 'funny section',
                          'title': 'some title',
                          'questionnaire': self.questionnaire.id}

    def test_get_create_section(self):
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
        templates = [template.name for template in response.templates]
        self.assertIn("sections/subsections/new.html", templates)
        self.assertIsNotNone(response.context['form'])
        self.assertIsInstance(response.context['form'], SectionForm)
        self.assertEqual("CREATE", response.context['btn_label'])

    def test_post_create_section(self):
        self.failIf(Section.objects.filter(**self.form_data))
        response = self.client.post(self.url, data=self.form_data)
        section = Section.objects.get(**self.form_data)
        self.failUnless(section)
        self.assertRedirects(response, expected_url='/questionnaire/entry/%s/section/%s/' % (self.questionnaire.id ,section.id))

    def test_post_with_form_increments_order_before_saving(self):
        Section.objects.create(name="Some", order=1, questionnaire=self.questionnaire)
        form_data = self.form_data.copy()
        form_data['name'] = 'Another section'
        self.failIf(Section.objects.filter(**form_data))
        response = self.client.post(self.url, data=form_data)
        section = Section.objects.get(order=2, name=form_data['name'])
        self.failUnless(section)
        self.assertRedirects(response, expected_url='/questionnaire/entry/%s/section/%s/' % (self.questionnaire.id ,section.id))

    def test_permission_required_for_create_section(self):
        self.assert_login_required(self.url)
        self.assert_permission_required(self.url)

    def test_post_invalid(self):
        Section.objects.create(name="Some", order=1, questionnaire=self.questionnaire)
        form_data = self.form_data.copy()
        form_data['name'] = ''
        self.failIf(Section.objects.filter(**form_data))
        response = self.client.post(self.url, data=form_data)
        section = Section.objects.filter(order=2, name=form_data['name'])
        self.failIf(section)
        self.assertIn('Section NOT created. See errors below.', response.content)
        self.assertIsInstance(response.context['form'], SectionForm)
        self.assertEqual("new-section-modal", response.context['id'])
        self.assertEqual("CREATE", response.context['btn_label'])


class EditSectionsViewTest(BaseTest):

    def setUp(self):
        self.client = Client()
        self.user, self.country = self.create_user_with_no_permissions()

        self.assign('can_edit_questionnaire', self.user)
        self.client.login(username=self.user.username, password='pass')

        self.questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English", year=2013)

        self.form_data = {'name': 'section',
                          'description': 'funny section',
                          'title': 'some title',
                          'order':1,
                          'questionnaire': self.questionnaire.id}
        self.create_form_data = self.form_data.copy()
        del self.create_form_data['questionnaire']
        self.section = Section.objects.create(questionnaire=self.questionnaire, **self.create_form_data)
        self.url = '/section/%d/edit/' % self.section.id

    def test_get_edit_section(self):
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
        templates = [template.name for template in response.templates]
        self.assertIn("sections/subsections/new.html", templates)
        self.assertIsNotNone(response.context['form'])
        self.assertIsInstance(response.context['form'], SectionForm)
        self.assertEqual(self.section, response.context['form'].instance)
        self.assertEqual("SAVE", response.context['btn_label'])

    def test_post_create_section(self):
        data = self.form_data.copy()
        data['name'] = 'Edited section name'
        self.failIf(Section.objects.filter(**data))
        response = self.client.post(self.url, data=data)
        section = Section.objects.get(**data)
        self.failUnless(section)
        self.assertRedirects(response, expected_url='/questionnaire/entry/%s/section/%s/' % (self.questionnaire.id ,section.id))
        self.assertIn('Section updated successfully.', response.cookies['messages'].value)

    def test_permission_required_for_edit_section(self):
        self.assert_login_required(self.url)
        self.assert_permission_required(self.url)

    def test_post_invalid(self):
        form_data = self.form_data.copy()
        form_data['name'] = ''
        self.failIf(Section.objects.filter(**form_data))
        response = self.client.post(self.url, data=form_data)
        section = Section.objects.filter(**form_data)
        self.failIf(section)
        self.assertIn('Section NOT updated. See errors below.', response.content)
        self.assertIsInstance(response.context['form'], SectionForm)
        self.assertEqual("SAVE", response.context['btn_label'])


class SubSectionsViewTest(BaseTest):

    def setUp(self):
        self.client = Client()
        self.user, self.country = self.create_user_with_no_permissions()

        self.assign('can_edit_questionnaire', self.user)
        self.client.login(username=self.user.username, password='pass')

        self.questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English", year=2013)
        self.section = Section.objects.create(name="section", questionnaire=self.questionnaire, order=1)
        self.url = '/questionnaire/entry/%s/section/%s/subsection/new/' % (self.questionnaire.id, self.section.id)
        self.form_data = {
                          'description': 'funny section',
                          'title': 'some title',
                        }

    def test_permission_required_for_create_section(self):
        self.assert_login_required(self.url)
        self.assert_permission_required(self.url)

    def test_get_create_subsection(self):
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
        templates = [template.name for template in response.templates]
        self.assertIn("sections/subsections/new.html", templates)
        self.assertIsNotNone(response.context['form'])
        self.assertIsInstance(response.context['form'], SubSectionForm)
        self.assertEqual("CREATE", response.context['btn_label'])

    def test_post_create_subsection(self):
        self.failIf(SubSection.objects.filter(section=self.section, **self.form_data))
        response = self.client.post(self.url, data=self.form_data)
        subsection = SubSection.objects.filter(section=self.section, **self.form_data)
        self.failUnless(subsection)
        self.assertEqual(1, subsection.count())
        self.assertIn('Subsection successfully created.', response.cookies['messages'].value)
        self.assertRedirects(response,expected_url='/questionnaire/entry/%s/section/%s/' % (self.questionnaire.id ,self.section.id))

    def test_post_with_form_increments_order_before_saving(self):
        SubSection.objects.create(title="Some", order=1, section=self.section)
        form_data = self.form_data.copy()
        form_data['title'] = 'Another subsection'
        self.failIf(SubSection.objects.filter(section=self.section, **form_data))
        response = self.client.post(self.url, data=form_data)
        subsection = SubSection.objects.filter(order=2, title=form_data['title'])
        self.failUnless(subsection)
        self.assertEqual(1, subsection.count())
        self.assertRedirects(response,expected_url='/questionnaire/entry/%s/section/%s/' % (self.questionnaire.id ,self.section.id))

    def test_post_invalid(self):
        SubSection.objects.create(title="Some", order=1, section=self.section)
        form_data = self.form_data.copy()
        form_data['title'] = ''
        self.failIf(SubSection.objects.filter(section=self.section, **form_data))
        response = self.client.post(self.url, data=form_data)
        subsection = SubSection.objects.filter(order=2, title=form_data['title'])
        self.failIf(subsection)
        self.assertIn('Subsection NOT created. See errors below.', response.content)
        self.assertIsInstance(response.context['form'], SubSectionForm)
        self.assertEqual("new-subsection-modal", response.context['id'])
        self.assertEqual("CREATE", response.context['btn_label'])


class EditSubSectionsViewTest(BaseTest):

    def setUp(self):
        self.client = Client()
        self.user, self.country = self.create_user_with_no_permissions()

        self.assign('can_edit_questionnaire', self.user)
        self.client.login(username=self.user.username, password='pass')

        self.questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English", year=2013)
        self.section = Section.objects.create(questionnaire=self.questionnaire, name="section", order=1)
        self.form_data = {'description': 'funny section',
                          'title': 'some title',
                          'order': 1,
                          'section': self.section.id}
        self.create_form_data = self.form_data.copy()
        del self.create_form_data['section']
        self.subsection = SubSection.objects.create(section=self.section, **self.create_form_data)
        self.url = '/subsection/%d/edit/' % self.subsection.id

    def test_get_edit_section(self):
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
        templates = [template.name for template in response.templates]
        self.assertIn("sections/subsections/new.html", templates)
        self.assertIsNotNone(response.context['form'])
        self.assertIsInstance(response.context['form'], SubSectionForm)
        self.assertEqual(self.subsection, response.context['form'].instance)
        self.assertEqual("SAVE", response.context['btn_label'])

    def test_post_create_section(self):
        data = self.form_data.copy()
        data['title'] = 'Edited subsection name'
        del data['order']
        self.failIf(SubSection.objects.filter(**data))
        response = self.client.post(self.url, data=data)
        subsection = SubSection.objects.get(**data)
        self.assertRedirects(response, expected_url=self.subsection.get_absolute_url())
        self.failUnless(subsection)
        self.assertIn('SubSection updated successfully.', response.cookies['messages'].value)

    def test_permission_required_for_edit_section(self):
        self.assert_login_required(self.url)
        self.assert_permission_required(self.url)

    def test_post_invalid(self):
        form_data = self.form_data.copy()
        form_data['title'] = ''
        self.failIf(SubSection.objects.filter(**form_data))
        response = self.client.post(self.url, data=form_data)
        section = SubSection.objects.filter(**form_data)
        self.failIf(section)
        self.assertIn('SubSection NOT updated. See errors below.', response.content)
        self.assertIsInstance(response.context['form'], SubSectionForm)
        self.assertEqual("SAVE", response.context['btn_label'])


class DeleteSectionsViewTest(BaseTest):

    def setUp(self):
        self.client = Client()
        self.user, self.country = self.create_user_with_no_permissions()

        self.assign('can_edit_questionnaire', self.user)
        self.client.login(username=self.user.username, password='pass')

        self.questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English", year=2013)
        self.section = Section.objects.create(name="section", questionnaire=self.questionnaire, order=1)
        self.section_1 = Section.objects.create(name="section 2", questionnaire=self.questionnaire, order=2)
        self.url = '/section/%d/delete/' % self.section.id

    def test_post_deletes_section(self):
        response = self.client.post(self.url)
        self.assertNotIn(self.section, Section.objects.all())

    def test_successful_post_redirect_to_referrer_url(self):
        referer_url = '/questionnaire/entry/%d/section/%d/' % (self.questionnaire.id, self.section_1.id)
        meta = {'HTTP_REFERER': referer_url}
        response = self.client.post(self.url, data={}, HTTP_REFERER=referer_url)
        self.assertRedirects(response, referer_url)

    def test_successful_post_redirect_to_home_page_if_referer_url_is_self(self):
        referer_url = '/questionnaire/entry/%d/section/%d/' % (self.questionnaire.id, self.section.id)
        meta = {'HTTP_REFERER': referer_url}
        response = self.client.post(self.url, data={}, HTTP_REFERER=referer_url)
        self.assertRedirects(response, reverse('home_page'), target_status_code=302)

    def test_successful_post_display_success_message(self):
        referer_url = '/questionnaire/entry/%d/section/%d/'%(self.questionnaire.id, self.section_1.id)
        meta = {'HTTP_REFERER': referer_url}
        response = self.client.post(self.url, data={}, **meta)
        message = "Section successfully deleted."
        self.assertIn(message, response.cookies['messages'].value)