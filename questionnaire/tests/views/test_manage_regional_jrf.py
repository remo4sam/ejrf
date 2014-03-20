from urllib import quote
from django.core.urlresolvers import reverse
from django.test import Client
from questionnaire.models import Organization, Questionnaire, Section
from questionnaire.tests.base_test import BaseTest


class ManageJRFViewTest(BaseTest):
    def setUp(self):
        self.client = Client()
        self.user, self.country, self.region = self.create_user_with_no_permissions()
        self.who = Organization.objects.create(name="WHO")
        self.assign('can_edit_questionnaire', self.user)
        self.client.login(username=self.user.username, password='pass')
        self.url = "/manage/region/%d/" % self.region.id

    def test_get_returns_region_specific_questionnaires(self):
        finalized_questionnaire = Questionnaire.objects.create(name="JRF Jamaica core", description="bla", year=2012,
                                                               status=Questionnaire.FINALIZED, region=self.region)
        draft_questionnaire = Questionnaire.objects.create(name="JRF Jamaica core", description="bla", year=2011,
                                                           status=Questionnaire.DRAFT, region=self.region)
        Section.objects.create(title="section", order=1, questionnaire=finalized_questionnaire, name="section",
                               region=self.region)
        Section.objects.create(title="section", order=1, questionnaire=draft_questionnaire, name="section",
                               region=self.region)

        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
        templates = [template.name for template in response.templates]
        self.assertIn('home/regional/index.html', templates)
        self.assertIn(finalized_questionnaire, response.context['finalized_questionnaires'])
        self.assertIn(draft_questionnaire, response.context['draft_questionnaires'])
        self.assertEqual(self.region, response.context['region'])

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


class EditQuestionnaireNameViewTest(BaseTest):
    def setUp(self):
        self.client = Client()
        self.user, self.country, self.region = self.create_user_with_no_permissions()
        self.who = Organization.objects.create(name="WHO")
        self.assign('can_edit_questionnaire', self.user)
        self.assign('can_view_users', self.user)
        self.client.login(username=self.user.username, password='pass')
        self.questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English", year=2013, region=self.region)
        self.url = "/manage/questionnaire/%d/edit_name/" % self.questionnaire.id

    def test_post(self):
        data = {'name': 'Edit Name Of Questionnaire'}
        self.failIf(Questionnaire.objects.filter(**data))
        response = self.client.post(self.url, data=data)
        questionnaire = Questionnaire.objects.get(**data)
        self.failUnless(questionnaire)
        self.assertRedirects(response, expected_url='/manage/')
        self.assertIn('Name of Questionnaire updated successfully.', response.cookies['messages'].value)

    

class FinalizeRegionalQuestionnaireViewTest(BaseTest):
    def setUp(self):
        self.client = Client()
        self.user, self.country, self.region = self.create_user_with_no_permissions()
        self.assign('can_view_users', self.user)

        self.client.login(username=self.user.username, password='pass')

        self.questionnaire = Questionnaire.objects.create(name="JRF Brazil", description="bla", year=2013,
                                                          status=Questionnaire.DRAFT)
        Section.objects.create(title="Cured Cases of Measles", order=1, questionnaire=self.questionnaire,
                               name="Cured Cases")
        self.url = '/questionnaire/%d/finalize/' % self.questionnaire.id

    def test_post_finalizes_questionnaire(self):
        referer_url = reverse('manage_regional_jrf_page', args=(self.region.id,))
        self.assign('can_edit_questionnaire', self.user)
        response = self.client.post(self.url, HTTP_REFERER=referer_url)
        self.assertNotIn(self.questionnaire, Questionnaire.objects.filter(status=Questionnaire.DRAFT).all())
        self.assertIn(self.questionnaire, Questionnaire.objects.filter(status=Questionnaire.FINALIZED).all())
        self.assertRedirects(response, referer_url)

    def test_post_unfinalizes_questionnaire(self):
        referer_url = reverse('manage_regional_jrf_page', args=(self.region.id,))
        self.assign('can_edit_questionnaire', self.user)
        questionnaire = Questionnaire.objects.create(name="JRF Brazil", description="bla", year=2013,
                                                     status=Questionnaire.FINALIZED)
        section = Section.objects.create(name="haha", questionnaire=questionnaire, order=1)
        url = '/questionnaire/%d/unfinalize/' % questionnaire.id
        response = self.client.post(url, HTTP_REFERER=referer_url)
        self.assertNotIn(questionnaire, Questionnaire.objects.filter(status=Questionnaire.FINALIZED).all())
        self.assertEqual(Questionnaire.DRAFT, Questionnaire.objects.get(id=questionnaire.id).status)
        self.assertRedirects(response, referer_url)

    def test_post_unfinalize_a_published_a_questionnaire_returns_errors(self):
        referer_url = reverse('manage_regional_jrf_page', args=(self.region.id,))
        self.assign('can_edit_questionnaire', self.user)
        questionnaire = Questionnaire.objects.create(name="JRF Brazil", description="bla", year=2013,
                                                     status=Questionnaire.PUBLISHED)
        Section.objects.create(name="haha", questionnaire=questionnaire, order=1)
        url = '/questionnaire/%d/unfinalize/' % questionnaire.id
        response = self.client.post(url, HTTP_REFERER=referer_url)
        self.assertIn(questionnaire, Questionnaire.objects.filter(status=Questionnaire.PUBLISHED).all())
        self.assertEqual(Questionnaire.PUBLISHED, Questionnaire.objects.get(id=questionnaire.id).status)
        self.assertRedirects(response, referer_url)
        message = "The questionnaire could not be unlocked because its published."
        self.assertIn(message, response.cookies['messages'].value)


