from time import sleep
from django.contrib.auth.models import User, Permission, Group
from django.contrib.contenttypes.models import ContentType
from lettuce import step, world
from questionnaire.features.pages.questionnaires import QuestionnairePage
from questionnaire.features.pages.sections import CreateSectionPage
from questionnaire.features.pages.users import LoginPage
from questionnaire.models import Country, UserProfile


@step(u'Given I am logged in as a global admin')
def given_i_am_logged_in_as_a_global_admin(step):
    world.uganda = Country.objects.create(name="Uganda")
    user = User.objects.create_user('Rajni', 'rajni@kant.com', 'pass')
    UserProfile.objects.create(user=user, country=world.uganda)
    auth_content = ContentType.objects.get_for_model(Permission)
    group = Group.objects.create(name="Data Submitter")
    permission, out = Permission.objects.get_or_create(codename='can_view_users', content_type=auth_content)
    permission_edit_questionnaire, out = Permission.objects.get_or_create(codename='can_edit_questionnaire',
                                                                          content_type=auth_content)
    group.permissions.add(permission, permission_edit_questionnaire)
    group.user_set.add(user)

    world.page = LoginPage(world.browser)
    world.page.visit()
    world.page.login(user, "pass")

@step(u'And I click add new section link')
def and_i_click_add_new_section_link(step):
    world.page.click_by_id("new-section")

@step(u'Then I should see a new section modal')
def then_i_should_see_a_new_section_modal(step):
    world.page = CreateSectionPage(world.browser, world.questionnaire)
    world.page.is_text_present("New Section", "Description", "Name", "Title")

@step(u'When i fill in the section data')
def when_i_fill_in_the_section_data(step):
    data = {'title': 'Some title',
            'description': 'some description'}

    world.page.fill_form(data)
    sleep(3)
    world.page.fill_form({'name': 'Some section'})


@step(u'Then I should see the section I created')
def then_i_should_see_the_section_i_created(step):
    world.page = QuestionnairePage(world.browser, world.section_1)
    world.page.is_text_present('Section created successfully')
    world.page.is_text_present('Some section')

@step(u'And I save the section')
def and_i_save_the_section(step):
    world.page.fill_form({'name': 'Some section'})
    world.page.click_by_id('save-new-section-modal')

@step(u'And I fill in invalid data')
def and_i_fill_in_invalid_data(step):
    data = {'name': '',
            'title': '',
            'description': 'some description'}
    world.page = CreateSectionPage(world.browser, world.questionnaire)
    world.page.fill_form(data)

@step(u'Then I should see error messages against the fields')
def then_i_should_see_error_messages_against_the_fields(step):
    world.page.is_text_present('This field is required')

<<<<<<< HEAD
@step(u'And I choose to update a section')
def and_i_choose_to_update_a_section(step):
    world.page.click_by_id('edit-section-%s' % world.section_1.id)

@step(u'Then I should see an edit section modal')
def then_i_should_see_an_edit_section_modal(step):
    world.page = CreateSectionPage(world.browser, world.questionnaire)
    world.page.is_text_present("Edit Section", "Description", "Name", "Title")

@step(u'When I update the section details')
def when_i_update_the_section_details(step):
    data = {'name': 'New Section Name',
            'title': 'New Section Title'}
    world.page.fill_form(data)

@step(u'And I save the changes to the section')
def and_i_save_the_changes_to_the_section(step):
    world.page.click_by_id('submit_edit_section_%s' % world.section_1.id)

@step(u'Then I should see a message that the section was updated')
def then_i_should_see_a_message_that_the_section_was_updated(step):
    world.page.is_text_present('Section updated successfully')

@step(u'And I should see the changes I made to the section in the questionnaire')
def and_i_should_see_the_changes_i_made_to_the_section_in_the_questionnaire(step):
    world.page.is_text_present('New Section Name')
    world.page.is_text_present('New Section Title')
=======
@step(u'And I choose to delete a section')
def when_i_choose_to_delete_a_section(step):
    world.page.click_by_id('id-delete-section-%s' % world.section1.id)

@step(u'Then I should see a confirmation dialog')
def then_i_should_see_a_confirmation_dialog(step):
    world.page.is_text_present('Delete Section')

@step(u'When I confirm that I want to delete')
def when_i_confirm_that_i_want_to_delete(step):
    world.page.click_by_id('confirm-delete-%s' % world.section1.id)

@step(u'Then I should see a message that the section was deleted')
def then_i_should_see_a_message_that_the_section_was_deleted(step):
    world.page.is_text_present('Section successfully deleted.')
    world.page.is_element_present_by_css('.alert-success')
>>>>>>> [Robert, Tom, Emily] Added funtional tests for the delete section story
