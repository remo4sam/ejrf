from django.contrib.auth.models import User, Group, Permission
from questionnaire.forms.user_profile import UserProfileForm, EditUserProfileForm
from questionnaire.models import Country, Region, UserProfile, Organization
from questionnaire.tests.base_test import BaseTest


class UserProfileFormTest(BaseTest):
    def setUp(self):
        self.region = Region.objects.create(name="Afro")
        self.uganda = Country.objects.create(name="uganda", code="UGX")
        self.global_admin = Group.objects.create(name='Global Admin')
        self.organization = Organization.objects.create(name="UNICEF")

        self.region.countries.add(self.uganda)
        self.form_data = {
            'username': 'user',
            'password1': 'kant',
            'password2': 'kant',
            'email': 'raj@ni.kant',
            'country': self.uganda.id,
            'region': self.region.id,
            'organization': self.organization.id,
            'groups': self.global_admin.id
        }

    def test_valid(self):
        user_profile_form = UserProfileForm(self.form_data)
        self.assertTrue(user_profile_form.is_valid())
        user = user_profile_form.save()
        saved_user = User.objects.get(username='user')
        self.failUnless(saved_user.id)
        self.assertEqual(1, len(saved_user.groups.all()))
        self.assertIn(self.global_admin, saved_user.groups.all())

        user_profile = UserProfile.objects.filter(user=user)
        self.failUnless(user_profile)
        self.assertEqual(user_profile[0].region, self.region)
        self.assertEqual(user_profile[0].country, self.uganda)
        self.assertEqual(user_profile[0].organization, self.organization)

    def test_email_already_used(self):
        form_data = self.form_data
        User.objects.create(email=form_data['email'])

        user_form = UserProfileForm(form_data)
        self.assertFalse(user_form.is_valid())
        message = "%s is already associated to a different user." % form_data['email']
        self.assertEquals(user_form.errors['email'], [message])

    def test_clean_username_no_duplicates_on_create(self):
        form_data = self.form_data
        User.objects.create(username=form_data['username'])
        user_form = UserProfileForm(form_data)
        self.assertFalse(user_form.is_valid())
        message = "%s is already associated to a different user." % form_data['username']
        self.assertEquals(user_form.errors['username'], [message])

    def test_clean_confirm_password(self):
        form_data = self.form_data
        form_data['password2'] = 'tank'
        user_form = UserProfileForm(form_data)
        self.assertFalse(user_form.is_valid())
        message = "The two password fields didn't match."
        self.assertEquals(user_form.errors['password2'], [message])

        form_data['password2'] = form_data['password1']
        user_form = UserProfileForm(form_data)
        self.assertTrue(user_form.is_valid())

    def test_country_must_belong_to_selected_region(self):
        sudan = Country.objects.create(name="Sudan", code="SDX")
        form_data = self.form_data.copy()
        form_data['country'] = sudan.id
        user_form = UserProfileForm(form_data)
        self.assertFalse(user_form.is_valid())
        message = "%s does not belong to region %s" % (sudan.name, self.region.name)
        self.assertEquals(user_form.errors['country'], [message])

    def test_valid_when_region_is_blank(self):
        form_data = self.form_data.copy()
        form_data['country'] = ''
        form_data['region'] = ''
        user_form = UserProfileForm(form_data)
        self.assertTrue(user_form.is_valid())

    def test_groups_required(self):
        form_data = self.form_data.copy()
        form_data['groups'] = ''
        user_form = UserProfileForm(form_data)
        self.assertFalse(user_form.is_valid())
        message = "This field is required."
        self.assertEquals(user_form.errors['groups'], [message])


class EditUserProfileFormTest(BaseTest):
    def setUp(self):
        self.region = Region.objects.create(name="Afro")
        self.uganda = Country.objects.create(name="uganda", code="UGX")
        self.global_admin = Group.objects.create(name='Global Admin')
        self.organization = Organization.objects.create(name="UNICEF")

        self.saved_user = User.objects.create(username='user1', email='test@unicef.com')
        self.user_profile = UserProfile.objects.create(user=self.saved_user, region=self.region, country=self.uganda,
                                                  organization=self.organization)
        self.global_admin.user_set.add(self.saved_user)

        self.region.countries.add(self.uganda)
        self.form_data = {
            'username': 'user',
            'email': 'raj@ni.kant', }

    def test_valid(self):
        edit_user_profile_form = EditUserProfileForm(instance=self.saved_user, data=self.form_data)
        user = edit_user_profile_form.save()

        self.assertTrue(edit_user_profile_form.is_valid())
        self.failUnless(self.saved_user.id)
        self.assertEqual(1, len(self.saved_user.groups.all()))
        self.assertIn(self.global_admin, self.saved_user.groups.all())

        user_profile = UserProfile.objects.get(user=user)
        self.failUnless(user_profile)
        self.assertEqual(self.organization, user_profile.organization)
        self.assertEqual(self.region, user_profile.region)
        self.assertEqual(self.uganda, user_profile.country)

    def test_username_already_used(self):
        another_user = User.objects.create(username='another_user', email='another_user@unicef.com')
        user_profile = UserProfile.objects.create(user=another_user, region=self.region, country=self.uganda,
                                                  organization=self.organization)
        self.global_admin.user_set.add(another_user)

        form_data = {
            'username': 'another_user',
            'email': 'test@unicef.com' }
        edit_user_profile_form = EditUserProfileForm(instance=self.saved_user, data=form_data)
        self.assertFalse(edit_user_profile_form.is_valid())
        message = "%s is already associated to a different user." % form_data['username']
        self.assertEquals(edit_user_profile_form.errors['username'], [message])

    def test_email_already_used(self):
        another_user = User.objects.create(username='another_user', email='another_user@unicef.com')
        user_profile = UserProfile.objects.create(user=another_user, region=self.region, country=self.uganda,
                                                  organization=self.organization)
        self.global_admin.user_set.add(another_user)

        form_data = {
            'username': 'user1',
            'email': 'another_user@unicef.com' }
        edit_user_profile_form = EditUserProfileForm(instance=self.saved_user, data=form_data)
        self.assertFalse(edit_user_profile_form.is_valid())
        message = "%s is already associated to a different user." % form_data['email']
        self.assertEquals(edit_user_profile_form.errors['email'], [message])
