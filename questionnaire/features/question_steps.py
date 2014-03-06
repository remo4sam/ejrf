from lettuce import step, world
from questionnaire.features.pages.questions import QuestionListingPage, CreateQuestionPage
from questionnaire.models import Question


@step(u'And I have 100 questions')
def and_i_have_100_questions(step):
    for i in range(0, 100):
        Question.objects.create(text="When will you be %s years old" % i, export_label="Export text for %s" % i,
                                instructions="question %s answer sensibly" % i, UID="%s" % i)

@step(u'And I visit the question listing page')
def and_i_visit_the_question_listing_page(step):
    world.page.click_by_id('id-question-bank-link')
    world.page = QuestionListingPage(world.browser)

@step(u'Then I should see all questions paginated')
def then_i_should_see_all_questions_paginated(step):
    for i in range(0, 4):
        world.page.is_text_present("Export text for %s" % i,  "%s" % i)
    world.page.click_link_by_text("2")

@step(u'And I click add new question page')
def and_i_click_add_new_question_page(step):
    world.page.click_by_id('id-add-new-question-link')

world.data = {'text': 'How many measles cases did you find this year',
              'instructions': 'Just give an answer',
              'export_label': 'blah'}

@step(u'And I fill in the question details')
def and_i_fill_in_the_question_details(step):
    world.page.fill_form(world.data)
    world.page.select('answer_type', 'Number')

@step(u'Then I should see the question created')
def then_i_should_see_the_question_created(step):
    world.page.is_text_present("Question successfully created")

@step(u'And I click save question button')
def and_i_click_save_question_button(step):
    world.page.click_by_css('.submit')

@step(u'And I select Multi-choice answer type')
def and_i_select_multi_choice_answer_type(step):
    world.page.select('answer_type', 'MultiChoice')

@step(u'Then I should see the option field')
def then_i_should_see_the_option_field(step):
    world.page.is_text_present('Option 1')

@step(u'When Fill in the option')
def when_fill_in_the_option(step):
    world.page = CreateQuestionPage(world.browser)
    world.page.fill_first_visible_option('options', 'Yes')

@step(u'When I click add more button')
def when_i_click_add_more_button(step):
    world.page.click_by_css('.add-option')

@step(u'Then I should see another option field')
def then_i_should_see_another_option_field(step):
    world.page.is_text_present('Option 2')

@step(u'When I click remove the added option field')
def when_i_click_remove_the_added_option_field(step):
    world.page.remove_option_field('.remove-option', 1)

@step(u'Then I should not see that option field')
def then_i_should_not_see_that_option_field(step):
    world.page.is_text_present('Option 2', status=False)

@step(u'And I fill in the multichoice question form data')
def and_i_fill_in_the_multichoice_question_form_data(step):
    data = {'text': 'How many measles cases did you find this year',
            'instructions': 'Just give an answer',
            'export_label': 'blah'}
    world.page.fill_form(data)

@step(u'And I check custom option')
def and_i_check_custom_option(step):
    world.page.check('custom')

@step(u'And I have a question without answers')
def and_i_have_a_question_without_answers(step):
    data = {'text': 'B. Number of cases tested',
            'instructions': "Enter the total number of cases",
            'UID': '00001', 'answer_type': 'Number'}
    world.question = Question.objects.create(**data)

@step(u'And I click delete on that question')
def and_i_click_delete_on_that_question(step):
    world.page.click_by_id('delete-question-%s' % world.question.id)

@step(u'Then I should see that question was deleted successfully')
def then_i_should_see_that_question_was_deleted_successfully(step):
    world.page.is_text_present("Question was deleted successfully")

@step(u'Then I should see a delete confirmation modal')
def then_i_should_see_a_delete_confirmation_modal(step):
    world.page.confirm_delete('question')

@step(u'When I confirm delete')
def when_i_confirm_delete(step):
    world.page.click_by_css('.confirm-delete')