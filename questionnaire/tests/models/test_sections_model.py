from questionnaire.models.sections import Section, SubSection
from questionnaire.models import Questionnaire, Question, QuestionGroup, QuestionGroupOrder, QuestionOption
from questionnaire.tests.base_test import BaseTest


class SectionTest(BaseTest):
    def setUp(self):
        self.questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English", description="From dropbox as given by Rouslan")

        self.section = Section.objects.create(title="Immunisation Coverage", order=1, description='section description',
                                                      questionnaire=self.questionnaire, name="im cover")

        self.sub_section = SubSection.objects.create(title="subsection 1", order=1, section=self.section)
        self.sub_section2 = SubSection.objects.create(title="subsection 2", order=2, section=self.section)

        self.question_group = QuestionGroup.objects.create(subsection=self.sub_section, order=1)
        self.question_group2 = QuestionGroup.objects.create(subsection=self.sub_section, order=2)
        self.question_group3 = QuestionGroup.objects.create(subsection=self.sub_section2, order=1)

        self.question1 = Question.objects.create(text='question 1', UID='C00001', answer_type='MultiChoice')
        self.question2 = Question.objects.create(text='question 2', instructions="instruction 2",
                                                    UID='C00002', answer_type='Text')

        self.question3 = Question.objects.create(text='question 3', instructions="instruction 3",
                                            UID='C00003', answer_type='Number')

        self.question4 = Question.objects.create(text='question 4', UID='C00004', answer_type='MultiChoice')
        self.question5 = Question.objects.create(text='question 4', instructions="instruction 2",
                                                    UID='C00005', answer_type='Number')
        self.question6 = Question.objects.create(text='question 6', instructions="instruction 3",
                                            UID='C00006', answer_type='Date')

        self.question_group.question.add(self.question1, self.question3, self.question2)
        self.question_group2.question.add(self.question4, self.question5)
        self.question_group3.question.add(self.question6)

        QuestionGroupOrder.objects.create(question=self.question1, question_group=self.question_group, order=1)
        QuestionGroupOrder.objects.create(question=self.question2, question_group=self.question_group, order=2)
        QuestionGroupOrder.objects.create(question=self.question3, question_group=self.question_group, order=3)
        QuestionGroupOrder.objects.create(question=self.question4, question_group=self.question_group2, order=1)
        QuestionGroupOrder.objects.create(question=self.question5, question_group=self.question_group2, order=2)
        QuestionGroupOrder.objects.create(question=self.question6, question_group=self.question_group3, order=1)

    def test_section_fields(self):
        section = Section()
        fields = [str(item.attname) for item in section._meta.fields]
        self.assertEqual(9, len(fields))
        for field in ['id', 'created', 'modified', 'title', 'order', 'questionnaire_id', 'name', 'description', 'region_id']:
            self.assertIn(field, fields)

    def test_section_store(self):
        self.failUnless(self.section.id)
        self.assertEqual("Immunisation Coverage", self.section.title)
        self.assertEqual("im cover", self.section.name)
        self.assertEqual("section description", self.section.description)
        self.assertEqual(self.questionnaire, self.section.questionnaire)
        self.assertIsNone(self.section.region)

    def test_should_order_questions(self):
        questions = self.section.ordered_questions()
        self.assertEqual(6, len(questions))
        self.assertEqual(self.question1, questions[0])
        self.assertEqual(self.question2, questions[1])
        self.assertEqual(self.question3, questions[2])
        self.assertEqual(self.question4, questions[3])
        self.assertEqual(self.question5, questions[4])
        self.assertEqual(self.question6, questions[5])

    def test_ordered_questions_should_repeat_questions_in_multiple_groups(self):
        self.question_group3.question.add(self.question4, self.question5)
        QuestionGroupOrder.objects.create(question=self.question4, question_group=self.question_group3, order=2)
        QuestionGroupOrder.objects.create(question=self.question5, question_group=self.question_group3, order=3)

        questions = self.section.ordered_questions()
        self.assertEqual(8, len(questions))
        self.assertEqual(self.question1, questions[0])
        self.assertEqual(self.question2, questions[1])
        self.assertEqual(self.question3, questions[2])
        self.assertEqual(self.question4, questions[3])
        self.assertEqual(self.question5, questions[4])
        self.assertEqual(self.question6, questions[5])
        self.assertEqual(self.question4, questions[6])
        self.assertEqual(self.question5, questions[7])

    def test_absolute_url(self):
        absolute_url = '/questionnaire/entry/%s/section/%s/' % (self.questionnaire.id, self.section.id)
        self.assertEqual(absolute_url, self.section.get_absolute_url())

    def test_gets_next_order(self):
        self.assertEqual(2, Section.get_next_order(self.questionnaire))

    def test_next_order_starts_from_0_if_no_sections_exists_in_a_questionnaire(self):
        Section.objects.filter(questionnaire=self.questionnaire).delete()
        self.assertEqual(0, Section.get_next_order(self.questionnaire))

    def test_mapped_question_orders(self):
        grid_question_group = QuestionGroup.objects.create(subsection=self.sub_section, order=11, grid=True, display_all=True)
        self.question1.is_primary = True
        self.question1.save()
        self.option1 = QuestionOption.objects.create(text='tusker lager', question=self.question1)
        self.option2 = QuestionOption.objects.create(text='tusker lager1', question=self.question1)
        self.option3 = QuestionOption.objects.create(text='tusker lager2', question=self.question1)

        grid_question_group.question.add(self.question1, self.question2, self.question3, self.question6)

        order1 = QuestionGroupOrder.objects.create(question=self.question1, question_group=grid_question_group, order=1)
        order2 = QuestionGroupOrder.objects.create(question=self.question2, question_group=grid_question_group, order=2)
        order3 = QuestionGroupOrder.objects.create(question=self.question3, question_group=grid_question_group, order=3)
        order6 = QuestionGroupOrder.objects.create(question=self.question6, question_group=grid_question_group, order=4)

        type_order_mapping = self.section.mapped_question_orders()

        for option in self.question1.options.all():
            for order in grid_question_group.orders.all():
                grid_question_group.map_orders_with_answer_type(type_order_mapping)
                self.assertIn({'option': option, 'order': order}, type_order_mapping[order.question.answer_type])

        for group in [self.question_group, self.question_group2, self.question_group3]:
            for order in group.orders.order_by('order'):
                self.assertIn({'option': '', 'order': order}, type_order_mapping[order.question.answer_type])


class SubSectionTest(BaseTest):
    def setUp(self):
        self.questionnaire = Questionnaire.objects.create(name="Uganda Revision 2014", description="some description")
        self.section = Section.objects.create(title="Immunisation Coverage", order=1,
                                              questionnaire=self.questionnaire, name="im cover" , description="section description")
        self.sub_section = SubSection.objects.create(title="Infant Immunisation Coverage", order=1, section=self.section)
        self.question1 = Question.objects.create(text='question 1', UID='C00001', answer_type='MultiChoice')
        self.question2 = Question.objects.create(text='question 2', instructions="instruction 2",
                                                    UID='C00002', answer_type='Text')

    def test_sub_section_fields(self):
        sub_section = SubSection()
        fields = [str(item.attname) for item in sub_section._meta.fields]
        self.assertEqual(8, len(fields))
        for field in ['id', 'created', 'modified', 'title', 'order', 'section_id', 'description', 'region_id']:
            self.assertIn(field, fields)

    def test_sub_section_store(self):
        self.failUnless(self.section.id)
        self.assertEqual("Infant Immunisation Coverage", self.sub_section.title)
        self.assertEqual(self.section, self.sub_section.section)
        self.assertIsNone(self.sub_section.region)

    def test_subsection_can_get_its_questions_groups(self):
        sub_group = QuestionGroup.objects.create(subsection=self.sub_section, name="Laboratory Investigation")
        self.assertEqual(1, len(self.sub_section.all_question_groups()))
        self.assertIn(sub_group, self.sub_section.all_question_groups())

    def test_subsection_can_get_its_questions_from_its_groups(self):
        sub_group = QuestionGroup.objects.create(subsection=self.sub_section, name="Laboratory Investigation")
        sub_group.question.add(self.question1, self.question2)

        questions = self.sub_section.all_questions()
        self.assertEqual(2, len(questions))
        self.assertIn(self.question1, questions)
        self.assertIn(self.question2, questions)

    def test_should_know_all_parent_groups(self):
        group1 = QuestionGroup.objects.create(subsection=self.sub_section, name="group 1")
        group2 = QuestionGroup.objects.create(subsection=self.sub_section, name="group 2")
        sub_group = QuestionGroup.objects.create(subsection=self.sub_section, name="subgroup 1", parent=group1)

        question = Question.objects.create(text='Disease', UID='C00003', answer_type='MultiChoice')
        group1.question.add(question)
        group2.question.add(question)

        known_groups = self.sub_section.parent_question_groups()

        self.assertEqual(2, len(known_groups))
        self.assertIn(group1, known_groups)
        self.assertIn(group2, known_groups)
        self.assertNotIn(sub_group, known_groups)

    def test_should_know_has_at_least_two_parent_groups(self):
        group1 = QuestionGroup.objects.create(subsection=self.sub_section, name="group 1")
        group2 = QuestionGroup.objects.create(subsection=self.sub_section, name="group 2")
        sub_section2 = SubSection.objects.create(title="subsection 2", order=2, section=self.section)
        group3 = QuestionGroup.objects.create(subsection=sub_section2, name="group of subsection2")
        sub_group = QuestionGroup.objects.create(subsection=self.sub_section, name="subgroup 1", parent=group1)

        question = Question.objects.create(text='Disease', UID='C00003', answer_type='MultiChoice')
        group1.question.add(question)
        group2.question.add(question)

        self.assertTrue(self.sub_section.has_at_least_two_groups())
        self.assertFalse(sub_section2.has_at_least_two_groups())

    def test_gets_next_order(self):
        self.assertEqual(2, SubSection.get_next_order(self.section.id))

    def test_next_order_starts_from_0_if_no_sections_exists_in_a_questionnaire(self):
        SubSection.objects.filter(section=self.section).delete()
        self.assertEqual(0, SubSection.get_next_order(self.section.id))

    def test_absolute_url(self):
        absolute_url = '/questionnaire/entry/%s/section/%s/' % (self.questionnaire.id, self.sub_section.section.id)
        self.assertEqual(absolute_url, self.sub_section.get_absolute_url())

