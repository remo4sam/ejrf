from time import sleep
from lettuce import step, world
from questionnaire.features.pages.questions import QuestionListingPage, CreateQuestionPage
from questionnaire.models import Question, Theme, Questionnaire, Section, SubSection, QuestionGroup, QuestionGroupOrder, QuestionOption, TextAnswer, Answer, AnswerGroup


@step(u'And I have 100 questions')
def and_i_have_100_questions(step):
    for i in range(0, 100):
        Question.objects.create(text="When will you be %s years old" % i, export_label="Export text for %s" % i,
                                instructions="question %s answer sensibly" % i, UID="%s" % i)


@step(u'I visit the question listing page')
def and_i_visit_the_question_listing_page(step):
    world.page = QuestionListingPage(world.browser)
    world.page.visit()


@step(u'And I have two themes')
def and_i_have_two_themes(step):
    world.theme1 = Theme.objects.create(name="Theme 1")
    world.theme2 = Theme.objects.create(name="Theme 2")


@step(u'Then I should see all questions paginated')
def then_i_should_see_all_questions_paginated(step):
    for i in range(0, 4):
        world.page.is_text_present("Export text for %s" % i, "%s" % i)
    world.page.click_link_by_text("2")


@step(u'And I click add new question page')
def and_i_click_add_new_question_page(step):
    world.page.click_by_id('id-add-new-question-link')

    world.data = {'text': 'How many measles cases did you find this year',
                  'instructions': 'Just give an answer',
                  'export_label': 'blah',
                  'theme': world.theme1.id}


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
            'export_label': 'blah',
            'theme': world.theme2.id}
    world.page.fill_form(data)


@step(u'And I check custom option')
def and_i_check_custom_option(step):
    world.page.check('custom')


@step(u'And I have a question without answers')
def and_i_have_a_question_without_answers(step):
    data = {'text': 'B. Number of cases tested',
            'instructions': "Enter the total number of cases",
            'UID': '00001', 'answer_type': 'Number',
            'theme': world.theme1}
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


@step(u'And I have a core question')
def and_i_have_a_core_question(step):
    world.core_question = Question.objects.create(text='Core Question Display Label', UID='C0001',
                                                  answer_type='MultiChoice', export_label='Core Question Export Label',
                                                  instructions='Sample Instructions')
    world.option1 = QuestionOption.objects.create(text="Option 1", question=world.core_question)
    world.option2 = QuestionOption.objects.create(text="Option 2", question=world.core_question)


@step(u'And that core question is used in a questionnaire with submitted responses')
def and_that_core_question_is_used_in_a_questionnaire_with_submitted_responses(step):
    world.questionnaire_status = Questionnaire.objects.create(name="JRF Core Status",
                                                              description="Questionnaire Status",
                                                              status=Questionnaire.PUBLISHED)
    world.section_status = Section.objects.create(order=1, title="Section AFRO", description="Description",
                                                  questionnaire=world.questionnaire_status, name="Cover page")
    world.subsection_status = SubSection.objects.create(order=1, section=world.section_status, title='AFRO Subsection')
    world.parent = QuestionGroup.objects.create(subsection=world.subsection_status, order=1)
    world.parent.question.add(world.core_question)
    QuestionGroupOrder.objects.create(question=world.core_question, question_group=world.parent, order=1)

    text_answer = TextAnswer.objects.create(question=world.core_question,
                              questionnaire=world.questionnaire_status,
                              status=Answer.SUBMITTED_STATUS, response='First Version Response')
    answerGroup = AnswerGroup.objects.create(grouped_question=world.parent)
    answerGroup.answer.add(text_answer)


@step(u'And I select the option to edit that question')
def and_i_select_the_option_to_edit_that_question(step):
    world.page.click_link_by_partial_href('/questions/%s/edit/' % world.core_question.id)


@step(u'The question should be displayed with all its attributes')
def the_question_should_be_displayed_with_all_its_attributes(step):
    world.page.validate_question_attributes(world.core_question)


@step(u'When I update the question with invalid details')
def when_i_update_the_question_with_invalid_details(step):
    question_data = {'text': '',
                     'instructions': '',
                     'export_label': '',
                     'theme': ''}
    world.page.fill_form(question_data)
    step.given('And I click save question button')

@step(u'I should see an error message')
def i_should_see_an_error_message(step):
    world.page.is_text_present('Question NOT updated. See errors below')
    world.page.is_text_present('This field is required')
    world.page.is_text_present('All questions must have export label')


@step(u'When I update the question with valid details')
def when_i_update_the_question_with_valid_details(step):
    world.theme = Theme.objects.create(name='Sample Theme')
    world.page.browser.reload()
    question_data = {'text': 'Updated Question Text',
                     'instructions': 'Updated Question Instructions',
                     'export_label': 'Updated Question Export Label',
                     'theme': world.theme.id}
    world.page.fill_form(question_data)
    world.page.submit()

@step(u'Then I should see a message that the question was successfully updated')
def then_i_should_see_a_message_that_the_question_was_successfully_updated(step):
    world.page.is_text_present('Question successfully updated')


@step(u'And I should see the updated details')
def and_i_should_see_the_updated_details(step):
    world.page.is_text_present('Updated Question Export Label')


@step(u'When I preview the submitted questionnaire where the question was used')
def when_i_preview_the_submitted_questionnaire_where_the_question_was_used(step):
    world.page.visit_url('/questionnaire/entry/%s/section/%s/?preview=1' % (world.questionnaire_status.id, world.section_status.id))


@step(u'I should see the earlier question display label')
def i_should_see_the_earlier_question_display_label(step):
    world.page.is_text_present(world.core_question.text)