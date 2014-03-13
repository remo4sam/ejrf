from time import sleep
from lettuce import step, world
from questionnaire.features.pages.questionnaires import QuestionnairePage
from questionnaire.features.pages.sections import CreateSubSectionPage


@step(u'And I click add new subsection link')
def and_i_click_add_new_subsection_link(step):
    world.page.click_by_id("new-subsection")

@step(u'Then I should see a new subsection modal')
def then_i_should_see_a_new_subsection_modal(step):
    world.page = CreateSubSectionPage(world.browser, world.questionnaire, world.section_1)
    world.page.is_text_present("New Subsection", "Description", "Title")

@step(u'When i fill in the subsection data')
def when_i_fill_in_the_subsection_data(step):
    data = {'title': 'Some title',
            'description': 'some description'}

    world.page.fill_this_form('#new-subsection-modal', data)
    sleep(3)

@step(u'And I save the subsection')
def and_i_save_the_subsection(step):
    world.page.click_by_id('save-new-subsection-modal')

@step(u'Then I should see the subsection I just created')
def then_i_should_see_the_subsection_i_just_created(step):
    world.page = QuestionnairePage(world.browser, world.section_1)
    world.page.is_text_present('Subsection successfully created.')
    world.page.is_text_present('Some title')

@step(u'And I choose to update a subsection')
def and_i_choose_to_update_a_subsection(step):
    world.page.click_by_id('edit-subsection-%s' % world.sub_section.id)

@step(u'Then I should see an edit subsection modal')
def then_i_should_see_an_edit_subsection_modal(step):
    world.page = CreateSubSectionPage(world.browser, world.questionnaire, world.section_1)
    world.page.is_text_present("Edit SubSection", "Title", "Description")

@step(u'When I update the subsection details')
def when_i_update_the_subsection_details(step):
    world.data = {'title': 'New SubSection Name',
                  'description': 'New SubSection description'}
    world.page.fill_this_form('#edit_subsection_%s_modal_form' % world.sub_section.id, world.data)

@step(u'And I save the changes to the subsection')
def and_i_save_the_changes_to_the_subsection(step):
    world.page.click_by_id('submit_edit_subsection_%s' % world.sub_section.id)

@step(u'Then I should see a message that the subsection was updated')
def then_i_should_see_a_message_that_the_subsection_was_updated(step):
    world.page.is_text_present('SubSection updated successfully')

@step(u'And I should see the changes I made to the subsection in the questionnaire')
def and_i_should_see_the_changes_i_made_to_the_subsection_in_the_questionnaire(step):
    world.page.is_text_present(world.data['title'])


@step(u'And I choose to delete one of the sub sections from the questionnaire')
def and_i_choose_to_delete_one_of_the_sub_sections_from_the_questionnaire(step):
    world.page.click_by_id('delete-subsection-%s' % world.sub_section.id)