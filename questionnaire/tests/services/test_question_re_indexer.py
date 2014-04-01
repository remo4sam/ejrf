from questionnaire.models import Questionnaire, Section, SubSection, Question, QuestionOption, QuestionGroup, \
    QuestionGroupOrder
from questionnaire.services.question_re_indexer import QuestionReIndexer
from questionnaire.tests.base_test import BaseTest


class TestQuestionReIndexer(BaseTest):
    def setUp(self):
        self.questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English", status=Questionnaire.PUBLISHED)

        self.section_1 = Section.objects.create(title="Reported Cases of Selected Vaccine Preventable Diseases (VPDs)",
                                                order=1,
                                                questionnaire=self.questionnaire, name="Reported Cases")

        self.sub_section = SubSection.objects.create(title="Reported cases for the year 2013", order=1,
                                                     section=self.section_1)

        self.question1 = Question.objects.create(text='Disease', UID='C00001', answer_type='MultiChoice')
        self.question2 = Question.objects.create(text='B. Number of cases tested',
                                                 instructions="Enter the total number of cases for which specimens were collected, and tested in laboratory",
                                                 UID='C00003', answer_type='Number')

        self.question3 = Question.objects.create(text='C. Number of cases positive',
                                                 instructions="Include only those cases found positive for the infectious agent.",
                                                 UID='C00004', answer_type='Number')

        self.option1 = QuestionOption.objects.create(text='tusker lager', question=self.question1)
        self.option2 = QuestionOption.objects.create(text='tusker lager1', question=self.question1)
        self.option3 = QuestionOption.objects.create(text='tusker lager2', question=self.question1)

        self.question_group = QuestionGroup.objects.create(subsection=self.sub_section, order=1)
        self.question_group.question.add(self.question1, self.question3, self.question2)

        self.order1 = QuestionGroupOrder.objects.create(question_group=self.question_group, question=self.question1,
                                                        order=1)
        self.order2 = QuestionGroupOrder.objects.create(question_group=self.question_group, question=self.question2,
                                                        order=2)
        self.order3 = QuestionGroupOrder.objects.create(question_group=self.question_group, question=self.question3,
                                                        order=3)
        self.data = {'Number-0-response': ["%d, 0" % self.order3.id],
                     'Text-1-response': ["%d, 1" % self.order2.id],
                     'Text-0-response': ["%d, 2" % self.order1.id]}

    def test_reorder_questions(self):
        dirty_data_query_dict = self.cast_to_queryDict(self.data)
        QuestionReIndexer(dirty_data_query_dict).reorder_questions()
        updated_orders = self.question_group.question_orders()
        self.assertEqual(3, updated_orders.count())
        self.assertEqual(self.order1, updated_orders.get(order=3))
        self.assertEqual(self.order2, updated_orders.get(order=2))
        self.assertEqual(self.order3, updated_orders.get(order=1))

    def test_get_old_orders(self):
        expected = {self.order1: ["%s" % self.order1.id, " %s" % 2],
                    self.order2: ["%s" % self.order2.id, " %s" % 1],
                    self.order3: ["%s" % self.order3.id, " %s" % 0]}
        dirty_data_query_dict = self.cast_to_queryDict(self.data)
        question_re_indexer = QuestionReIndexer(dirty_data_query_dict)
        self.assertEqual(expected, question_re_indexer.get_old_orders())

    def test_clean_posted_data(self):
        dirty_data = {u'Text-3-response': [u'', u'179,5'], u'Text-6-response': [u'', u'182,6'],
                      u'Text-5-response': [u'', u'181,4'],
                      u'Number-0-response': [u'', u'183,7'], u'Text-0-response': [u'', u'176,0'],
                      u'Text-2-response': [u'', u'178,3'], u'Text-4-response': [u'', u'180,2'],
                      u'csrfmiddlewaretoken': [u'f5YpJke56IFgXPxEq2H3jhrWMSDGHMnn'],
                      u'Text-1-response': [u'', u'177,1']}

        dirty_data_query_dict = self.cast_to_queryDict(dirty_data)
        cleaned_data = {u'Text-3-response': [u'179', u'5'], u'Text-6-response': [u'182', u'6'],
                        u'Text-5-response': [u'181', u'4'],
                        u'Number-0-response': [u'183', u'7'], u'Text-0-response': [u'176', u'0'],
                        u'Text-2-response': [u'178',u'3'], u'Text-4-response': [u'180', u'2'],
                        u'Text-1-response': [u'177',u'1']}

        question_re_indexer = QuestionReIndexer(dirty_data_query_dict)
        self.assertEqual(cleaned_data, question_re_indexer.clean_data_posted())


    def test_is_allowed(self):
        question_re_indexer = QuestionReIndexer({})
        self.assertTrue(question_re_indexer.is_allowed("Text-3-response"))
        self.assertFalse(question_re_indexer.is_allowed("Beer-3-response"))
        self.assertFalse(question_re_indexer.is_allowed("csrfmiddlewaretoken"))

    def test_clean_values(self):
        dirty_values = u'179,5'
        question_re_indexer = QuestionReIndexer({})
        self.assertEqual([u'179',u'5'], question_re_indexer.clean_values(dirty_values))
