from lettuce import step, world
from questionnaire.features.pages.extract import ExtractPage
from questionnaire.features.pages.users import LoginPage
from questionnaire.models import Questionnaire, SubSection, Section, QuestionGroup, NumericalAnswer, Region, Country, \
    Organization, Answer, Question, QuestionGroupOrder, AnswerGroup


@step(u'And I logged in the user')
def and_i_logged_in_the_user(step):
    world.page = LoginPage(world.browser)
    world.page.visit()
    data = {'username': world.user.username,
            'password': "pass"}
    world.page.fill_form(data)
    world.page.submit()

@step(u'And I visit the extract page')
def and_i_visit_the_extract_page(step):
    world.page = ExtractPage(world.browser)
    world.page.visit()

@step(u'I should see a list of filter options')
def then_i_should_see_a_list_of_questionnaires(step):
    world.page.is_text_present('Year')
    world.page.is_text_present('Region')
    world.page.is_text_present('Country')
    world.page.is_text_present('Theme')

@step(u'And I have a questionnaires')
def and_i_have_two_questionnaires(step):
    world.questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English",
                                                       description="From dropbox as given by Rouslan", year=2013)
    world.section_1 = Section.objects.create(title="Reported Cases of Selected Vaccine Preventable Diseases (VPDs)",
                                             order=1, questionnaire=world.questionnaire, name="Reported Cases")

    world.sub_section = SubSection.objects.create(title="Reported cases for the year 2013", order=1,
                                                  section=world.section_1)
    world.parent = QuestionGroup.objects.create(subsection=world.sub_section, order=1)

@step(u'And I have questions and their answers')
def and_i_have_questions_and_their_answers(step):
        world.question1 = Question.objects.create(text='what do you drink?', UID='abc123', answer_type='MultiChoice')
        world.question2 = Question.objects.create(text='what do you drink at nite?', UID='abc125', answer_type='MultiChoice')
        world.parent.question.add(world.question1, world.question2)
        world.organisation = Organization.objects.create(name="WHO")
        world.regions = Region.objects.create(name="The Afro", organization=world.organisation)
        world.country = Country.objects.create(name="Uganda", code="UGX")
        world.regions.countries.add(world.country)
        QuestionGroupOrder.objects.create(question=world.question1, question_group=world.parent, order=1)
        QuestionGroupOrder.objects.create(question=world.question2, question_group=world.parent, order=2)

        world.question1_answer = NumericalAnswer.objects.create(question=world.question1, country=world.country,
                                                                status=Answer.SUBMITTED_STATUS,  response=23)
        world.question2_answer = NumericalAnswer.objects.create(question=world.question2, country=world.country,
                                                                status=Answer.SUBMITTED_STATUS, response=1)
        world.answer_group1 = AnswerGroup.objects.create(grouped_question=world.parent, row=1)
        world.answer_group1.answer.add(world.question1_answer, world.question2_answer)


@step(u'When I click the extract link')
def when_i_click_the_extract_link(step):
    world.page.click_by_css('#extract-link')
    world.page = ExtractPage(world.browser)

@step(u'Then I should see the export data button')
def then_i_should_see_the_export_data_button(step):
    world.page.extract_button_present()