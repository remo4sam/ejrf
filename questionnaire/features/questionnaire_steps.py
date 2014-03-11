from time import sleep
from lettuce import step, world
from questionnaire.features.pages.questionnaires import QuestionnairePage
from questionnaire.models import Questionnaire, Section, SubSection, Question, QuestionGroup, QuestionGroupOrder, QuestionOption


@step(u'And I have a questionnaire with sections and subsections')
def and_i_have_a_questionnaire_with_sections_and_subsections(step):
    world.questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English", description="From dropbox as given by Rouslan",
                                                       status=Questionnaire.PUBLISHED)
    world.section_1 = Section.objects.create(title="Section 1 Title Sample", order=1, questionnaire=world.questionnaire, name="Section 1 Name Sample",
                                             description="Section 1 Description")
    world.section_2 = Section.objects.create(title="Section 2 Title Sample", order=2, questionnaire=world.questionnaire, name="Section 2 Name Sample",
                                             description="Section 2 Description")
    world.section_3 = Section.objects.create(title="Section 3 Title Sample", order=3, questionnaire=world.questionnaire, name="Section 3 Name Sample",
                                             description="Section 3 Description")
    world.sub_section = SubSection.objects.create(title="Subsection Title Sample", order=1, section=world.section_1)

@step(u'And I have a question group and questions in that group')
def and_i_have_a_question_group_and_questions_in_that_group(step):
    world.question1 = Question.objects.create(text='Disease', UID='C00001', answer_type='MultiChoice')
    world.question2 = Question.objects.create(text='B. Number of cases tested',
                                              instructions="Enter the total number of cases for which",
                                              UID='C00003', answer_type='Number')

    world.question3 = Question.objects.create(text='C. Number of cases positive',
                                              instructions="Include only those cases the infectious agent.",
                                              UID='C00004', answer_type='Number')

    world.question_group = QuestionGroup.objects.create(subsection=world.sub_section, order=1, name="Immunization", allow_multiples=1)
    world.question_group.question.add(world.question1, world.question3, world.question2)

    QuestionOption.objects.create(text='Option 2', question=world.question1)

@step(u'And I set orders for the questions in the group')
def and_i_set_orders_for_the_questions_in_the_group(step):
    QuestionGroupOrder.objects.create(question=world.question1, question_group=world.question_group, order=1)
    QuestionGroupOrder.objects.create(question=world.question2, question_group=world.question_group, order=2)
    QuestionGroupOrder.objects.create(question=world.question3, question_group=world.question_group, order=3)

@step(u'And I visit that questionnaires section page')
def and_i_visit_that_questionnaires_section_page(step):
    world.page = QuestionnairePage(world.browser, world.section_1)
    world.page.visit()

@step(u'Then I should see the section title and descriptions')
def then_i_should_see_the_section_title_and_descriptions(step):
    world.page.is_text_present(world.section_1.title, world.section_1.description)

@step(u'And I should see the questions')
def then_i_should_see_the_questions(step):
    world.page.is_text_present(world.question1.text,world.question2.text,world.question3.text)

@step(u'And I should see the answer fields')
def and_i_should_see_the_answer_fields(step):
    world.page.validate_fields()

@step(u'And I should see the instructions')
def and_i_should_see_the_instructions(step):
    world.page.validate_instructions(world.question2)

@step(u'And i have a subgroup with questions in that group')
def and_i_have_a_subgroup_with_questions_in_that_group(step):
    world.question_1a = Question.objects.create(text='Disease', UID='C00021', answer_type='MultiChoice')

    world.question_subgroup = QuestionGroup.objects.create(subsection=world.sub_section, order=1,
                                                           parent=world.question_group, name="Immunization subgroup")
    world.question_subgroup.question.add(world.question_1a)

@step(u'And I set question orders for the group and subgroup')
def and_i_set_question_orders_for_the_group_and_subgroup(step):
    QuestionGroupOrder.objects.create(question=world.question_1a, question_group=world.question_group, order=4)

@step(u'Then I should see the group title and description')
def then_i_should_see_the_group_title_and_description(step):
    world.page.is_text_present(world.question_group.name)

@step(u'And I should see the subgroup title and description')
def and_i_should_see_the_subgroup_title_and_description(step):
    world.page.is_text_present(world.question_subgroup.name)

@step(u'When I click on a different section tab')
def when_i_click_on_a_different_section_tab(step):
    world.page.click_by_id("section-%s" % world.section_2.id)

@step(u'Then I should see that section page')
def then_i_should_see_that_section_page(step):
    world.page = QuestionnairePage(world.browser, world.section_2)
    world.page.validate_url()

@step(u'Then I should see an Add More button')
def then_i_should_see_an_add_more_button(step):
    world.page.is_text_present('Add More')

@step(u'When I click the Add More button')
def when_i_click_the_add_more_button(step):
    world.page.click_by_css('.add-more')

@step(u'Then I should see a new question group')
def then_i_should_see_a_new_subsection(step):
    assert(world.page.number_of_elements("Immunization"), 2)

@step(u'When I click the question group delete button')
def when_i_click_the_sub_section_delete_button(step):
    world.page.click_by_css('.delete-more')

@step(u'Then I should not see that question group')
def then_i_should_not_see_that_question_group(step):
    assert(world.page.number_of_elements("Immunization"), 1)
