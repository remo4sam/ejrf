from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from lettuce import step, world
import time
from questionnaire.features.pages.manage import AssignModal, ManageJrfPage
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
    world.page.is_text_not_present(world.question3.text)

@step(u'And I confirm my actions')
def and_i_confirm_my_actions(step):
    time.sleep(2)
    world.page.click_by_id('confirm-unassign-%s' % world.question3.id)

@step(u'Then I should see a message that the question was unassigned')
def then_i_should_see_a_message_that_the_question_was_unassigned(step):
    world.page.is_text_present('Question successfully unassigned from questionnaire')