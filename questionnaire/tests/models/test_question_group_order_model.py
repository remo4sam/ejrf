from questionnaire.models import QuestionGroup, SubSection, Section, Questionnaire, Question
from questionnaire.models.question_group_orders import QuestionGroupOrder
from questionnaire.tests.base_test import BaseTest


class QuestionGroupOrderTest(BaseTest):
    def setUp(self):
        self.question = Question.objects.create(text='Uganda Revision 2014 what what?', UID='abc123', answer_type='Text')
        self.questionnaire = Questionnaire.objects.create(name="Uganda Revision 2014", description="some description")
        self.section = Section.objects.create(title="Immunisation Coverage", order=1, questionnaire=self.questionnaire)
        self.sub_section = SubSection.objects.create(title="Immunisation Extra Coverage", order=1, section=self.section)
        self.grouped_question = QuestionGroup.objects.create(subsection=self.sub_section, order=1)

    def test_question_group_order_fields(self):
        question_group_order = QuestionGroupOrder()
        fields = [str(item.attname) for item in question_group_order._meta.fields]
        self.assertEqual(6, len(fields))
        for field in ['id', 'created', 'modified', 'order', 'question_group_id', 'question_id']:
            self.assertIn(field, fields)

    def test_store(self):
        question_group_order = QuestionGroupOrder.objects.create(question_group=self.grouped_question, question=self.question, order=1)
        self.failUnless(question_group_order.id)
        self.assertEqual(self.question, question_group_order.question)
        self.assertEqual(self.grouped_question, question_group_order.question_group)

    def test_order_knows_it_is_last_of_his_type_in_group(self):
        last_text_question = Question.objects.create(text='another text q', UID='123', answer_type='Text')
        number_question = Question.objects.create(text='number q', UID='abc', answer_type='Number')
        question_group_order = QuestionGroupOrder.objects.create(question_group=self.grouped_question, question=self.question, order=1)
        another_question_group_order = QuestionGroupOrder.objects.create(question_group=self.grouped_question, question=last_text_question, order=2)
        number_group_order = QuestionGroupOrder.objects.create(question_group=self.grouped_question, question=number_question, order=3)

        self.assertFalse(question_group_order.is_last_answer_type_in_group())
        self.assertTrue(another_question_group_order.is_last_answer_type_in_group())
        self.assertTrue(number_group_order.is_last_answer_type_in_group())