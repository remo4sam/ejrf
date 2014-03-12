from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from lettuce import step, world
import time
from questionnaire.features.pages.manage import AssignModal, ManageJrfPage
from questionnaire.features.pages.step_utils import create_user_with_no_permissions, assign
from questionnaire.features.pages.users import LoginPage
from questionnaire.models import UserProfile, Organization, Question, QuestionGroup, QuestionGroupOrder, Questionnaire, Section, SubSection


@step(u'Given I am a logged-in Global Admin')
def given_i_am_a_logged_in_global_admin(step):
    world.unicef = Organization.objects.create(name="UNICEF")
    user = User.objects.create_user('globaladmin', 'global@unicef.com', 'pass')
    UserProfile.objects.create(user=user, organization=world.unicef)

    auth_content = ContentType.objects.get_for_model(Permission)
    group = Group.objects.create(name="Global Admin")
    permission, out = Permission.objects.get_or_create(codename='can_view_users', content_type=auth_content)
    permission_edit_questionnaire, out = Permission.objects.get_or_create(codename='can_edit_questionnaire',
                                                                          content_type=auth_content)
    group.permissions.add(permission, permission_edit_questionnaire)
    group.user_set.add(user)

    world.page = LoginPage(world.browser)
    world.page.visit()
    world.page.login(user, 'pass')

@step(u'And I have a questionnaire with sections and with subsections')
def and_i_have_a_questionnaire_with_sections_and_with_subsections(step):
    world.questionnaire = Questionnaire.objects.create(name="JRF Bolivia version", description="some more description",
                                                        year=2013, status=Questionnaire.DRAFT)
    world.section1 = Section.objects.create(order=0,
                        title="WHO/UNICEF Joint Reporting Form on Immunization for the Period January-December, 2013",
                        description="""If a question is not relevant, enter "NR" (not relevant)""",
                        questionnaire=world.questionnaire, name="Cover page")
    world.section2 = Section.objects.create(order=1,
                        title="Another title",
                        description="This is just another one of them",
                        questionnaire=world.questionnaire, name="Cover page")
    world.sub_section = SubSection.objects.create(order=1, section=world.section1)

@step(u'And I have unassigned questions')
def and_i_have_unassigned_questions(step):
    world.question1 = Question.objects.create(text='Position/title', export_label='Position/title', UID='00024',
                                              answer_type='Text',)
    world.question2 = Question.objects.create(text='Email address', export_label='Email address', UID='00025',
                                              answer_type='Text',)

@step(u'And I have assigned questions')
def and_i_have_assigned_questions(step):
    world.question3 = Question.objects.create(text='Name of UNICEF contact', export_label='UNICEF Contact',
                                              UID='00026', answer_type='Text',)
    world.question4 = Question.objects.create(text='Name of WHO contact', export_label='WHO Contact', UID='00028',
                                              answer_type='Text',)

    parent = QuestionGroup.objects.create(subsection=world.sub_section, order=1)
    parent.question.add(world.question3, world.question4)

    QuestionGroupOrder.objects.create(question=world.question3, question_group=parent, order=1)
    QuestionGroupOrder.objects.create(question=world.question4, question_group=parent, order=2)

@step(u'When I open that questionnaire for editing')
def when_i_open_that_questionnaire_for_editing(step):
    world.page = ManageJrfPage(world.browser)
    world.page.visit()
    world.page.selectQuestionnaire(world.questionnaire)

@step(u'Then I should see options to assign questions to sub-sections')
def then_i_should_see_options_to_assign_questions_to_sub_sections(step):
    world.page.is_text_present('Assign Question')

@step(u'When I choose to assign a question to a sub-section')
def when_i_choose_to_assign_a_question_to_a_sub_section(step):
    world.page.click_by_id('id-assign-%s' % world.sub_section.id)

@step(u'Then I should see the question bank with both assigned and unassigned questions')
def then_i_should_see_the_question_bank_with_both_assigned_and_unassigned_questions(step):
    world.page = AssignModal(world.browser)
    world.page.validate_questions(world.question1, world.question2, world.question3, world.question4)

@step(u'When I select questions to assign to the questionnaire')
def when_i_select_questions_to_assign_to_the_questionnaire(step):
    world.page.check(world.question1.id)
    world.page.check(world.question2.id)
    world.page.click_by_id('submit_assign_button')

@step(u'Then I should see the newly assigned questions in the questionnaire when I am done editing')
def then_i_should_see_the_newly_assigned_questions_in_the_questionnaire_when_i_m_done_editing(step):
    world.page.is_text_present(world.question1.export_label)
    world.page.is_text_present(world.question2.export_label)

@step(u'Then I should see options for unassigning questions from the questionnaire')
def then_i_should_see_options_for_unassigning_questions_from_the_questionnaire(step):
    world.page.is_element_present_by_css('.unassign-question')

@step(u'When I choose to unassign a question from the questionnaire')
def when_i_unassign_a_question_from_the_questionnaire(step):
    world.page.click_by_id('unassign-question-%s' % world.question3.id)

@step(u'And that question should no longer appear in the questionnaire')
def then_that_question_should_no_longer_appear_in_the_questionnaire(step):
    world.page.is_text_present(world.question3.text, status=False)

@step(u'And I confirm my actions')
def and_i_confirm_my_actions(step):
    time.sleep(2)
    world.page.click_by_id('confirm-unassign-%s' % world.question3.id)

@step(u'Then I should see a message that the question was unassigned')
def then_i_should_see_a_message_that_the_question_was_unassigned(step):
    world.page.is_text_present('Question successfully unassigned from questionnaire')

@step(u'Given I am a logged-in as a Regional Admin')
def given_i_am_a_logged_in_as_a_regional_admin(step):
    world.user, world.country, world.region = create_user_with_no_permissions()
    world.user = assign('can_edit_questionnaire', world.user)

@step(u'And I login the regional user')
def and_i_login_the_regional_user(step):
    world.page = LoginPage(world.browser)
    world.page.visit()
    world.page.login(world.user, 'pass')

@step(u'And I choose to assign a question to a sub-section')
def and_i_choose_to_assign_a_question_to_a_sub_section(step):
    world.page.click_by_id("id-assign-%s" % world.sub_section.id)
    time.sleep(3)

@step(u'And I have regional questions already assigned to my questionnaire')
def and_i_have_assigned_regional_questions(step):
    world.question3 = Question.objects.create(text='Name of UNICEF contact', export_label='UNICEF Contact',
                                              UID='00026', answer_type='Text', region=world.region)
    world.question4 = Question.objects.create(text='Name of WHO contact', export_label='WHO Contact', UID='00028',
                                              answer_type='Text', region=world.region)

    group = QuestionGroup.objects.create(subsection=world.sub_section, order=1)
    group.question.add(world.question3, world.question4)

    QuestionGroupOrder.objects.create(question=world.question3, question_group=group, order=1)
    QuestionGroupOrder.objects.create(question=world.question4, question_group=group, order=2)

@step(u'When I open that regional questionnaire for editing')
def when_i_open_that_regional_questionnaire_for_editing(step):
    world.page.click_by_id("questionnaire-%s" % world.questionnaire.id)

@step(u'And I have a questionnaire for my region with sections and subsections')
def and_i_have_a_questionnaire_for_my_region_with_sections_and_subsections(step):
    world.questionnaire = Questionnaire.objects.create(name="JRF Bolivia version", description="some more description",
                                                       year=2013, status=Questionnaire.DRAFT, region=world.region)
    world.section1 = Section.objects.create(order=0, title="WHO/UNICEF Joint Reporting Form",
                                            questionnaire=world.questionnaire, name="Cover page", region=world.region)
    world.section2 = Section.objects.create(order=1, title="Another title", description="This is just another one of them",
                                            questionnaire=world.questionnaire, name="Cover page", region=world.region)
    world.sub_section = SubSection.objects.create(order=1, section=world.section1, region=world.region)

@step(u'And I have regional questions that are not assigned to my questionnaire')
def and_i_have_regional_questions_that_are_not_assigned_to_my_questionnaire(step):
    world.not_assigned_question1 = Question.objects.create(text='Name of UNICEF contact', export_label='UNICEF Contact',
                                                           UID='0033w', answer_type='Text', region=world.region)
    world.not_assigned_question2 = Question.objects.create(text='Name of WHO contact', export_label='WHO Contact', UID='00238',
                                                           answer_type='Text', region=world.region)

@step(u'When I select the regional questions to assign to the questionnaire')
def when_i_select_the_regional_questions_to_assign_to_the_questionnaire(step):
    world.page.check(world.not_assigned_question1.id)
    world.page.check(world.not_assigned_question2.id)

@step(u'And I click done button')
def and_i_click_done_button(step):
    world.page.click_by_id('submit_assign_button')

@step(u'Then I should see the newly assigned regional questions in the questionnaire')
def then_i_should_see_the_newly_assigned_regional_questions_in_the_questionnaire(step):
    world.page.is_text_present(world.not_assigned_question1.text, world.not_assigned_question2.text)
    world.page.is_text_present("Questions successfully assigned to questionnaire.")

@step(u'And I should see question numbers with region name')
def and_i_should_see_question_numbers_with_region_name(step):
    last_order = world.question4.orders.all()[0].order
    question_number1 = '%s - %d. %d.'%(world.region.name, world.section1.order, last_order+1)
    question_number2 = '%s - %d. %d.'%(world.region.name, world.section1.order, last_order+2)
    print question_number1, question_number2
    print question_number1, question_number2
    world.page.is_text_present(question_number1)
    world.page.is_text_present(question_number2)