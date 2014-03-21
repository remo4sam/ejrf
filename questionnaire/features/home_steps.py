from lettuce import step, world
import time
from questionnaire.models import Organization, Region, Country, Question, SubSection, Questionnaire, Section, \
    QuestionOption, QuestionGroup, NumericalAnswer, Answer, QuestionGroupOrder, AnswerGroup


@step(u'Given I two have regions and three countries in those regions')
def given_i_two_have_regions_and_three_countries_in_those_regions(step):
    world.organisation = Organization.objects.create(name="WHO")

    world.afro = Region.objects.create(name="Afro", organization=world.organisation)
    world.uganda = Country.objects.create(name="Uganda", code="UGX")
    world.rwanda = Country.objects.create(name="Rwanda", code="RWA")
    world.kenya = Country.objects.create(name="Kenya", code="KYE")
    world.afro.countries.add(world.uganda, world.rwanda)

    world.asean = Region.objects.create(name="Asean", organization=world.organisation)
    world.singapore = Country.objects.create(name="Singapore", code="SNP")
    world.malyasia = Country.objects.create(name="Malyasia", code="MLS")
    world.india = Country.objects.create(name="India", code="IND")
    world.asean.countries.add(world.malyasia, world.singapore)


@step(u'Given I have a questionnaire published one of the regions')
def given_i_have_a_questionnaire_published_one_of_the_regions(step):
    world.questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English", year=2013, region=world.afro, status=Questionnaire.PUBLISHED)
    world.section_1 = Section.objects.create(title="Reported Cases of Selected Vaccine Preventable Diseases (VPDs)", order=1,
                                             questionnaire=world.questionnaire, name="Reported Cases")
    world.sub_section = SubSection.objects.create(title="Reported cases for the year 2013", order=1, section=world.section_1)
    world.primary_question = Question.objects.create(text='Disease', UID='C00003', answer_type='MultiChoice', is_primary=True)
    world.option = QuestionOption.objects.create(text="Measles", question=world.primary_question, UID="QO1")
    world.option2 = QuestionOption.objects.create(text="TB", question=world.primary_question, UID="QO2")
    world.question1 = Question.objects.create(text='B. Number of cases tested', UID='C00004', answer_type='Number')
    world.question2 = Question.objects.create(text='C. Number of cases positive', UID='C00005', answer_type='Number')

    world.parent = QuestionGroup.objects.create(subsection=world.sub_section, order=1)
    world.parent.question.add(world.question1, world.question2, world.primary_question)
    QuestionGroupOrder.objects.create(question=world.primary_question, question_group=world.parent, order=1)
    QuestionGroupOrder.objects.create(question=world.question1, question_group=world.parent, order=2)
    QuestionGroupOrder.objects.create(question=world.question2, question_group=world.parent, order=3)



@step(u'And one of the countries in that region has  two versions of answers for the questionnaire')
def and_one_of_the_countries_in_that_region_has_two_versions_of_answers_for_the_questionnaire(step):
    world.answer_1 = NumericalAnswer.objects.create(question=world.question2, country=world.rwanda, status=Answer.SUBMITTED_STATUS,
                                              response=22, questionnaire=world.questionnaire)
    world.answer_2 = NumericalAnswer.objects.create(question=world.question1, country=world.rwanda, status=Answer.SUBMITTED_STATUS,
                                              response=23, questionnaire=world.questionnaire)
    answer_group_2 = AnswerGroup.objects.create(grouped_question=world.parent, row=1)
    answer_group_2.answer.add(world.answer_2, world.answer_1)

    answer_1 = NumericalAnswer.objects.create(question=world.question2, country=world.rwanda, status=Answer.DRAFT_STATUS,
                                                    response=10, version=2, questionnaire=world.questionnaire)
    answer_2 = NumericalAnswer.objects.create(question=world.question1, country=world.rwanda, status=Answer.DRAFT_STATUS,
                                                    response=100, version=2, questionnaire=world.questionnaire)
    answer_group_2 = AnswerGroup.objects.create(grouped_question=world.parent, row=2)
    answer_group_2.answer.add(answer_2, answer_1)


@step(u'When I expand that region')
def when_i_expand_that_region(step):
    world.page.click_by_id('region-%s-collapse' % world.afro.id)

@step(u'Then I should see the country with started status')
def then_i_should_see_the_country_with_started_status(step):
    world.page.is_text_present("In Progress")

@step(u'And when I click the country')
def and_when_i_click_the_country(step):
    world.page.click_by_id('region-%s-country-%s-collapse' % (world.afro.id, world.rwanda.id))

@step(u'Then I should see its versions listed under it')
def then_i_should_see_its_versions_listed_under_it(step):
    world.page.is_text_present("Version 1", "Version 2")

@step(u'When I click on version 1')
def when_i_click_on_version_1(step):
    world.page.click_by_id('preview-version-%s' % world.answer_1.version)

@step(u'Then I should see the submitted answers in a modal')
def then_i_should_see_the_submitted_answers_in_a_modal(step):
    world.page.is_text_present("Preview Questionnaire")
    world.page.is_element_present_by_value("%s" % world.answer_1.response)
    world.page.is_element_present_by_value("%s" % world.answer_2.response)