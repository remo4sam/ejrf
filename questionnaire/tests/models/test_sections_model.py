from questionnaire.models.sections import Section, SubSection
from questionnaire.models import Questionnaire, Question, QuestionGroup
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

    def test_section_fields(self):
        section = Section()
        fields = [str(item.attname) for item in section._meta.fields]
        self.assertEqual(8, len(fields))
        for field in ['id', 'created', 'modified', 'title', 'order', 'questionnaire_id', 'name', 'description']:
            self.assertIn(field, fields)

    def test_section_store(self):
        self.failUnless(self.section.id)
        self.assertEqual("Immunisation Coverage", self.section.title)
        self.assertEqual("im cover", self.section.name)
        self.assertEqual("section description", self.section.description)
        self.assertEqual(self.questionnaire, self.section.questionnaire)

    def test_should_know_questions(self):
        self.assertEqual(6, len(self.section.all_questions()))
        self.assertIn(self.question1, self.section.all_questions())
        self.assertIn(self.question2, self.section.all_questions())
        self.assertIn(self.question3, self.section.all_questions())
        self.assertIn(self.question4, self.section.all_questions())
        self.assertIn(self.question5, self.section.all_questions())
        self.assertIn(self.question6, self.section.all_questions())

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
        self.assertEqual(7, len(fields))
        for field in ['id', 'created', 'modified', 'title', 'order', 'section_id', 'description']:
            self.assertIn(field, fields)

    def test_sub_section_store(self):
        self.failUnless(self.section.id)
        self.assertEqual("Infant Immunisation Coverage", self.sub_section.title)
        self.assertEqual(self.section, self.sub_section.section)

    def test_subsection_can_get_its_questions_groups(self):
        sub_group = QuestionGroup.objects.create(subsection=self.sub_section, name="Laboratory Investigation")
        self.assertEqual(1, len(self.sub_section.all_question_groups()))
        self.assertIn(sub_group, self.sub_section.all_question_groups())

    def test_subsection_can_get_its_questions_from_its_groups(self):
        sub_group = QuestionGroup.objects.create(subsection=self.sub_section, name="Laboratory Investigation")
        sub_group.question.add(self.question1, self.question2)

        questions = self.sub_section.all_questions()
        print questions
        self.assertEqual(2, len(questions))
        self.assertIn(self.question1, questions)
        self.assertIn(self.question2, questions)
