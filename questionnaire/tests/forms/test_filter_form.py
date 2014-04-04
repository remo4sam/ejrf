from datetime import date
from django.contrib.auth.models import Group

from questionnaire.forms.filter import UserFilterForm, ExportFilterForm
from questionnaire.models import Region, Organization, Country, Theme, Questionnaire
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


class ExportFilterFormTest(BaseTest):

    def setUp(self):
        self.afro = Region.objects.create(name="Afro")
        self.uganda = Country.objects.create(name="Uganda", code="UGX")
        self.kenya = Country.objects.create(name="Kenya", code="KY")
        self.theme = Theme.objects.create(name="some theme", region=self.afro)
        self.questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English", year=2013)
        self.afro.countries.add(self.kenya, self.uganda)

        self.form_data = {
            'themes': [self.theme.id],
            'year': [self.questionnaire.year],
            'regions': [self.afro.id],
            'countries': [self.uganda.id, self.kenya.id],
        }

    def test_valid(self):
        export_filter = ExportFilterForm(self.form_data)
        self.assertTrue(export_filter.is_valid())

    def test_valid_when_themes_are_blank(self):
        form_data = self.form_data.copy()
        form_data['themes'] = ''
        export_filter = ExportFilterForm(form_data)
        self.assertTrue(export_filter.is_valid())

    def test_valid_when_region_is_blank(self):
        form_data = self.form_data.copy()
        form_data['regions'] = ''
        export_filter = ExportFilterForm(form_data)
        self.assertTrue(export_filter.is_valid())

    def test_valid_when_countries_is_blank(self):
        form_data = self.form_data.copy()
        form_data['countries'] = ''
        export_filter = ExportFilterForm(form_data)
        self.assertTrue(export_filter.is_valid())

    def test_valid_when_year_is_blank(self):
        form_data = self.form_data.copy()
        form_data['year'] = ''
        export_filter = ExportFilterForm(form_data)
        self.assertTrue(export_filter.is_valid())

    def test_invalid_when_if_year_is_does_not_have_questionnaire(self):
        form_data = self.form_data.copy()
        selected_year = date.today().year
        form_data['year'] = [selected_year]
        export_filter = ExportFilterForm(form_data)
        self.assertFalse(export_filter.is_valid())
        error_message = "Select a valid choice. %d is not one of the available choices." % selected_year
        self.assertIn(error_message, export_filter.errors['year'])