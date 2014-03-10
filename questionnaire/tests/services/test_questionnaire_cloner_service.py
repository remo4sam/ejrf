from questionnaire.models import Question, QuestionGroup, Questionnaire, SubSection, Section, QuestionOption, QuestionGroupOrder
from questionnaire.services.questionnaire_cloner import QuestionnaireClonerService
from questionnaire.tests.base_test import BaseTest


class QuestionnaireClonerServiceTest(BaseTest):

    def setUp(self):
        self.questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English", description="From dropbox as given by Rouslan", year=2013, status=Questionnaire.FINALIZED)
        self.section_1 = Section.objects.create(title="Reported Cases of Selected Vaccine Preventable Diseases (VPDs)", order=1,
                                                      questionnaire=self.questionnaire, name="Reported Cases")
        self.section_2 = Section.objects.create(title="Cured Cases of Measles", order=1,
                                                questionnaire=self.questionnaire, name="Cured Cases")

        self.sub_section1 = SubSection.objects.create(title="Reported cases for the year 2013", order=1, section=self.section_1)
        self.sub_section2 = SubSection.objects.create(title="Reported cases for the year", order=2, section=self.section_1)
        self.sub_section3 = SubSection.objects.create(title="Reported cures 2014", order=1, section=self.section_2)
        self.sub_section4 = SubSection.objects.create(title="Reported cures", order=2, section=self.section_2)
        self.primary_question = Question.objects.create(text='Disease', UID='C00003', answer_type='MultiChoice',
                                                        is_primary=True)
        self.option = QuestionOption.objects.create(text="Measles", question=self.primary_question, UID="QO1")
        self.option2 = QuestionOption.objects.create(text="TB", question=self.primary_question, UID="QO2")

        self.question1 = Question.objects.create(text='B. Number of cases tested', UID='C00004', answer_type='Number')

        self.question2 = Question.objects.create(text='C. Number of cases positive',
                                                 instructions="""
                                                 Include only those cases found positive for the infectious agent.
                                                 """,
                                                 UID='C00005', answer_type='Number')

        self.parent10 = QuestionGroup.objects.create(subsection=self.sub_section1, order=1)
        self.parent120 = QuestionGroup.objects.create(subsection=self.sub_section1, order=2)

        self.parent11 = QuestionGroup.objects.create(subsection=self.sub_section2, order=1)
        self.parent12 = QuestionGroup.objects.create(subsection=self.sub_section2, order=2)

        self.parent21 = QuestionGroup.objects.create(subsection=self.sub_section3, order=1)
        self.parent22 = QuestionGroup.objects.create(subsection=self.sub_section3, order=2)

        self.parent31 = QuestionGroup.objects.create(subsection=self.sub_section3, order=1)
        self.parent32 = QuestionGroup.objects.create(subsection=self.sub_section3, order=2)

        self.parent41 = QuestionGroup.objects.create(subsection=self.sub_section4, order=1)
        self.parent42 = QuestionGroup.objects.create(subsection=self.sub_section4, order=2)

        self.parent10.question.add(self.question1, self.question2, self.primary_question)

    def test_returns_all_a_new_questionnaire_instance_when_clone_is_called(self):
        questionnaire, old = QuestionnaireClonerService(self.questionnaire).clone()
        self.assertEqual(old, self.questionnaire)
        self.assertNotEqual(self.questionnaire, questionnaire)
        questionnaires = Questionnaire.objects.all()
        self.assertEqual(2, len(questionnaires))
        self.assertIn(questionnaire, questionnaires)
        self.assertIn(self.questionnaire, questionnaires)
        self.assertEqual(Questionnaire.FINALIZED, old.status)

    def test_returns_all_a_old_sections_on_the_new_questionnaire_instance_when_clone_is_called(self):
        questionnaire, old = QuestionnaireClonerService(self.questionnaire).clone()
        old_sections = old.sections.all()
        self.assertEqual(2, old_sections.count())
        self.assertIn(self.section_1, old_sections)
        self.assertIn(self.section_2, old_sections)

        sections = questionnaire.sections.all()
        self.assertEqual(2, sections.count())
        self.assertNotIn(self.section_1, sections)
        self.assertNotIn(self.section_2, sections)

        section_values = old_sections.values('title', 'name', 'description', 'order')
        for section_data in section_values:
            self.assertEqual(2, Section.objects.filter(**section_data).count())

    def test_returns_all_a_old_sub_sections_on_the_new_questionnaire_instance_when_clone_is_called(self):
        self.assertEqual(4, SubSection.objects.all().count())

        new, old = QuestionnaireClonerService(self.questionnaire).clone()

        self.assertEqual(8, SubSection.objects.all().count())

        old_sections = old.sections.all()
        for section in old_sections:
            subsections = section.sub_sections.all()
            self.assertEqual(2, subsections.count())
            for subsection_values in subsections.values('title', 'description', 'order'):
                self.assertEqual(2, SubSection.objects.filter(**subsection_values).count())

        new_sections = new.sections.all()
        for section in new_sections:
            subsections = section.sub_sections.all()
            self.assertEqual(2, subsections.count())
            for subsection_values in subsections.values('title', 'description', 'order'):
                self.assertEqual(2, SubSection.objects.filter(**subsection_values).count())

    def test_clones_all_groups_from_questionnaire(self):
        self.assertEqual(10, QuestionGroup.objects.all().count())
        new, old = QuestionnaireClonerService(self.questionnaire).clone()
        self.assertEqual(20, QuestionGroup.objects.all().count())

        old_sections = old.sections.all()
        for section in old_sections:
            subsections = section.sub_sections.all()
            for subsection in subsections:
                for group_values in subsection.all_question_groups().values('name', 'instructions', 'parent', 'order', 'allow_multiples'):
                    self.assertEqual(10, QuestionGroup.objects.filter(**group_values).count())

        new_sections = new.sections.all()
        for section in new_sections:
            subsections = section.sub_sections.all()
            for subsection in subsections:
                for group_values in subsection.all_question_groups().values('name', 'instructions', 'parent', 'order', 'allow_multiples'):
                    self.assertEqual(10, QuestionGroup.objects.filter(**group_values).count())

    def test_clones_sub_groups_of_groups_from_questionnaire(self):
        sub_group1 = QuestionGroup.objects.create(subsection=self.sub_section1, order=1, parent=self.parent10)
        sub_group2 = QuestionGroup.objects.create(subsection=self.sub_section1, order=1, parent=self.parent12)
        self.assertEqual(1, QuestionGroup.objects.filter(parent=self.parent10).count())
        self.assertEqual(1, QuestionGroup.objects.filter(parent=self.parent12).count())

        self.assertEqual(12, QuestionGroup.objects.all().count())
        new, old = QuestionnaireClonerService(self.questionnaire).clone()
        self.assertEqual(24, QuestionGroup.objects.all().count())
        self.assertEqual(2, QuestionGroup.objects.filter(subsection=self.sub_section1, parent__in=[self.parent10, self.parent12]).count())
        self.assertEqual(12, len(old.all_groups()))
        self.assertIn(sub_group1, old.all_groups())
        self.assertIn(sub_group2, old.all_groups())
        self.assertEqual(12, len(new.all_groups()))
        self.assertNotIn(sub_group1, new.all_groups())
        self.assertNotIn(sub_group2, new.all_groups())
        self.assertEqual(2, QuestionGroup.objects.filter(subsection__section__in=new.sections.all(), parent__isnull=False).count())

    def test_clones_questions_in_the_questionnaire_with_their_order_objects(self):
        question3 = Question.objects.create(text='B. Number of cases tested', UID=Question.next_uid(), answer_type='Number')
        question4 = Question.objects.create(text='C. Number of cases positive', UID=Question.next_uid(), answer_type='Number')
        QuestionGroupOrder.objects.create(order=1, question_group=self.parent10, question=self.primary_question)
        QuestionGroupOrder.objects.create(order=2, question_group=self.parent10, question=self.question1)
        QuestionGroupOrder.objects.create(order=3, question_group=self.parent10, question=self.question2)
        QuestionGroupOrder.objects.create(order=4, question_group=self.parent120, question=question3)
        QuestionGroupOrder.objects.create(order=5, question_group=self.parent120, question=question4)

        self.assertEqual(5, Question.objects.all().count())
        self.parent10.question.add(question3, question4, self.question1, self.question1)
        new, old = QuestionnaireClonerService(self.questionnaire).clone()
        self.assertEqual(5, Question.objects.all().count())
        self.assertEqual(5, len(old.get_all_questions()))
        self.assertEqual(5, len(new.get_all_questions()))
