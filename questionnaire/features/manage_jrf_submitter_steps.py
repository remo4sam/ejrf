from lettuce import step, world
from questionnaire.features.pages.step_utils import create_regional_questionnaire_with_one_question
from questionnaire.models import TextAnswer, Answer


@step(u'And I have a "([^"]*)" questionnaire for my region')
def and_i_have_a_group1_questionnaire_for_my_region(step, type):
    world.questionnaire, world.question, world.answer_group = create_regional_questionnaire_with_one_question(world.region)

    if type == 'draft':
        answer = TextAnswer.objects.create(question=world.question, country=world.uganda,
                                  questionnaire=world.questionnaire,
                                  status=Answer.DRAFT_STATUS, response='This Data Submitter')
        world.answer_group.answer.add(answer)

    if type == 'submitted':
        answer = TextAnswer.objects.create(question=world.question, country=world.uganda,
                                  questionnaire=world.questionnaire,
                                  status=Answer.SUBMITTED_STATUS, response='This Data Submitter')
        world.answer_group.answer.add(answer)


@step(u'Then that questionnaire should appear under the list of "([^"]*)"  questionnaires')
def then_that_questionnaire_should_appear_under_the_list_of_group1_questionnaires(step, type):
    world.page.validate_questionnaire_type_appears_in_right_category(world.questionnaire, type)


@step(u'When I open the "([^"]*)" questionnaire for editing')
def when_i_open_the_group1_questionnaire_for_editing(step, type):
    if type == 'draft':
        world.page.click_by_id('draft-questionnaire-%s' % world.questionnaire.id)
    if type == 'submitted':
        world.page.click_by_id('submitted-questionnaire-%s' % world.questionnaire.id)
    if type == 'new':
        world.page.click_by_id('new-questionnaire-%s' % world.questionnaire.id)


@step(u'Then that questionnaire should open in "([^"]*)"')
def then_that_questionnaire_should_open_in_group1(step, mode):
    world.page.is_text_present(world.question.text)
    world.page.validate_questionnaire_opens_in_correct_mode(world.questionnaire, mode)


@step(u'And uploading attachments should be "([^"]*)"')
def and_uploading_attachments_should_be_group1(step, status):
    world.page.click_by_id('id_attachments')
    world.page.is_text_present('Attachments List')

    if status == 'allowed':
        world.page.is_text_present('Upload Support Document')
    else:
        world.page.is_text_present('Upload Support Document', status=False)