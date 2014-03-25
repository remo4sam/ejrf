from lettuce import step, world
from questionnaire.features.pages.home import HomePage


@step(u'And I am on the home page')
def and_i_am_on_the_home_page(step):
    world.page = HomePage(world.browser)
    world.page.visit()


@step(u'Then I should see questions on the top menu')
def then_i_should_see_questions_on_the_top_menu(step):
    world.page.is_text_present("QUESTIONS")
