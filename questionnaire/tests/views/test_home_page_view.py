from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import Client
from questionnaire.models import Questionnaire, Section, Country, Region, Question, SubSection, QuestionGroup
from questionnaire.models.answers import AnswerStatus
from questionnaire.tests.base_test import BaseTest


class HomePageViewTest(BaseTest):

    def setUp(self):
        self.client = Client()
        self.user, self.country, self.region = self.create_user_with_no_permissions()
        self.assign('can_submit_responses', self.user)
        self.client.login(username=self.user.username, password='pass')

    def test_get(self):
        response = self.client.get("/")
        self.assertEqual(200, response.status_code)
        templates = [template.name for template in response.templates]
        self.assertIn('home/index.html', templates)

    def test_homepage_redirects_to_latest_published_questionnaire_logged_in_as_data_submitter(self):
        questionnaire = Questionnaire.objects.create(name="JRF", description="bla", status=Questionnaire.PUBLISHED, region=self.region)
        section = Section.objects.create(title="section", order=1, questionnaire=questionnaire, name="section")
        Section.objects.create(title="section", order=2, questionnaire=questionnaire, name="section")

        response = self.client.get("/")
        expected_url = "/questionnaire/entry/%d/section/%d/" % (questionnaire.id, section.id)
        self.assertRedirects(response, expected_url=expected_url)

    def test_homepage_doesnot__redirects_to_latest_questionnaire_that_is_not_published_logged_data_submitter(self):
        Questionnaire.objects.create(name="JRF", description="bla", status=Questionnaire.FINALIZED)
        response = self.client.get("/")
        self.assertEqual(200, response.status_code)
        templates = [template.name for template in response.templates]
        self.assertIn('home/index.html', templates)
        message = "Sorry, The JRF is not yet published at the moment"
        self.assertIn(message, str(response.content))

    def test_login_required_for_home_get(self):
        self.assert_login_required('/')

    def test_homepage_redirects_to_manage_regional_jrf_when_logged_in_as_regional_admin(self):
        User.objects.all().delete()
        self.client.logout()
        user, self.country, self.region = self.create_user_with_no_permissions()
        self.assign('can_edit_questionnaire', user)
        self.client.login(username=user.username, password='pass')
        response = self.client.get("/")
        self.assertRedirects(response, expected_url=reverse('manage_regional_jrf_page', args=(self.region.id,)))


class GlobalAdminHomePageViewTest(BaseTest):

    def setUp(self):
        self.client = Client()
        self.user, self.country, self.region = self.create_user_with_no_permissions()
        self.assign('can_view_users', self.user)
        self.assign('can_edit_users', self.user)
        self.client.login(username=self.user.username, password='pass')
        self.afro = Region.objects.create(name="Afro")
        self.uganda = Country.objects.create(name="Uganda", code="UGX")
        self.rwanda = Country.objects.create(name="Rwanda", code="RWA")
        self.afro.countries.add(self.uganda, self.rwanda)

    def test_get(self):
        response = self.client.get("/")
        self.assertEqual(200, response.status_code)
        templates = [template.name for template in response.templates]
        self.assertIn('home/index.html', templates)
        self.assertIn(self.uganda, response.context['region_country_status_map'][self.afro])
        self.assertIn(self.rwanda, response.context['region_country_status_map'][self.afro])

    def test_login_required_for_home_get(self):
        self.assert_login_required('/')