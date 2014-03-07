from django.contrib.auth.models import Group
from questionnaire.forms.filter import UserFilterForm
from questionnaire.models import Region, Organization
from questionnaire.tests.base_test import BaseTest


class UserProfileFormTest(BaseTest):

    def setUp(self):
        self.region = Region.objects.create(name="Afro")
        self.organization = Organization.objects.create(name="UNICEF")
        self.global_admin = Group.objects.create(name="UNICEF")
        self.form_data = {
            'organization': self.organization.id,
            'region': self.region.id,
            'role': self.global_admin.id,
        }

    def test_valid(self):
        user_filter = UserFilterForm(self.form_data)
        self.assertTrue(user_filter.is_valid())

    def test_valid_when_organization_is_blank(self):
        form_data = self.form_data.copy()
        form_data['organization'] = ''
        user_filter = UserFilterForm(form_data)
        self.assertTrue(user_filter.is_valid())

    def test_valid_when_region_is_blank(self):
        form_data = self.form_data.copy()
        form_data['region'] = ''
        user_filter = UserFilterForm(form_data)
        self.assertTrue(user_filter.is_valid())

    def test_valid_when_role_is_blank(self):
        form_data = self.form_data.copy()
        form_data['role'] = ''
        user_filter = UserFilterForm(form_data)
        self.assertTrue(user_filter.is_valid())