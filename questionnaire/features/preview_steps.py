from lettuce import step, world
import time
from questionnaire.features.pages.manage import QuestionnairePreviewModal


@step(u'And I choose to preview my responses')
def and_i_choose_to_preview_my_responses(step):
    world.page.click_by_id('preview_modal_btn')

@step(u'Then I should see a preview layout of my responses')
def then_i_should_see_a_preview_layout_of_my_responses(step):
    world.page.is_text_present('Preview Questionnaire')
    world.page.is_element_present_by_id('preview_modal')

@step(u'And it should contain my responses')
def and_it_should_contain_my_responses(step):
    world.page.validate_responses(world.valid_responses)

@step(u'And the response fields in the preview should be inactive')
def and_the_response_fields_in_the_preview_should_be_inactive(step):
    assert False, 'This step must be implemented'

@step(u'And there should be a provision for me to submit my responses')
def and_there_should_be_a_provision_for_me_to_submit_my_responses(step):
    world.page.is_element_present_by_id('submit_button')

@step(u'And there should be a provision for me to exit the preview')
def and_there_should_be_a_provision_for_me_to_exit_the_preview(step):
    world.page.is_element_present_by_id('cancel_button')

@step(u'When I choose to exit the responses preview')
def when_i_choose_to_exit_the_preview(step):
    world.page.click_by_id('preview-close-button')

@step(u'Then I should see my questionnaire again with options for saving')
def then_i_should_see_my_questionnaire_again(step):
    time.sleep(2)
    world.page.is_text_present('Preview Questionnaire', status=False)
    world.page.is_element_present_by_id('save_draft_button')
    world.page.is_element_present_by_id('cancel_button')

@step(u'Then I should be able to see an option to preview the questionnaire')
def then_i_should_be_able_to_see_an_option_to_preview_the_questionnaire(step):
    world.page.is_element_present_by_id('preview_modal_btn')

@step(u'When I choose the option to preview the questionnaire')
def when_i_choose_the_option_to_preview_the_questionnaire(step):
    world.page.click_by_id('preview_modal_btn')

@step(u'Then I should see a preview layout of my questionnaire')
def then_i_should_see_a_preview_layout_of_my_questionnaire(step):
    world.page.is_text_present('Preview Questionnaire')
    world.page.is_element_present_by_id('preview_modal')

@step(u'And I should see all my assigned questions in the preview')
def and_i_should_see_all_my_assigned_questions_in_the_preview(step):
    world.page = QuestionnairePreviewModal(world.browser)
    world.page.validate_questions(world.question3, world.question4)

@step(u'And the response fields should be active')
def and_the_response_fields_should_be_active(step):
    assert False, 'This step must be implemented'

@step(u'When I choose to exit the questionnaire preview')
def when_i_choose_to_exit_the_questionnaire_preview(step):
    world.page.click_by_id('preview-close-button')

@step(u'Then I should see my questionnaire again with options for editing')
def then_i_should_see_my_questionnaire_again_with_options_for_editing(step):
    world.page.is_text_present('Assign Question')
    world.page.is_text_present('Edit')
    world.page.is_element_present_by_css('.delete-section')
    world.page.is_element_present_by_css('.delete-section')