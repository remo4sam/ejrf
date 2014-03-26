from lettuce import step, world
from questionnaire.features.pages.home import HomePage
from questionnaire.features.pages.step_utils import assign, create_user_with_no_permissions
from questionnaire.features.pages.users import LoginPage
from questionnaire.models import Theme

@step(u'Given that I am logged in as a regional admin')
def given_that_i_am_logged_in_as_a_regional_admin(step):
    world.user, world.country, world.region = create_user_with_no_permissions()
    world.user = assign('can_edit_questionnaire', world.user)
    world.page = LoginPage(world.browser)
    world.page.visit()
    world.page.login(world.user, "pass")

@step(u'And I have two regional themes')
def and_i_have_two_themes(step):
    world.theme1 = Theme.objects.create(name="Theme 1", region=world.region)
    world.theme2 = Theme.objects.create(name="Theme 2", region=world.region)

@step(u'And I am on the home page')
def and_i_am_on_the_home_page(step):
    world.page = HomePage(world.browser)
    world.page.visit()


@step(u'Then I should see questions on the top menu')
def then_i_should_see_questions_on_the_top_menu(step):
    world.page.is_text_present("QUESTIONS")
