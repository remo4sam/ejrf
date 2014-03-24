from lettuce import step, world
from questionnaire.features.pages.questions import QuestionListingPage
from questionnaire.features.pages.step_utils import create_user_with_no_permissions, assign
from questionnaire.features.pages.users import LoginPage
from questionnaire.models import Question


@step(u'Given that I am logged in as a regional admin')
def given_that_i_am_logged_in_as_a_regional_admin(step):
    world.user, world.country, world.region = create_user_with_no_permissions()
    world.user = assign('can_edit_questionnaire', world.user)
    world.page = LoginPage(world.browser)
    world.page.visit()
    world.page.login(world.user, "pass")


@step(u'And I have regional questions in the question bank')
def and_i_have_regional_questions_in_the_question_bank(step):
    world.question1 = Question.objects.create(text='Name of UNICEF contact', export_label='UNICEF Contact',
                                              UID='00026', answer_type='Text', region=world.region)
    world.question2 = Question.objects.create(text='Name of WHO contact', export_label='WHO Contact', UID='00028',
                                              answer_type='Text', region=world.region)


@step(u'When I navigate to the question bank')
def when_i_navigate_to_the_question_bank(step):
    world.page = QuestionListingPage(world.browser)
    world.page.visit()


@step(u'Then I should see an option to delete each question')
def then_i_should_see_an_option_to_delete_each_question(step):
    assert world.page.is_element_present_by_id('delete-question-%s' % world.question1.id)
    assert world.page.is_element_present_by_id('delete-question-%s' % world.question2.id)


@step(u'When I choose to delete a question')
def when_i_choose_to_delete_a_question(step):
    world.page.click_by_id('delete-question-%s' % world.question2.id)


@step(u'Then I should see a prompt to confirm deleting the question')
def then_i_should_see_a_prompt_to_confirm_deleting_the_question(step):
    world.page.is_text_present('Confirm Delete')
    world.page.is_text_present('Are you sure you want to delete this question?')


@step(u'When I confirm the regional question deletion')
def when_i_confirm_the_regional_question_deletion(step):
    world.page.click_by_id('confirm-delete-question-%s' % world.question2.id)

@step(u'Then that question should not appear in the Question bank')
def then_that_question_should_not_appear_in_the_question_bank(step):
    assert (world.page.is_element_present_by_id('delete-question-%s' % world.question2.id), False)


@step(u'And I should see a message that the regional question was deleted')
def and_i_should_see_a_message_that_the_regional_question_was_deleted(step):
    world.page.is_text_present('Question was deleted successfully')