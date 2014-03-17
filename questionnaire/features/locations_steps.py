from lettuce import step, world
from questionnaire.features.pages.locations import ListRegionsPage, ListCountriesPage
from questionnaire.features.pages.step_utils import create_user_with_no_permissions, assign
from questionnaire.features.pages.users import LoginPage
from questionnaire.models.locations import Region, Country, Organization


@step(u'Given I am logged in as a data submitter')
def given_i_am_logged_in(step):
    world.user, world.uganda, world.afro = create_user_with_no_permissions()
    world.user = assign('can_submit_responses', world.user)

    world.page = LoginPage(world.browser)
    world.page.visit()
    world.page.login(world.user, 'pass')

@step(u'And I have two regions')
def given_i_have_two_regions(step):
    world.org = Organization.objects.create(name="WHO")
    world.afro = Region.objects.create(name="AFRO", organization=world.org)
    world.paho = Region.objects.create(name="PAHO", organization=world.org)

@step(u'And I visit the list regions page')
def and_i_visit_the_list_regions_page(step):
    world.page = ListRegionsPage(world.browser)
    world.page.visit()

@step(u'Then I should see the list of regions')
def then_i_should_see_the_list_of_regions(step):
    world.page.validate_region_list([world.afro, world.paho])

@step(u'Given I have two countries in a region')
def given_i_have_two_countries_in_a_region(step):
    world.org = Organization.objects.create(name="WHO")
    world.afro = Region.objects.create(name="AFRO", organization=world.org)
    world.uganda = Country.objects.create(name="Uganda", code="UGX")
    world.uganda.regions.add(world.afro)
    world.kenya = Country.objects.create(name="Kenya", code="KSX")
    world.kenya.regions.add(world.afro)

@step(u'And I visit the list countries page in that region')
def and_i_visit_the_list_countries_page_in_that_region(step):
    world.page = ListCountriesPage(world.browser, world.afro)
    world.page.visit()

@step(u'Then I should see the list of countries in that region')
def then_i_should_see_the_list_of_countries_in_that_region(step):
    world.page.validate_country_list([world.uganda, world.kenya])

@step(u'When I click on the first region name')
def when_i_click_on_the_first_region_name(step):
    world.page.click_link_by_text(world.afro.name)

@step(u'Then I should see the list country page')
def then_i_should_see_the_list_country_page(step):
    world.page = ListCountriesPage(world.browser, world.afro)
    world.page.validate_url()