from time import sleep
from lettuce import step, world
from questionnaire.features.pages.questionnaires import QuestionnairePage
from questionnaire.models import Questionnaire, Section, SubSection, Question, QuestionGroup, QuestionGroupOrder, QuestionOption

@step(u'And I have a grid group with all options of the primary question showable')
def and_i_have_a_grid_group_with_all_options_of_the_primary_question_showable(step):
    world.grid_group = QuestionGroup.objects.create(subsection=world.sub_section, order=1, grid=True, display_all=True)

@step(u'And I have 3 questions in that group one of which is primary')
def and_i_have_3_questions_in_that_group_one_of_which_is_primary(step):
    world.question1 = Question.objects.create(text='Disease', UID='C00001', answer_type='MultiChoice', is_primary=True)
    question2 = Question.objects.create(text='Total Cases', UID='C00002', answer_type='Number',
                                        instructions="Include only those cases found positive for the infectious.")

    world.question3 = Question.objects.create(text='Number of cases tested', UID='C00003', answer_type='Number')

    world.question4 = Question.objects.create(text='Number of cases positive', UID='C00004', answer_type='Number')
    world.question5 = Question.objects.create(text='Number of cases positive', UID='004404', answer_type='Number')
    world.grid_group.question.add(world.question1, question2, world.question5)

    world.option1 = QuestionOption.objects.create(text="Diphteria", question=world.question1)
    world.option2 = QuestionOption.objects.create(text="Measles", question=world.question1)
    world.option3 = QuestionOption.objects.create(text="Pertussis", question=world.question1)
    world.option4 = QuestionOption.objects.create(text="Yellow fever", question=world.question1)
    world.option5 = QuestionOption.objects.create(text="Mumps", question=world.question1)
    world.option6 = QuestionOption.objects.create(text="Rubella", question=world.question1)
    QuestionGroupOrder.objects.create(question=world.question1, question_group=world.grid_group, order=1)
    QuestionGroupOrder.objects.create(question=question2, question_group=world.grid_group, order=2)
    QuestionGroupOrder.objects.create(question=world.question3, question_group=world.grid_group, order=3)
    QuestionGroupOrder.objects.create(question=world.question4, question_group=world.grid_group, order=4)
    QuestionGroupOrder.objects.create(question=world.question5, question_group=world.grid_group, order=5)


@step(u'Then I should see that grid with all the options of the primary question shown')
def then_i_should_see_that_grid_with_all_the_options_of_the_primary_question_shown(step):
    for i in range(1, 5):
        world.page.is_text_present(eval("world.option%d" % i).text)

@step(u'And I have a sub group in that group with two questions')
def and_i_have_a_sub_group_in_that_group_with_two_questions(step):
    sub_group = QuestionGroup.objects.create(subsection=world.sub_section, order=2, grid=True,
                                             name="Labaratory Investigation",
                                             display_all=True, parent=world.grid_group,
                                             instructions="Include only those cases found positive.")
    sub_group.question.add(world.question3, world.question4)

@step(u'When I respond the questions')
def when_i_respond_the_questions(step):
    data ={ }
    counter =0
    for index, option in  enumerate(world.question1.options.all()):
        data['MultiChoice-%d-response'%index] = option.id
        for i in range(4):
            data['Number-%d-response'%counter] = counter
            counter +=1
    world.valid_responses = data.copy()

    world.page.fill_form(data)

@step(u'And I should see my responses in the form')
def and_i_should_see_my_responses_in_the_form(step):
    assert False, 'This step must be implemented'