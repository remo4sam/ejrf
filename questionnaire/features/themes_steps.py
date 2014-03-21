from lettuce import step, world
from questionnaire.features.pages.theme import ThemePage
from questionnaire.models import Theme


@step(u'Given I have 100 themes')
def given_i_have_100_themes(step):
    for counter in range(100):
        Theme.objects.create(name='theme %d' % counter, description="Description for theme %d" % counter)

@step(u'And I visit the themes listing page')
def and_i_visit_the_themes_listing_page(step):
    world.page = ThemePage(world.browser)
    world.page.visit()

@step(u'Then I should see 2 of the themes')
def then_i_should_see_the_themes_paginated(step):
    for counter in range(2):
        world.page.is_text_present('theme %d' % counter, "Description for theme %d" % counter)