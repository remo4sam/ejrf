from urllib import quote

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
        self.url = "/manage/region/%d/" % (self.region.id)

    def test_get_returns_region_specific_questionnaires(self):
        finalized_questionnaire = Questionnaire.objects.create(name="JRF Jamaica core", description="bla", year=2012,
                                             status=Questionnaire.FINALIZED, region=self.region)
        draft_questionnaire = Questionnaire.objects.create(name="JRF Jamaica core", description="bla", year=2011,
                                             status=Questionnaire.DRAFT, region=self.region)
        Section.objects.create(title="section", order=1, questionnaire=finalized_questionnaire, name="section", region=self.region)
        Section.objects.create(title="section", order=1, questionnaire=draft_questionnaire, name="section", region=self.region)

        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
        templates = [template.name for template in response.templates]
        self.assertIn('home/regional/index.html', templates)
        self.assertIn(finalized_questionnaire, response.context['finalized_questionnaires'])
        self.assertIn(draft_questionnaire, response.context['draft_questionnaires'])
        self.assertEqual(self.region, response.context['region'])

    def test_permission_required_for_create_section(self):
        self.assert_permission_required(self.url)

        user_not_in_same_region, country, region = self.create_user_with_no_permissions(username="asian_chic", country_name="China", region_name="ASEAN")
        self.assign('can_edit_questionnaire', user_not_in_same_region)

        self.client.logout()
        self.client.login(username='asian_chic', password='pass')
        response = self.client.get(self.url)
        self.assertRedirects(response, expected_url='/accounts/login/?next=%s' % quote(self.url),
                             status_code=302, target_status_code=200, msg_prefix='')