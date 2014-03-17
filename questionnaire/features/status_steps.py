from lettuce import step, world
from questionnaire.features.pages.home import HomePage
from questionnaire.models import Region, Organization, Country, Questionnaire, Section, SubSection, Question, QuestionGroup, TextAnswer, Answer


@step(u'And I have regions and countries')
def and_i_have_regions_and_countries(step):
    world.organization = Organization.objects.create(name='WHO')

    world.region_afro = Region.objects.create(name='AFR', organization=world.organization)
    world.region_euro = Region.objects.create(name='EUR', organization=world.organization)

    world.country_uganda = Country.objects.create(name='Uganda')
    world.country_kenya = Country.objects.create(name='Kenya')

    world.region_afro.countries.add(world.country_uganda, world.country_kenya)


@step(u'And I have published Questionnaires to a region')
def and_i_have_published_questionnaires_to_a_region(step):
    world.questionnaire_afro = Questionnaire.objects.create(name="JRF Core Status", description="Questionnaire Status",
                                                            status=Questionnaire.PUBLISHED, region=world.region_afro)

    world.section_afro = Section.objects.create(order=0, title="Section AFRO", description="Description",
                                                questionnaire=world.questionnaire_afro, name="Cover page")
    world.subsection_afro = SubSection.objects.create(order=1, section=world.section_afro)

    world.question1 = Question.objects.create(text='Name of person in Ministry of Health', UID='C001',
                                              answer_type='Text')

    parent = QuestionGroup.objects.create(subsection=world.subsection_afro, order=1)
    parent.question.add(world.question1)


@step(u'I am viewing the homepage')
def when_i_am_viewing_the_homepage(step):
    world.page = HomePage(world.browser)
    world.page.visit()


@step(u'Then I should see the regions listed')
def then_i_should_see_the_regions_listed(step):
    world.page.is_text_present(world.region_afro.name, world.region_euro.name)


@step(u'I select a region in the region list')
def when_i_select_a_region(step):
    world.page.click_link_by_partial_href('#collapse%s' % world.region_afro.id)


@step(u'Then I should see the countries in that region')
def then_i_should_see_countries_in_that_region(step):
    world.page.is_text_present(world.country_uganda.name, world.country_kenya.name)


@step(u'And I select that region in the region list')
def and_i_select_that_region_in_the_region_list(step):
    step.given('I select a region in the region list')


@step(u'And the data submitters in that region have "([^"]*)"')
def and_the_data_submitters_in_that_region_have_group1(step, status):
    if status == 'started responding':
        world.answer_qn1 = TextAnswer.objects.create(question=world.question1, country=world.country_uganda,
                                                     status=Answer.DRAFT_STATUS, response='This UG Data Submitter')
        world.answer_qn1 = TextAnswer.objects.create(question=world.question1, country=world.country_kenya,
                                                     status=Answer.DRAFT_STATUS, response='This KY Data Submitter')
    if status == 'submitted responses':
        world.answer_qn1 = TextAnswer.objects.create(question=world.question1, country=world.country_uganda,
                                                     status=Answer.SUBMITTED_STATUS, response='This UG Data Submitter')
        world.answer_qn1 = TextAnswer.objects.create(question=world.question1, country=world.country_kenya,
                                                     status=Answer.SUBMITTED_STATUS, response='This KY Data Submitter')


@step(u'Then I should see the status of responses for countries in that region as "([^"]*)"')
def then_i_should_see_the_status_of_responses_for_countries_in_that_region_as_group1(step, result):
    world.page.is_text_present(result)