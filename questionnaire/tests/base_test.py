import csv
from django.contrib.auth.models import User, Permission, Group
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from urllib import quote
from questionnaire.models import Country, UserProfile, Region


class BaseTest(TestCase):

    def write_to_csv(self, mode, data, csvfilename='test.csv'):
        with open(csvfilename, mode) as fp:
            _file = csv.writer(fp, delimiter=',')
            _file.writerows(data)
            fp.close()

    def create_user_with_no_permissions(self, username=None, country_name="Uganda", region_name="Afro"):
        username = username if username else "user"
        user = User.objects.create(username=username, email="user@mail.com")
        uganda = Country.objects.create(name=country_name)
        region = None
        if region_name:
            region = Region.objects.create(name=region_name)
            region.countries.add(uganda)
        UserProfile.objects.create(user=user, country=uganda, region=region)
        user.set_password("pass")
        user.save()
        return user, uganda, region

    def login_user(self):
        self.client.login(username='user', password='pass')

    def assert_login_required(self, url):
        self.client.logout()
        response = self.client.get(url)
        self.assertRedirects(response, expected_url='/accounts/login/?next=%s' % quote(url),
                             status_code=302, target_status_code=200, msg_prefix='')

    def assign(self, permissions, user):
        auth_content = ContentType.objects.get_for_model(Permission)
        group = Group.objects.get_or_create(name="Group with %s permissions" % permissions)[0]
        permission, out = Permission.objects.get_or_create(codename=permissions, content_type=auth_content)
        group.permissions.add(permission)
        group.user_set.add(user)
        return user

    def assert_permission_required(self, url):
        self.client.logout()
        self.client.login(username='user_with_no_perms', password='pass')
        response = self.client.get(url)
        self.assertRedirects(response, expected_url='/accounts/login/?next=%s' % quote(url),
                             status_code=302, target_status_code=200, msg_prefix='')
