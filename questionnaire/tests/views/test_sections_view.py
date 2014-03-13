from django.core.urlresolvers import reverse
from django.test import Client

from questionnaire.forms.sections import SectionForm, SubSectionForm
from questionnaire.models import Questionnaire, Section, SubSection, Region
from questionnaire.tests.base_test import BaseTest
from urllib import quote


class SectionsViewTest(BaseTest):
    def setUp(self):
        self.client = Client()
        self.user, self.country, self.region = self.create_user_with_no_permissions()

        self.assign('can_edit_questionnaire', self.user)
        self.client.login(username=self.user.username, password='pass')

        self.questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English", year=2013, region=self.region)
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
        self.assertEqual(self.region, section.region)
        self.assertRedirects(response,
                             expected_url='/questionnaire/entry/%s/section/%s/' % (self.questionnaire.id, section.id))

    def test_post_with_form_increments_order_before_saving(self):
        Section.objects.create(name="Some", order=1, questionnaire=self.questionnaire)
        form_data = self.form_data.copy()
        form_data['name'] = 'Another section'
        self.failIf(Section.objects.filter(**form_data))
        response = self.client.post(self.url, data=form_data)
        section = Section.objects.get(order=2, name=form_data['name'])
        self.failUnless(section)
        self.assertRedirects(response,
                             expected_url='/questionnaire/entry/%s/section/%s/' % (self.questionnaire.id, section.id))

    def test_permission_required_for_create_section(self):
        self.assert_permission_required(self.url)

        user_not_in_same_region, country, region = self.create_user_with_no_permissions(username="asian_chic",
                                                                                        country_name="China",
                                                                                        region_name="ASEAN")
        self.assign('can_edit_questionnaire', user_not_in_same_region)

        self.client.logout()
        self.client.login(username='asian_chic', password='pass')
        response = self.client.get(self.url)
        self.assertRedirects(response, expected_url='/accounts/login/?next=%s' % quote(self.url),
                             status_code=302, target_status_code=200, msg_prefix='')


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
        self.user, self.country, self.region = self.create_user_with_no_permissions()

        self.assign('can_edit_questionnaire', self.user)
        self.client.login(username=self.user.username, password='pass')

        self.questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English", year=2013, region=self.region)

        self.form_data = {'name': 'section',
                          'description': 'funny section',
                          'title': 'some title',
                          'order': 1,
                          'questionnaire': self.questionnaire.id}
        self.create_form_data = self.form_data.copy()
        del self.create_form_data['questionnaire']
        self.section = Section.objects.create(region=self.region, questionnaire=self.questionnaire, **self.create_form_data)
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
        self.assertRedirects(response,
                             expected_url='/questionnaire/entry/%s/section/%s/' % (self.questionnaire.id, section.id))
        self.assertIn('Section updated successfully.', response.cookies['messages'].value)

    def test_permission_required_for_create_section(self):
        self.assert_permission_required(self.url)

        user_not_in_same_region, country, region = self.create_user_with_no_permissions(username="asian_chic",
                                                                                        country_name="China",
                                                                                        region_name="ASEAN")
        self.assign('can_edit_questionnaire', user_not_in_same_region)

        self.client.logout()
        self.client.login(username='asian_chic', password='pass')
        response = self.client.post(self.url, data=self.create_form_data)
        self.assertRedirects(response, expected_url='/accounts/login/?next=%s' % quote(self.url),
                             status_code=302, target_status_code=200, msg_prefix='')

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

    def test_sections_owned_by_others_cannot_be_edited(self):
        self.section.region = None
        self.section.save()
        response = self.client.get(self.url)
        self.assertRedirects(response, expected_url='/accounts/login/?next=%s'%self.url)
        response = self.client.post(self.url)
        self.assertRedirects(response, expected_url='/accounts/login/?next=%s'%self.url)


class DeleteSectionsViewTest(BaseTest):
    def setUp(self):
        self.client = Client()
        self.user, self.country, self.region = self.create_user_with_no_permissions()
        self.assign('can_edit_questionnaire', self.user)
        self.client.login(username=self.user.username, password='pass')

        self.questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English", year=2013)
        self.section = Section.objects.create(name="section", questionnaire=self.questionnaire, order=1, region=self.region)
        self.section_1 = Section.objects.create(name="section 2", questionnaire=self.questionnaire, order=2, region=self.region)
        self.url = '/section/%d/delete/' % self.section.id

    def test_post_deletes_section(self):
        referer_url = '/questionnaire/entry/%d/section/%d/' % (self.questionnaire.id, self.section.id)
        self.client.post(self.url, HTTP_REFERER=referer_url)
        self.assertNotIn(self.section, Section.objects.all())

    def test_successful_post_redirect_to_referer_url_if_not_deleting_self(self):
        delete_url = '/section/%d/delete/' % self.section_1.id
        referer_url = '/questionnaire/entry/%d/section/%d/' % (self.questionnaire.id, self.section.id)
        response = self.client.post(delete_url, data={}, HTTP_REFERER=referer_url)
        self.assertRedirects(response, referer_url)

    def test_successful_post_redirect_to_first_section_if_referer_url_is_self(self):
        referer_url = '/questionnaire/entry/%d/section/%d/' % (self.questionnaire.id, self.section.id)
        response = self.client.post(self.url, data={}, HTTP_REFERER=referer_url)
        self.assertRedirects(response, reverse('questionnaire_entry_page', args=(self.questionnaire.id, self.section_1.id)))

    def test_successful_post_display_success_message(self):
        referer_url = '/questionnaire/entry/%d/section/%d/' % (self.questionnaire.id, self.section_1.id)
        meta = {'HTTP_REFERER': referer_url}
        response = self.client.post(self.url, data={}, **meta)
        message = "Section successfully deleted."
        self.assertIn(message, response.cookies['messages'].value)

    def test_successful_deletion_of_section_reindexes_section_orders(self):
        referer_url = '/questionnaire/entry/%d/section/%d/' % (self.questionnaire.id, self.section_1.id)
        meta = {'HTTP_REFERER': referer_url}
        section_3 = Section.objects.create(name="section", questionnaire=self.questionnaire, order=3, region=self.region)
        Section.objects.create(name="section 2", questionnaire=self.questionnaire, order=4)
        self.client.post('/section/%d/delete/' % section_3.id, data={}, **meta)
        self.assertEqual([1, 2, 3], list(Section.objects.values_list('order', flat=True)))

    def test_sections_owned_by_others_cannot_be_deleted(self):
        self.section.region = None
        self.section.save()
        response = self.client.get(self.url)
        self.assertRedirects(response, expected_url='/accounts/login/?next=%s'%self.url)
        response = self.client.post(self.url)
        self.assertRedirects(response, expected_url='/accounts/login/?next=%s'%self.url)


class SubSectionsViewTest(BaseTest):
    def setUp(self):
        self.client = Client()
        self.user, self.country, self.region = self.create_user_with_no_permissions()

        self.assign('can_edit_questionnaire', self.user)
        self.client.login(username=self.user.username, password='pass')

        self.questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English", year=2013, region=self.region)
        self.section = Section.objects.create(name="section", questionnaire=self.questionnaire, order=1)
        self.url = '/questionnaire/entry/%s/section/%s/subsection/new/' % (self.questionnaire.id, self.section.id)
        self.form_data = {
            'description': 'funny section',
            'title': 'some title',
        }

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
        self.assertRedirects(response, expected_url='/questionnaire/entry/%s/section/%s/' % (
        self.questionnaire.id, self.section.id))

    def test_post_with_form_increments_order_before_saving(self):
        SubSection.objects.create(title="Some", order=1, section=self.section)
        form_data = self.form_data.copy()
        form_data['title'] = 'Another subsection'
        self.failIf(SubSection.objects.filter(section=self.section, **form_data))
        response = self.client.post(self.url, data=form_data)
        subsection = SubSection.objects.filter(order=2, title=form_data['title'])
        self.failUnless(subsection)
        self.assertEqual(1, subsection.count())
        self.assertRedirects(response, expected_url='/questionnaire/entry/%s/section/%s/' % (
        self.questionnaire.id, self.section.id))

    def test_permission_required_for_create_section(self):
        self.assert_permission_required(self.url)

        user_not_in_same_region, country, region = self.create_user_with_no_permissions(username="asian_chic",
                                                                                        country_name="China",
                                                                                        region_name="ASEAN")
        self.assign('can_edit_questionnaire', user_not_in_same_region)

        self.client.logout()
        self.client.login(username='asian_chic', password='pass')
        response = self.client.get(self.url)
        self.assertRedirects(response, expected_url='/accounts/login/?next=%s' % quote(self.url),
                             status_code=302, target_status_code=200, msg_prefix='')

    def test_post_invalid(self):
        SubSection.objects.create(title="Some", order=1, section=self.section)
        form_data = self.form_data.copy()
        form_data['title'] = ''
        self.failIf(SubSection.objects.filter(section=self.section, **form_data))
        response = self.client.post(self.url, data=form_data)
        subsection = SubSection.objects.filter(order=2, title=form_data['title'])
        self.failUnless(subsection)
        self.assertEqual('', subsection[0].title)


class EditSubSectionsViewTest(BaseTest):
    def setUp(self):
        self.client = Client()
        self.user, self.country, self.region = self.create_user_with_no_permissions()

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
        self.subsection = SubSection.objects.create(section=self.section, region=self.region, **self.create_form_data)
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

    def test_subsections_owned_by_others_cannot_be_edited(self):
        self.subsection.region = None
        self.subsection.save()
        response = self.client.get(self.url)
        self.assertRedirects(response, expected_url='/accounts/login/?next=%s'%self.url)
        response = self.client.post(self.url)
        self.assertRedirects(response, expected_url='/accounts/login/?next=%s'%self.url)

    def test_post_invalid(self):
        form_data = self.form_data.copy()
        form_data['title'] = ''
        self.failIf(SubSection.objects.filter(**form_data))
        response = self.client.post(self.url, data=form_data)
        section = SubSection.objects.filter(**form_data)
        self.failUnless(section)
        self.assertEqual('', section[0].title)


class DeleteSubSectionsViewTest(BaseTest):
    def setUp(self):
        self.client = Client()
        self.user, self.country, self.region = self.create_user_with_no_permissions()

        self.assign('can_edit_questionnaire', self.user)
        self.client.login(username=self.user.username, password='pass')

        self.questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English", year=2013, region=self.region)
        self.section = Section.objects.create(name="section", questionnaire=self.questionnaire, order=1, region=self.region)
        self.form_data = {'description': 'First Section',
                          'title': 'Title for First Section',
                          'order': 1,
                          'section': self.section.id}
        self.create_form_data = self.form_data.copy()
        del self.create_form_data['section']
        self.subsection = SubSection.objects.create(section=self.section, region=self.region, **self.create_form_data)
        self.url = '/subsection/%d/delete/' % self.subsection.id

    def test_post_deletes_subsection(self):
        response = self.client.post(self.url)
        self.assertNotIn(self.subsection, SubSection.objects.all())

    def test_successful_post_redirect_to_referrer_url(self):
        referer_url = '/questionnaire/entry/%d/section/%d/' % (self.questionnaire.id, self.section.id)
        meta = {'HTTP_REFERER': referer_url}
        response = self.client.post(self.url, data={}, HTTP_REFERER=referer_url)
        self.assertRedirects(response, referer_url)

    def test_successful_post_display_success_message(self):
        response = self.client.post(self.url)
        message = "Subsection successfully deleted."
        self.assertIn(message, response.cookies['messages'].value)

    def test_successful_deletion_reindexes_subsections(self):
        sub_section1 = SubSection.objects.create(title="Cured Cases of Measles 3", order=2, section=self.section)
        sub_section2 = SubSection.objects.create(title="Cured Cases of Measles 3", order=3, section=self.section, region=self.region)
        sub_section3 = SubSection.objects.create(title="Cured Cases of Measles 3", order=4, section=self.section)
        referer_url = '/questionnaire/entry/%d/section/%d/' % (self.questionnaire.id, self.section.id)
        meta = {'HTTP_REFERER': referer_url}
        self.client.post('/subsection/%d/delete/' % sub_section2.id, data={}, **meta)
        self.assertEqual([1, 2, 3], list(SubSection.objects.values_list('order', flat=True)))

    def test_subsections_owned_by_others_cannot_be_deleted(self):
        self.subsection.region = None
        self.subsection.save()
        response = self.client.get(self.url)
        self.assertRedirects(response, expected_url='/accounts/login/?next=%s'%self.url)
        response = self.client.post(self.url)
        self.assertRedirects(response, expected_url='/accounts/login/?next=%s'%self.url)


class RegionalSectionsViewTest(BaseTest):

    def setUp(self):
        self.client = Client()
        self.user, self.country, self.region = self.create_user_with_no_permissions()
        self.questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English", year=2013, region=self.region)
        self.section = Section.objects.create(name="section", questionnaire=self.questionnaire, order=1, region=self.region)
        self.section1 = Section.objects.create(name="section1", questionnaire=self.questionnaire, order=2, region=self.region)
        self.subsection = SubSection.objects.create(title="subsection 1", section=self.section, order=1, region=self.region)
        self.user = self.assign('can_edit_questionnaire', self.user)

    def test_post_deletes_section_that_belongs_to_your_region(self):
        client = Client()
        client.login(username=self.user.username, password='pass')
        url = '/section/%s/delete/' % self.section.id
        referer_url = '/questionnaire/entry/%d/section/%d/' % (self.questionnaire.id, self.section.id)
        response = client.post(url, HTTP_REFERER=referer_url)
        self.assertRedirects(response, expected_url=self.questionnaire.absolute_url())
        self.assertRaises(Section.DoesNotExist, Section.objects.get, id=self.section.id)

    def test_post_delete_section_spares_section_thats_not_for_your_region(self):
        client = Client()
        user_not_in_same_region, country, region = self.create_user_with_no_permissions(username="asian_chic",
                                                  country_name="China", region_name="ASEAN")
        self.assign('can_edit_questionnaire', self.user)
        client.login(username=user_not_in_same_region.username, password='pass')

        paho = Region.objects.create(name="paho")
        section = Section.objects.create(name="section", questionnaire=self.questionnaire, order=1, region=paho)

        url = '/section/%s/delete/' % section.id
        self.assert_permission_required(url)

        response = client.post(url)
        self.failUnless(Section.objects.filter(id=section.id))
        self.assertRedirects(response, expected_url='/accounts/login/?next=%s' % quote(url))


class RegionalSubSectionsViewTest(BaseTest):

    def setUp(self):
        self.user, self.country, self.region = self.create_user_with_no_permissions()
        self.questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English", year=2013, region=self.region)
        self.section = Section.objects.create(name="section", questionnaire=self.questionnaire, order=1, region=self.region)
        self.section1 = Section.objects.create(name="section1", questionnaire=self.questionnaire, order=2, region=self.region)
        self.subsection = SubSection.objects.create(title="subsection 1", section=self.section, order=1, region=self.region)
        self.user = self.assign('can_edit_questionnaire', self.user)

    def test_post_deletes_section_that_belongs_to_your_region(self):
        client = Client()
        client.login(username=self.user.username, password='pass')
        url = '/subsection/%s/delete/' % self.subsection.id
        referer_url = '/questionnaire/entry/%d/section/%d/' % (self.questionnaire.id, self.section.id)
        response = client.post(url, HTTP_REFERER=referer_url)
        self.assertRaises(SubSection.DoesNotExist, SubSection.objects.get, id=self.section.id)
        self.assertRedirects(response, expected_url=self.questionnaire.absolute_url())

    def test_post_delete_section_spares_section_thats_not_for_your_region(self):
        client = Client()
        user_not_in_same_region, country, region = self.create_user_with_no_permissions(username="asian_chic",
                                                  country_name="China", region_name="ASEAN")
        self.assign('can_edit_questionnaire', self.user)
        client.login(username=user_not_in_same_region.username, password='pass')

        section = Section.objects.create(name="section", questionnaire=self.questionnaire, order=1, region=self.region)
        subsection = SubSection.objects.create(title="subsection 1", section=section, order=1, region=self.region)

        url = '/subsection/%s/delete/' % subsection.id
        self.assert_permission_required(url)

        response = client.post(url)
        self.failUnless(SubSection.objects.filter(id=subsection.id))
        self.assertRedirects(response, expected_url='/accounts/login/?next=%s' % quote(url))