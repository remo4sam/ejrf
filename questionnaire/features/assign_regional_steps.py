from time import sleep
from lettuce import step, world
from questionnaire.features.pages.step_utils import assign, create_user_with_no_permissions, \
    create_regional_admin_with_no_permissions
from questionnaire.features.pages.users import LoginPage
from questionnaire.models import Question, QuestionGroup, QuestionGroupOrder, Questionnaire, Section, SubSection


@step(u'Given I am a Regional Admin')
def given_i_am_a_logged_in_as_a_regional_admin(step):
    world.user, world.region = create_regional_admin_with_no_permissions()
    world.user = assign('can_edit_questionnaire', world.user)


@step(u'I login the regional user')
def and_i_login_the_regional_user(step):
    world.page = LoginPage(world.browser)
    world.page.visit()
    world.page.login(world.user, 'pass')


@step(u'And I have regional questions already assigned to my questionnaire')
def and_i_have_assigned_regional_questions(step):
    world.question3 = Question.objects.create(text='question 3', export_label='UNICEF Contact',
                                              UID='00026', answer_type='Text', region=world.region)
    world.question4 = Question.objects.create(text='question 4', export_label='WHO Contact', UID='00028',
                                              answer_type='Text', region=world.region)
    world.question5 = Question.objects.create(text='question 5', export_label='WHO Contact', UID='000928',
                                              answer_type='Text', region=world.region)

    group = QuestionGroup.objects.create(subsection=world.sub_section, order=1)
    group.question.add(world.question3, world.question4, world.question5)

    QuestionGroupOrder.objects.create(question=world.question3, question_group=group, order=1)
    QuestionGroupOrder.objects.create(question=world.question4, question_group=group, order=2)
    QuestionGroupOrder.objects.create(question=world.question5, question_group=group, order=3)


@step(u'And I have a questionnaire for my region with sections and subsections')
def and_i_have_a_questionnaire_for_my_region_with_sections_and_subsections(step):
    world.questionnaire = Questionnaire.objects.create(name="JRF Bolivia version", description="some more description",
                                                       year=2013, status=Questionnaire.DRAFT, region=world.region)
    world.section1 = Section.objects.create(order=0, title="section 1",
                                            questionnaire=world.questionnaire, name="section 1", region=world.region)
    world.section_1 = Section.objects.create(order=4, title="section_1",
                                            questionnaire=world.questionnaire, name="section_1")
    world.section2 = Section.objects.create(order=1, title="Another title",
                                            description="This is just another one of them",
                                            questionnaire=world.questionnaire, name="Reported Cases",
                                            region=world.region)
    world.section3 = Section.objects.create(order=2, title="Section 3 Title",
                                            description="Section 3 description",
                                            questionnaire=world.questionnaire, name="Section 3", region=world.region)
    world.section4 = Section.objects.create(order=3, title="Core Section",
                                            description="Section 3 description",
                                            questionnaire=world.questionnaire, name="Section 3")
    world.sub_section = SubSection.objects.create(title="regional subs", order=1, section=world.section1, region=world.region)
    world.sub_section_1 = SubSection.objects.create(title="other R subs", order=1, section=world.section_1, region=world.region)
    world.core_sub_section = SubSection.objects.create(title="core subs", order=2, section=world.section_1)


@step(u'When I open that regional questionnaire for editing')
def when_i_open_that_regional_questionnaire_for_editing(step):
    world.page.click_by_id("questionnaire-%s" % world.questionnaire.id)


@step(u'And I have regional questions that are not assigned to my questionnaire')
def and_i_have_regional_questions_that_are_not_assigned_to_my_questionnaire(step):
    world.not_assigned_question1 = Question.objects.create(text='Name of UNICEF contact', export_label='UNICEF Contact',
                                                           UID='0033w', answer_type='Text', region=world.region)
    world.not_assigned_question2 = Question.objects.create(text='Name of UNICEF contact', export_label='UNICEF Contact',
                                                           UID='00334', answer_type='Text', region=world.region)
    world.not_assigned_question3 = Question.objects.create(text='Name of WHO contact', export_label='WHO Contact',
                                                           UID='0023w',
                                                           answer_type='Text', region=world.region)


@step(u'And I have core questions assigned to my questionnaire')
def and_i_have_core_questions_assigned_to_my_questionnaire(step):
    world.question7 = Question.objects.create(text='Global Name of UNICEF contact', export_label='UNICEF Contact',
                                              UID='01026', answer_type='Text')
    world.question8 = Question.objects.create(text='Global Name of WHO contact', export_label='WHO Contact',
                                              UID='01028',
                                              answer_type='Text')

    group = QuestionGroup.objects.create(subsection=world.sub_section, order=2)
    group.question.add(world.question7, world.question8)

    QuestionGroupOrder.objects.create(question=world.question7, question_group=group, order=1)
    QuestionGroupOrder.objects.create(question=world.question8, question_group=group, order=2)


@step(u'When I select the regional questions to assign to the questionnaire')
def when_i_select_the_regional_questions_to_assign_to_the_questionnaire(step):
    world.page.check(world.not_assigned_question1.id)
    world.page.check(world.not_assigned_question2.id)
    world.page.check(world.not_assigned_question3.id)


@step(u'Then I should see the newly assigned regional questions in the questionnaire')
def then_i_should_see_the_newly_assigned_regional_questions_in_the_questionnaire(step):
    world.page.is_text_present(world.not_assigned_question1.text, world.not_assigned_question2.text)
    world.page.is_text_present("Questions successfully assigned to questionnaire.")


@step(u'Then I should see unassign options for each regional question')
def then_i_should_see_unassign_options_for_each_regional_question(step):
    world.page.is_element_present_by_id('unassign-question-%s' % world.not_assigned_question2.id)


@step(u'And I should not see unassign options for the core questions')
def and_i_should_not_see_unassign_options_for_the_core_questions(step):
    assert (world.page.is_element_present_by_id('unassign-question-%s' % world.question7.id), False)
    assert (world.page.is_element_present_by_id('unassign-question-%s' % world.question8.id), False)


@step(u'I choose to unassign a question from a sub-section')
def and_i_choose_to_unassign_a_question_from_a_sub_section(step):
    world.page.click_by_id('unassign-question-%s' % world.question4.id)


@step(u'Then I should see a prompt to confirm unassign of the question')
def then_i_should_see_a_prompt_to_confirm_unassign_of_the_question(step):
    world.page.is_text_present('Confirm Unassign')
    world.page.is_text_present('Are you sure you want to unassign this question?')


@step(u'When I confirm unassign of the question')
def when_i_confirm_unassign_of_the_question(step):
    world.page.click_by_id('confirm-unassign-question-%s' % world.question4.id)


@step(u'Then the unassigned question should not appear in the questionnaire')
def then_the_unassigned_question_should_not_appear_in_the_questionnaire(step):
    assert world.page.is_element_not_present_by_id('confirm-unassign-%s' % world.question4.id)


@step(u'And I should see a message that question is successfully unassigned')
def and_i_should_see_a_message_that_question_is_successfully_unassigned(step):
    world.page.is_text_present('Question successfully unassigned from questionnaire')


@step(u'And the question numbering should be updated')
def and_the_question_numbering_should_be_updated(step):
    world.page.is_text_present('0.1.2.%s' % (world.question5.text))


@step(u'And the regional question numbers should be prefixed with the region name')
def and_the_regional_question_numbers_should_be_prefixed_with_the_region_name(step):
    sleep(2)
    world.page.is_text_present('%s - 0.4.%s' % (world.region.name, world.not_assigned_question1.text))