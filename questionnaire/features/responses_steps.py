from time import sleep
from django.contrib.auth.models import User
from lettuce import step, world
from questionnaire.features.pages.questionnaires import QuestionnairePage
from questionnaire.features.pages.users import LoginPage
from questionnaire.models import Questionnaire, Section, SubSection, Question, QuestionGroup, QuestionGroupOrder, Region, Country, UserProfile

@step(u'Given I am a logged-in user with a user Profile')
def given_i_am_a_logged_in_user_with_a_user_profile(step):
    world.region = Region.objects.create(name="Afro")
    world.country = Country.objects.create(name="Uganda", code="UGA")
    world.region.countries.add(world.country)
    world.user = User.objects.create(username='user', email='user@mail.com')
    world.user.set_password("password")
    world.user.save()
    UserProfile.objects.create(user=world.user, country=world.country, region=world.region)

    world.page = LoginPage(world.browser)
    world.page.visit()
    data = {'username': world.user.username,
            'password': "password"}
    world.page.fill_form(data)
    world.page.submit()

@step(u'And I have a questionnaire with questions')
def given_i_have_a_questionnaire_with_questions(step):
    world.questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English", status=Questionnaire.PUBLISHED,
                                                       region=world.afro)

    world.section_1 = Section.objects.create(order=0,
                        title="WHO/UNICEF Joint Reporting Form on Immunization for the Period January-December, 2013",
                        description="0",
                        questionnaire=world.questionnaire, name="Cover page")
    world.section_2 = Section.objects.create(title="Reported Cases of Selected Vaccine Preventable Diseases (VPDs)", order=1,
                                              questionnaire=world.questionnaire, name="Reported Cases")
    world.sub_section = SubSection.objects.create(order=1, section=world.section_1)

    world.question1 = Question.objects.create(text='Name of person in Ministry of Health responsible for completing this form',
                                    UID='C00023', answer_type='Text', instructions="""
    List the name of the person responsible for submitting the completed form.
    Since multiple departments in the Ministry of Health may have relevant data,
    this person should liaise with other departments to ensure that the form
    contains the most accurate and complete data possible. For example,
    information on Vitamin A may come from the nutrition department.""")
    world.question2 = Question.objects.create(text='Position/title', UID='C00024', answer_type='Text',)
    world.question3 = Question.objects.create(text='Email address', UID='C00025', answer_type='Text',)
    world.question4 = Question.objects.create(text='Name of UNICEF contact', UID='C00026', answer_type='Text',)
    world.question5 = Question.objects.create(text='Email address of UNICEF contact', UID='C00027', answer_type='Text',)
    world.question6 = Question.objects.create(text='Name of WHO contact', UID='C00028', answer_type='Text',)
    world.question7 = Question.objects.create(text='Email address of WHO contact', UID='C00029', answer_type='Text',)
    world.question8 = Question.objects.create(text='Total number of districts in the country', UID='C00030', answer_type='Number',
                                    instructions="""
                                    A district is defined as the third administrative level (nation is the first, province is the second).
                                    """)

    parent = QuestionGroup.objects.create(subsection=world.sub_section, order=1)
    parent.question.add(world.question1, world.question2, world.question3, world.question4, world.question5, world.question6, world.question7, world.question8)

    QuestionGroupOrder.objects.create(question=world.question1, question_group=parent, order=1)
    QuestionGroupOrder.objects.create(question=world.question2, question_group=parent, order=2)
    QuestionGroupOrder.objects.create(question=world.question3, question_group=parent, order=3)
    QuestionGroupOrder.objects.create(question=world.question4, question_group=parent, order=4)
    QuestionGroupOrder.objects.create(question=world.question5, question_group=parent, order=5)
    QuestionGroupOrder.objects.create(question=world.question6, question_group=parent, order=6)
    QuestionGroupOrder.objects.create(question=world.question7, question_group=parent, order=7)
    QuestionGroupOrder.objects.create(question=world.question8, question_group=parent, order=8)


@step(u'And I navigate to the section of the questionnaire to be filled in')
def and_i_navigate_to_the_section_of_the_questionnaire_to_be_filled_in(step):
    world.page = QuestionnairePage(world.browser, world.section_1)
    world.page.visit()

@step(u'I enter valid responses to the questions')
def and_i_enter_valid_responses_to_the_questions(step):
    world.valid_responses = {
        'Text-0-response': 'James Smith',
        'Text-1-response': 'EPI Manager',
        'Text-2-response': 'jsmith@moh.gov.ug',
        'Text-3-response': 'Angellina Jones',
        'Text-4-response': 'ajones@unicef.org',
        'Text-5-response': 'Brad Wolfstrom',
        'Text-6-response': 'brad.wolfstrom@who.org',
        'Number-0-response': '200'}
    world.page.fill_form(world.valid_responses)

@step(u'I click the save button')
def when_i_click_the_save_button(step):
    world.page.click_by_id('save_draft_button')

@step(u'Then I should see a message that a draft of my responses has been saved')
def then_i_should_see_a_message_that_a_draft_of_my_responses_has_been_saved(step):
    world.page.validate_alert_success()

@step(u'And when I navigate back to this section')
def and_when_i_navigate_back_to_this_section(step):
    world.page.visit()

@step(u'I should see my responses filled out')
def i_should_see_my_responses_filled_out(step):
    world.page.validate_responses(world.valid_responses)

@step(u'When I enter invalid responses to the questions')
def when_i_enter_invalid_responses_to_the_questions(step):
    invalid_responses = {
        'Text-0-response': '',
        'Text-1-response': '',
        'Text-2-response': '',
        'Text-3-response': 'Angellina Jones',
        'Text-4-response': 'ajones@unicef.org',
        'Text-5-response': 'Brad Wolfstrom',
        'Text-6-response': 'brad.wolfstrom@who.org',
        'Number-0-response': 'something that is not a number'}
    world.page.fill_form(invalid_responses)

@step(u'Then I should see a save draft error message')
def then_i_should_see_a_save_draft_error_message(step):
    world.page.validate_alert_error()

@step(u'I switch to another section')
def and_i_switch_to_another_section(step):
    world.page.click_link_by_partial_href('section/2')

@step(u'When I choose to submit my responses')
def when_i_choose_to_submit_my_responses(step):
    world.page.click_by_id('submit_questionnaire_btn')

@step(u'Then I should see a preview')
def then_i_should_see_a_preview(step):
    world.page.is_text_present('Preview Questionnaire')

@step(u'When I choose to submit the responses in the preview')
def when_i_choose_to_submit_the_responses_in_the_preview(step):
    world.page.browser.execute_script('document.getElementById("submit_button").click();')

@step(u'Then I should see a message that the submission was successful')
def then_i_should_see_a_message_that_the_submission_was_successful(step):
    sleep(3)
    world.page.is_text_present('Questionnaire Submitted')

@step(u'And the response fields should be disabled')
def and_the_response_fields_should_be_disabled(step):
    world.page.validate_fields_disabled(world.valid_responses)

@step(u'And the action for submit should be replaced with edit')
def and_the_action_for_submit_should_be_replaced_with_edit(step):
    assert world.page.is_element_not_present_by_id('submit_questionnaire_btn')
    assert world.page.is_element_present_by_id('edit_questionnaire_link')

@step(u'And I should see my submitted responses')
def and_i_should_see_my_submitted_responses(step):
    world.page.validate_responses(world.valid_responses)

@step(u'When I select the option to edit my responses')
def when_i_select_the_option_to_edit_my_responses(step):
    world.page.click_by_id('edit_questionnaire_link')

@step(u'Then the response fields should be enabled')
def then_the_response_fields_should_be_enabled(step):
    world.page.validate_fields_enabled(world.valid_responses)

@step(u'Then the action for edit should be replaced with submit')
def then_the_action_for_edit_should_be_replaced_with_submit(step):
    assert world.page.is_element_present_by_id('submit_questionnaire_btn')
    assert world.page.is_element_not_present_by_id('edit_questionnaire_link')