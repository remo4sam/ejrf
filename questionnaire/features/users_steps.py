from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from lettuce import step, world
from questionnaire.features.pages.extract import ExtractPage
from questionnaire.features.pages.home import HomePage
from questionnaire.features.pages.step_utils import create_user_with_no_permissions, assign
from questionnaire.features.pages.users import LoginPage, UserListingPage, CreateUserPage
from questionnaire.models import Region, Country, UserProfile, Organization


@step(u'Given I am registered user')
def given_i_am_registered_user(step):
    world.user, world.uganda, world.region = create_user_with_no_permissions(username="Cool")
    assign('can_submit_responses', world.user)

@step(u'And I visit the login page')
def and_i_visit_the_login_page(step):
    world.page = LoginPage(world.browser)
    world.page.visit()

@step(u'And I fill in the login credentials')
def and_i_fill_in_the_login_credentials(step):
    data = {'username': world.user.username,
            'password': "pass"}
    world.page.fill_form(data)

@step(u'And I submit the form')
def and_i_submit_the_form(step):
    world.page.submit()

@step(u'Then I should be redirected home page')
def then_i_should_be_redirected_dashboard(step):
    world.page = HomePage(world.browser)
    world.page.validate_url()
    world.page.is_text_present("Electronic Joint Reporting Form")

@step(u'And I should see my username and the logout link')
def and_i_should_see_my_username_and_the_logout_link(step):
    world.page.is_text_present(world.user.get_username(), "Logout")

@step(u'Given I visit the login page')
def given_i_visit_the_login_page(step):
    world.page = LoginPage(world.browser)
    world.page.visit()

@step(u'And I fill in invalid user credentials')
def and_i_fill_in_invalid_user_credentials(step):
    data = {'username': "invalid username",
            'password': "pass"}
    world.page.fill_form(data)

@step(u'Then I should see an error message')
def then_i_should_see_an_error_message(step):
    world.page.is_text_present("Please enter a correct username and password.")

@step(u'When I click the logout link')
def when_i_click_the_logout_link(step):
    world.page.click_link_by_partial_href("/accounts/logout/")


@step(u'Then I should see the login page again')
def then_i_should_see_the_login_page_again(step):
    world.page = LoginPage(world.browser)
    world.page.validate_url()

@step(u'Given I visit the extract page')
def given_i_visit_the_extract_page(step):
    world.page = ExtractPage(world.browser)
    world.page.visit()

@step(u'When I fill in the login credentials')
def when_i_fill_in_the_login_credentials(step):
    world.page = LoginPage(world.browser)
    data = {'username': world.user.username,
            'password': "pass"}
    world.page.fill_form(data)

@step(u'Then I should see the extract page')
def then_i_should_see_the_extract_page(step):
    world.page = ExtractPage(world.browser)

@step(u'Given I have a global admin user')
def given_i_have_a_global_admin_user(step):
    world.user = User.objects.create(username='user1', email='rajni@kant.com')
    world.user.set_password('pass')
    world.user.save()
    world.global_admin = Group.objects.create(name='Global Admin')
    auth_content = ContentType.objects.get_for_model(Permission)
    permission, out = Permission.objects.get_or_create(codename='can_view_users', content_type=auth_content)
    world.global_admin.permissions.add(permission)
    world.global_admin.user_set.add(world.user)

@step(u'And I have 100 other users')
def and_i_have_100_other_users(step):
    for i in range(0, 100):
        User.objects.create(username='Rajni%s' % str(i), email='rajni@kant%s.com' % str(i), password='I_Rock')

@step(u'And I visit the user listing page')
def and_i_visit_the_user_listing_page(step):
    world.page = UserListingPage(world.browser)
    world.page.visit()

@step(u'Then I should see the list of users paginated')
def then_i_should_see_the_list_of_users_paginated(step):
    world.page.validate_user_list_headers()
    world.page.validate_pagination()

@step(u'And I click an new user button')
def and_i_click_an_new_user_button(step):
    world.page.click_by_css("#add-new-user")
    world.page = CreateUserPage(world.browser)

@step(u'And I fill in the user information')
def and_i_fill_in_the_user_information(step):
    world.form_data = {
        'username': 'rajni',
        'password1': 'kant',
        'password2': 'kant',
        'email': 'raj@ni.kant'}
    world.page.fill_form(world.form_data)

@step(u'And I select global admin role')
def and_i_select_global_admin_role(step):
    world.page.check(world.global_admin.id)

@step(u'Then I should see that the user was successfully created')
def then_i_should_see_that_the_user_was_successfully_created(step):
    world.page.is_text_present("%s created successfully." % world.global_admin.name)

@step(u'And I should see the user listed on the listing page')
def and_i_should_see_the_user_listed_on_the_listing_page(step):
    world.page.is_text_present(world.form_data['username'], world.form_data['email'], world.global_admin.name)

@step(u'And I have a region, in an organization')
def and_i_have_a_region(step):
    world.afro_region = Region.objects.create(name="Afro")
    world.uganda = Country.objects.create(name="Afro", code="COD")
    world.afro_region.countries.add(world.uganda)

@step(u'And I have 10 users in one of the regions')
def and_i_have_10_users_in_one_region(step):
    for i in range(0, 10):
        world.user = User.objects.create(username='Rajni%s' % str(i), email='rajni@kant%s.com' % str(i), password='I_Rock')
        world.country = Country.objects.create(name="Country%s" % str(i), code="UGX")
        world.afro_region.countries.add(world.country)
        UserProfile.objects.create(user=world.user, country=world.country, region=world.afro_region)

@step(u'And I have five others not in that region')
def and_i_have_five_others_not_in_that_region(step):
    region = Region.objects.create(name="Afro")
    for i in range(11, 16):
        world.user = User.objects.create(username='Jacinta%s' % str(i), email='jacinta%s@gmail.com' % str(i), password='I_Rock')
        UserProfile.objects.create(user=world.user, region=region)


@step(u'And I select a region')
def and_i_select_a_region(step):
    world.page.select('region', world.afro_region.id)

@step(u'And I click get list')
def and_i_click_get_list(step):
    world.page.click_by_css("#get-list-btn")

@step(u'Then I should see only the users in that region')
def then_i_should_see_only_the_users_in_that_region(step):
    for i in range(0, 2):
        world.page.is_text_present('Rajni%s' % str(i), 'rajni@kant%s.com' % str(i))

    for i in range(11, 13):
        world.page.is_text_present('Jacinta%s' % str(i), 'jacinta%s@gmail.com' % str(i), status=False)

@step(u'And I select regional admin role')
def and_i_select_regional_admin_role(step):
    world.page.check(world.regional_admin.id)

@step(u'Then I should see only region and country fields')
def then_i_should_see_only_region_and_country_fields(step):
    world.page.is_text_present("Region", "Organization")
    world.page.validate_only_organization_and_region_drop_down_visible()

@step(u'And I select the region for the new user')
def when_i_select_the_country_and_region_for_the_new_user(step):
    world.page.select('region', world.afro_region.id)

@step(u'And I have roles')
def and_i_have_roles(step):
    world.regional_admin = Group.objects.create(name='Regional Admin')
    world.country_admin = Group.objects.create(name='Country Admin')
    world.data_submitter = Group.objects.create(name='Data Submitter')

@step(u'Then I should see that the data regional admin was successfully created')
def then_i_should_see_that_the_data_regional_admin_was_successfully_created(step):
    world.page.is_text_present("%s created successfully." % world.regional_admin.name)

@step(u'And I have two organizations, region and role')
def and_i_have_an_organization_region_and_role(step):
    world.organization = Organization.objects.create(name="UNICEF")
    world.who_organization = Organization.objects.create(name="WHO")
    world.region = Region.objects.create(name="Afro", organization=world.organization)
    world.paho = Region.objects.create(name="PAHO", organization=world.who_organization)
    world.global_admin = Group.objects.create(name="Global")
    world.regional_admin = Group.objects.create(name="Regional")

@step(u'And I have 4 users in the UNICEF organization, 2 of which are regional admins in the AFRO region')
def and_i_have_4_users_in_the_unicef_organization(step):
    for i in range(0, 4):
        world.jacinta = User.objects.create(username="jacinta%s" % str(i), email='jacinta%s@gmail.com' % str(i))
        UserProfile.objects.create(user=world.jacinta, region=world.region, organization=world.organization)
        if i < 2:
            world.regional_admin.user_set.add(world.jacinta)

@step(u'And I have 2 users in the WHO organization')
def and_i_have_2_users_in_the_who_organization(step):
    for i in range(5, 7):
        world.jacinta = User.objects.create(username="jacinta%s" % str(i))
        UserProfile.objects.create(user=world.jacinta, region=world.region, organization=world.who_organization)

@step(u'Then I should see only regional admin users in the UNICEF organization in the AFRO region')
def then_i_should_see_only_regional_admin_users_in_the_unicef_organization_in_the_afro_region(step):
    for i in range(0, 2):
        world.page.is_text_present('jacinta%s' % str(i), 'jacinta%s@gmail.com' % str(i))

@step(u'And I should not see the rest of the users')
def and_i_should_not_see_the_rest_of_the_users(step):
    for i in range(4, 7):
        world.page.is_text_present('jacinta%s' % str(i), 'jacinta%s@gmail.com' % str(i), status=False)

@step(u'And I select unicef')
def and_i_select_unicef(step):
    world.page.select('organization', world.organization.id)

@step(u'Then I should see the region under unicef in the select')
def then_i_should_see_the_region_under_unicef_in_the_select(step):
    world.page.select('region', world.region.id)

@step(u'And I should not see the region under who in the select')
def and_i_should_not_see_the_region_under_who_in_the_select(step):
    world.page.validate_select_not_present(world.paho.name)

@step(u'And I have two organizations and regions')
def and_i_have_two_organizations_and_regions(step):
    world.unicef = Organization.objects.create(name="UNICEF")
    world.who = Organization.objects.create(name="WHO")
    world.region = Region.objects.create(name="Afro", organization=world.unicef)
    world.paho = Region.objects.create(name="PAHO", organization=world.who)

@step(u'And I have four roles')
def and_i_have_four_roles(step):
    world.regional_admin = Group.objects.create(name="Regional Admin")
    world.country_admin = Group.objects.create(name="Country Admin")
    world.data_submitter = Group.objects.create(name="Data Submitter")

@step(u'When I select the global admin role')
def when_i_select_the_global_admin_role(step):
    world.page.check(world.global_admin.id)

@step(u'Then I should see organisations drop down')
def then_i_should_see_organisations_drop_down(step):
    world.page.validate_only_organization_drop_down_visible()

@step(u'When I select the region admin role')
def when_i_select_the_region_admin_role(step):
    world.page.check(world.regional_admin.id)

@step(u'Then I should see region and country')
def then_i_should_see_region_and_country(step):
    world.page.validate_only_organization_and_region_drop_down_visible()

@step(u'When I select the country admin role')
def when_i_select_the_country_admin_role(step):
    world.page.check(world.country_admin.id)

@step(u'Then I should see country drop down')
def then_i_should_see_country_drop_down(step):
    world.page.validate_only_country_drop_down_visible()

@step(u'When I select the data submitter role')
def when_i_select_the_data_submitter_role(step):
    world.page.check(world.data_submitter.id)

@step(u'And I have a region')
def and_i_have_a_region(step):
    world.afro_region = Region.objects.create(name="Afro")
    world.uganda = Country.objects.create(name="Afro", code="COD")
    world.afro_region.countries.add(world.uganda)

@step(u'Then I should see only organization and region fields')
def then_i_should_see_only_organization_and_region_fields(step):
    world.page.validate_only_organization_and_region_drop_down_visible()

@step(u'And I have one region, in an organization')
def and_i_have_one_region_in_an_organization(step):
    world.unicef = Organization.objects.create(name="Unicef")
    world.afro_region = Region.objects.create(name="Afro")
    world.unicef.regions.add(world.afro_region)

@step(u'When I select the organization')
def when_i_select_the_organization(step):
    world.page.select('organization', world.unicef.id)

@step(u'When I select UNICEF organization')
def when_i_select_unicef_organization(step):
    world.page.select('organization', world.organization.id)

@step(u'And I select the AFRO region and regional admin role')
def and_i_select_the_afro_region_and_regional_admin_role(step):
    world.page.select('region', world.region.id)
    world.page.select('role', world.regional_admin.id)

@step(u'And I have a countries in that region')
def and_i_have_a_countries_in_that_region(step):
    world.uganda = Country.objects.create(name="Uganda")
    world.rwanda = Country.objects.create(name="Rwanda")
    world.afro_region.countries.add(world.uganda, world.rwanda)

@step(u'And I fill in data submitter information')
def and_i_fill_in_data_submitter_information(step):
    world.form_data = {
        'username': 'jacinta',
        'password1': 'pass',
        'password2': 'pass',
        'email': 'iacinta@ni.kant'}
    world.page.fill_form(world.form_data)

@step(u'And I select data submitter role')
def and_i_select_data_submitter_role(step):
    world.page.check(world.data_submitter.id)

@step(u'When I select a country')
def when_i_select_a_country(step):
    world.page.select('country', world.uganda.id)

@step(u'Then I should see that the data submitter was successfully created')
def then_i_should_see_that_the_data_submitter_was_successfully_created(step):
    world.page.is_text_present("%s created successfully." % world.data_submitter.name)
    world.page.is_text_present(world.form_data['username'], world.form_data['email'], 'Active')

@step(u'And I have 2 country admins and data submitters in countries in the AFRO')
def and_i_have_2_country_admins_and_data_submitters_in_countries_in_the_afro(step):
    world.user = User.objects.create(username="mutoni", email="mutoni@ccc.ccc")
    UserProfile.objects.create(user=world.user, country=world.uganda)
    world.user1 = User.objects.create(username="mbabazi", email="mbabazi@ccc.ccc")
    UserProfile.objects.create(user=world.user1, country=world.rwanda)
    world.data_submitter.user_set.add(world.user, world.user1)

@step(u'And I select the AFRO region')
def and_i_select_the_afro_region(step):
    world.page.select('region', world.region.id)

@step(u'Then I should see all the data submitters too')
def then_i_should_see_all_the_users_in_the_region_including_data_submitters_and_country_admins(step):
    world.page.is_text_present(world.user.username, world.user.email)
    world.page.is_text_present(world.user1.username, world.user1.email)

@step(u'And I have countries in AFRO region')
def and_i_have_countries_in_afro_region(step):
    world.uganda = Country.objects.create(name="Uganda")
    world.rwanda = Country.objects.create(name="Rwanda")
    world.region.countries.add(world.uganda, world.rwanda)

@step(u'And I click the create button')
def and_i_click_the_create_button(step):
    world.page.click_by_css('button.submit')

@step(u'And I have a an active data submitter user')
def and_i_have_a_an_active_data_submitter_user(step):
    password = 'pass'
    world.uganda = Country.objects.create(name="Uganda")
    world.datasubmitteruser = User.objects.create_user('ds', 'ds@ds.com', password)
    UserProfile.objects.create(user=world.datasubmitteruser, country=world.uganda)

@step(u'And I select that user')
def and_i_select_that_user(step):
    world.page.click_link_by_partial_href('/users/%s/edit' % world.datasubmitteruser.id)

@step(u'And I make that user inactive')
def and_i_make_that_user_inactive(step):
    world.page.uncheck_by_name('is_active')
    world.page.click_by_css('button.submit')

@step(u'Then that user should be unable to log in')
def then_that_user_should_be_unable_to_log_in(step):
    world.page = LoginPage(world.browser)
    world.page.visit()
    data = {'username': world.datasubmitteruser.username,
            'password': "pass"}
    world.page.fill_form(data)
    world.page.submit()

@step(u'And they should see a message that their account is inactive when they try to log in')
def and_they_should_see_a_message_that_their_account_is_inactive_when_they_try_to_log_in(step):
    world.page.is_text_present('This account is inactive')
