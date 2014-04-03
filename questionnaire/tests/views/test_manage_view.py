from django.core.urlresolvers import reverse
from django.test import Client
from questionnaire.forms.questionnaires import QuestionnaireFilterForm, PublishQuestionnaireForm
from questionnaire.models import Questionnaire, Section, Organization, Region
from questionnaire.tests.base_test import BaseTest


class ManageJRFViewTest(BaseTest):

    def setUp(self):
        self.client = Client()
        self.user, self.country, self.region = self.create_user_with_no_permissions()
        self.who = Organization.objects.create(name="WHO")
        self.unicef = Organization.objects.create(name="UNICEF")
        self.paho = Region.objects.create(name="The Paho", organization=self.who)
        self.pacific = Region.objects.create(name="haha", organization=self.who)
        self.assign('can_view_users', self.user)
        self.client.login(username=self.user.username, password='pass')

    def test_get_returns_only_core_and_region_specific_questionnaires(self):
        core1 = Questionnaire.objects.create(name="JRF Jamaica core", description="bla", year=2012,
                                             status=Questionnaire.FINALIZED)
        core1_publish = Questionnaire.objects.create(name="JRF Jamaica core", description="bla", year=2011,
                                             status=Questionnaire.PUBLISHED)
        core2 = Questionnaire.objects.create(name="JRF Brazil core", description="bla", year=2013,
                                             status=Questionnaire.DRAFT)
        questionnaire1 = Questionnaire.objects.create(name="JRF Jamaica paho", description="bla", year=2012,
                                                      status=Questionnaire.FINALIZED, region=self.paho)
        questionnaire2 = Questionnaire.objects.create(name="JRF Brazil Paho", description="bla", year=2013,
                                                      status=Questionnaire.DRAFT, region=self.paho)
        Section.objects.create(title="section", order=1, questionnaire=core2, name="section")
        Section.objects.create(title="section", order=1, questionnaire=core1, name="section")
        Section.objects.create(title="section", order=1, questionnaire=questionnaire1, name="section")
        Section.objects.create(title="section", order=1, questionnaire=questionnaire2, name="section")
        Section.objects.create(title="section", order=1, questionnaire=core1_publish, name="section")

        response = self.client.get("/manage/")
        self.assertEqual(200, response.status_code)
        templates = [template.name for template in response.templates]
        self.assertIn('home/global/index.html', templates)
        self.assertIn(core1, response.context['finalized_questionnaires'])
        self.assertIn(core1_publish, response.context['finalized_questionnaires'])
        self.assertIn(core2, response.context['draft_questionnaires'])
        self.assertIsInstance(response.context['filter_form'], QuestionnaireFilterForm)
        self.assertEqual(reverse('duplicate_questionnaire_page'), response.context['action'])

        question_map = response.context['regions_questionnaire_map']
        self.assertEqual(questionnaire2, question_map[self.paho]['drafts'][0])
        self.assertEqual(questionnaire1, question_map[self.paho]['finalized'][0])

        self.assertEqual(0, len(question_map[self.pacific]['drafts']))
        self.assertEqual(0, len(question_map[self.pacific]['finalized']))

    def test_permission_reguired(self):
        self.assert_permission_required("/manage/")


class FinalizeQuestionnaireViewTest(BaseTest):

    def setUp(self):
        self.client = Client()
        self.user, self.country, self.region = self.create_user_with_no_permissions()
        self.assign('can_view_users', self.user)

        self.client.login(username=self.user.username, password='pass')

        self.questionnaire = Questionnaire.objects.create(name="JRF Brazil", description="bla", year=2013, status=Questionnaire.DRAFT)
        Section.objects.create(title="Cured Cases of Measles", order=1, questionnaire=self.questionnaire, name="Cured Cases")
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
        questionnaire = Questionnaire.objects.create(name="JRF Brazil", description="bla", year=2013, status=Questionnaire.FINALIZED)
        section = Section.objects.create(name="haha", questionnaire=questionnaire, order=1)
        url = '/questionnaire/%d/unfinalize/' % questionnaire.id
        response = self.client.post(url, HTTP_REFERER=referer_url)
        self.assertNotIn(questionnaire, Questionnaire.objects.filter(status=Questionnaire.FINALIZED).all())
        self.assertEqual(Questionnaire.DRAFT, Questionnaire.objects.get(id=questionnaire.id).status)
        self.assertRedirects(response, referer_url)

    def test_post_shows_error_message_when_attempting_to_unfinalize_published_questionnaire(self):
        questionnaire = Questionnaire.objects.create(name="JRF Brazil", description="bla", year=2013, status=Questionnaire.PUBLISHED)
        Section.objects.create(title="Cured Cases of Measles", order=1, questionnaire=questionnaire, name="Cured Cases")
        url = '/questionnaire/%d/unfinalize/' % questionnaire.id
        response = self.client.post(url)
        self.assertRedirects(response, reverse('manage_jrf_page'))
        message = "The questionnaire could not be unlocked because its published."
        self.assertIn(message, response.cookies['messages'].value)

    def test_permission_reguired(self):
        self.assert_permission_required("/manage/")


class PublishQuestionnaireToRegionsViewTest(BaseTest):

    def setUp(self):
        self.client = Client()
        self.user, self.country, self.region = self.create_user_with_no_permissions()
        self.assign('can_view_users', self.user)
        self.client.login(username=self.user.username, password='pass')

        self.questionnaire = Questionnaire.objects.create(name="JRF Brazil", description="bla", year=2013, status=Questionnaire.FINALIZED)
        Section.objects.create(title="Cured Cases of Measles", order=1, questionnaire=self.questionnaire, name="Cured Cases")

        self.url = '/questionnaire/%d/publish/' % self.questionnaire.id
        self.who = Organization.objects.create(name="WHO")
        self.unicef = Organization.objects.create(name="UNICEF")
        self.australia = Region.objects.create(name="Australia", organization=self.who)

    def test_post_publishes_questionnaire(self):
        afro = Region.objects.create(name="The Afro", organization=self.who)
        paho = Region.objects.create(name="The Paho", organization=self.who)
        pacific = Region.objects.create(name="haha", organization=self.who)
        asia = Region.objects.create(name="hehe", organization=self.who)
        questionnaire = Questionnaire.objects.create(name="JRF Brazil", description="bla", year=2013, status=Questionnaire.FINALIZED, region=afro)
        Section.objects.create(title="Cured Cases of Measles", order=1, questionnaire=questionnaire, name="Cured Cases")
        Region.objects.create(name="UNICEF ASIA", organization=self.unicef)

        data = {'regions': [paho.id, pacific.id, asia.id,]}

        response = self.client.post(self.url, data=data)
        self.assertRedirects(response, reverse('manage_jrf_page'))
        message = "The questionnaire has been published to %s, %s, %s" % (paho.name, pacific.name, asia.name)
        self.assertIn(message, response.cookies['messages'].value)
        questionnaires = Questionnaire.objects.filter(year=self.questionnaire.year)
        self.assertEqual(5, questionnaires.count())
        [self.assertEqual(1, region.questionnaire.all().count()) for region in [paho, pacific, asia]]
        self.assertEqual(1, afro.questionnaire.all().count())

    def test_post_publishes_questionnaire_with_errors(self):
        data = {'regions': []}
        response = self.client.post(self.url, data=data)
        self.assertEqual(200, response.status_code)
        message = "Questionnaire could not be published see errors below"
        self.assertIn(message, str(response.content))

    def test_get_publish(self):
        response = self.client.get("/questionnaire/%d/publish/" % self.questionnaire.id)
        self.assertEqual(200, response.status_code)
        templates = [template.name for template in response.templates]
        self.assertIn('questionnaires/_publish.html', templates)
        self.assertEqual(self.questionnaire, response.context['questionnaire'])
        self.assertIsInstance(response.context['publish_form'], PublishQuestionnaireForm)
        self.assertEqual("Publish", response.context['btn_label'])
        self.assertEqual(reverse("manage_jrf_page"), response.context['cancel_url'])

    def test_permission_reguired(self):
        self.assert_permission_required("/manage/")


class ApproveQuestionnaireToDataSubmittersViewTest(BaseTest):

    def setUp(self):
        self.client = Client()
        self.user, self.country, self.region = self.create_user_with_no_permissions()
        self.assign('can_view_users', self.user)
        self.client.login(username=self.user.username, password='pass')

        self.questionnaire = Questionnaire.objects.create(name="JRF Brazil", description="bla", year=2013, status=Questionnaire.FINALIZED, region=self.region)
        Section.objects.create(title="Cured Cases of Measles", order=1, questionnaire=self.questionnaire, name="Cured Cases")

        self.url = '/questionnaire/%d/approve/' % self.questionnaire.id
        self.who = Organization.objects.create(name="WHO")
        self.unicef = Organization.objects.create(name="UNICEF")
        self.australia = Region.objects.create(name="Australia", organization=self.who)

    def test_post_approves_questionnaire(self):
        referer_url = reverse('manage_jrf_page',)
        self.assign('can_view_users', self.user)
        response = self.client.post(self.url, HTTP_REFERER=referer_url)
        self.assertNotIn(self.questionnaire, Questionnaire.objects.filter(status=Questionnaire.FINALIZED, region=self.region).all())
        self.assertIn(self.questionnaire, Questionnaire.objects.filter(status=Questionnaire.PUBLISHED, region=self.region).all())
        self.assertRedirects(response, referer_url)

    def test_get_approve_questionnaire(self):
        referer_url = reverse('manage_jrf_page',)
        response = self.client.get(self.url, HTTP_REFERER=referer_url)
        self.assertEqual(200, response.status_code)
        self.assertEqual(self.questionnaire, response.context['questionnaire'])
        self.assertEqual("/manage/", response.context['cancel_url'])
        self.assertEqual("Approve", response.context['btn_label'])

    def test_permission_reguired(self):
        self.assert_permission_required("/manage/")