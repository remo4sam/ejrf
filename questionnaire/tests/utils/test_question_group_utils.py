from questionnaire.models import Question, QuestionGroupOrder, QuestionOption, QuestionGroup, SubSection, Section, Questionnaire
from questionnaire.tests.base_test import BaseTest
from questionnaire.utils.model_utils import map_question_type_with


class QuestionGroupUtilTest(BaseTest):
    def setUp(self):
        self.questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English")

        self.section1 = Section.objects.create(title="Reported Cases of Selected Vaccine", order=1,
                                               questionnaire=self.questionnaire, name="Reported Cases")

        self.sub_section = SubSection.objects.create(title="subsection 1", order=1, section=self.section1)
        self.sub_section2 = SubSection.objects.create(title="subsection 2", order=2, section=self.section1)

        self.question_group = QuestionGroup.objects.create(subsection=self.sub_section, order=1, grid=True, display_all=True)

        self.question1 = Question.objects.create(text='Favorite beer 1', UID='C00001', answer_type='MultiChoice', is_primary=True)
        self.option1 = QuestionOption.objects.create(text='tusker lager', question=self.question1)
        self.option2 = QuestionOption.objects.create(text='tusker lager1', question=self.question1)
        self.option3 = QuestionOption.objects.create(text='tusker lager2', question=self.question1)

        self.question2 = Question.objects.create(text='question 2', instructions="instruction 2",
                                                 UID='C00002', answer_type='Text')

        self.question3 = Question.objects.create(text='question 3', instructions="instruction 3",
                                                 UID='C00003', answer_type='Number')

        self.question4 = Question.objects.create(text='question 4', instructions="instruction 4",
                                                 UID='C00005', answer_type='Date')
        self.question_group.question.add(self.question1, self.question3, self.question2, self.question4)
        self.available_answer_types = ['Date', 'Number', 'MultiChoice', 'Text']
        self.order1 = QuestionGroupOrder.objects.create(question=self.question1, question_group=self.question_group, order=1)
        self.order2 = QuestionGroupOrder.objects.create(question=self.question2, question_group=self.question_group, order=2)
        self.order3 = QuestionGroupOrder.objects.create(question=self.question3, question_group=self.question_group, order=3)
        self.order4 = QuestionGroupOrder.objects.create(question=self.question4, question_group=self.question_group, order=4)

        self.empty_mapping = {type_: [] for type_ in self.available_answer_types}

    def test_maps_question_type_with_orders(self):
        expected_map = {self.question4.answer_type: [{'option': self.option1, 'order': self.order4}],
                        self.question1.answer_type: [{'option': self.option1, 'order': self.order1}], 'Number': [], 'Text': []}

        orders = self.question_group.orders.filter(question__in=[self.question1, self.question4])
        map_question_type_with(orders, self.empty_mapping, option=self.option1)
        self.assertEqual(expected_map, self.empty_mapping)

    def test_maps_multiple_questions_type_with_orders_when_they_are_of_same_type(self):
        question5 = Question.objects.create(text='question 5', instructions="instruction 5", UID='04444', answer_type='Date')
        self.question_group.question.add(question5)
        order5 = QuestionGroupOrder.objects.create(question=question5, question_group=self.question_group, order=5)

        expected_map = {self.question4.answer_type: [{'option': self.option1, 'order': self.order4}, {'option': self.option1, 'order': order5}],
                        self.question1.answer_type: [{'option': self.option1, 'order': self.order1}], 'Number': [], 'Text': []}

        orders = self.question_group.orders.filter(question__in=[self.question1, self.question4, question5])
        map_question_type_with(orders,  self.empty_mapping, option=self.option1)
        self.assertEqual(expected_map, self.empty_mapping)