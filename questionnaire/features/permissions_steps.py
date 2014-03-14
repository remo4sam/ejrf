from lettuce import step, world


@step(u'Then I should not see the users and questionnaire links')
def then_i_should_not_see_the_users_and_questionnaire_links(step):
    world.page.is_text_present("USERS", "QUESTIONNAIRE", status=False)


@step(u'And I should see home, extract and attachments links')
def and_i_should_see_home_extract_and_attachments_links(step):
    world.page.is_text_present("HOME", "EXTRACT")