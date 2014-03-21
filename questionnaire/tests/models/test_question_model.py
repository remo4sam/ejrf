from django.db import IntegrityError
from questionnaire.models import Questionnaire, Section, SubSection, Organization, Region, Country, QuestionGroup, \
    NumericalAnswer, Answer, QuestionGroupOrder, AnswerGroup, MultiChoiceAnswer, TextAnswer, DateAnswer
from questionnaire.models.questions import Question, QuestionOption
from questionnaire.tests.base_test import BaseTest


class QuestionTest(BaseTest):
    def setUp(self):
        self.questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English",
                                                          description="From dropbox as given by Rouslan")
        self.section_1 = Section.objects.create(title="Reported Cases of Selected Vaccine Preventable Diseases (VPDs)",
                                                order=1,
                                                questionnaire=self.questionnaire, name="Reported Cases")
        self.sub_section_1 = SubSection.objects.create(title="Reported cases for the year 2013", order=1,
                                                       section=self.section_1)
        self.sub_section_2 = SubSection.objects.create(title="Another", order=2, section=self.section_1)
        self.organisation = Organization.objects.create(name="WHO")
        self.regions = Region.objects.create(name="The Afro", organization=self.organisation)
        self.country = Country.objects.create(name="Uganda")
        self.regions.countries.add(self.country)
        self.question1 = Question.objects.create(text='B. Number of cases tested',
                                                 instructions="instructions hahaha",
                                                 UID='C00003', answer_type='Number')
        self.parent_group = QuestionGroup.objects.create(subsection=self.sub_section_1, name="Laboratory Investigation")
        self.parent_group.question.add(self.question1)

        self.question1_answer = NumericalAnswer.objects.create(question=self.question1, country=self.country,
                                                               status=Answer.SUBMITTED_STATUS, response=23)
        self.question1_answer_2 = NumericalAnswer.objects.create(question=self.question1, country=self.country,
                                                                 status=Answer.SUBMITTED_STATUS, response=1)

    def test_question_unicode(self):
        self.assertEqual(str(self.question1), 'B. Number of cases tested'.encode('utf8'))

    def test_question_knows_its_in_questionnaire(self):
        question1 = Question.objects.create(text='B. Number of cases tested', UID='00023', answer_type='Number')
        self.assertFalse(question1.is_assigned_to(self.questionnaire))

    def test_question_knows_groups_it_is_in_given_a_questionnaire(self):
        parent_group_2 = QuestionGroup.objects.create(subsection=self.sub_section_1, name="group", order=2)
        parent_group_2.question.add(self.question1)

        question_groups = self.question1.question_groups_in(self.questionnaire)
        self.assertEqual(2, question_groups.count())
        self.assertIn(self.parent_group, question_groups)
        self.assertIn(parent_group_2, question_groups)

    def test_question_knows_all_its_questionnaire(self):
        other_questionnaire = Questionnaire.objects.create(name="other qnaire",description="haha")
        section_1 = Section.objects.create(title="section 1", order=1, questionnaire=other_questionnaire, name="ha")
        sub_section_1 = SubSection.objects.create(title="subs1", order=1, section=section_1)
        parent_group = QuestionGroup.objects.create(subsection=sub_section_1, name="group")
        parent_group.question.add(self.question1)

        questionnaires = self.question1.questionnaires()
        self.assertEqual(2, questionnaires.count())
        self.assertIn(self.questionnaire, questionnaires)
        self.assertIn(other_questionnaire, questionnaires)

    def test_question_knows_its_not_in_questionnaire(self):
        self.assertTrue(self.question1.is_assigned_to(self.questionnaire))

    def test_question_fields(self):
        question = Question()
        fields = [str(item.attname) for item in question._meta.fields]
        self.assertEqual(12, len(fields))
        for field in ['id', 'created', 'modified', 'text', 'instructions', 'UID', 'answer_type',
                      'region_id', 'is_primary', 'is_required', 'export_label', 'parent_id']:
            self.assertIn(field, fields)

    def test_question_store(self):
        question = Question.objects.create(text='Uganda Revision 2014 what what?', UID='abc123', answer_type='Text')
        self.failUnless(question.id)
        self.assertEqual('Uganda Revision 2014 what what?', question.text)
        self.assertIsNone(question.instructions)
        self.assertEqual('abc123', question.UID)
        self.assertIsNone(question.region)
        self.assertIsNone(question.parent)
        self.assertTrue(question.is_core)
        self.assertFalse(question.is_primary)
        self.assertFalse(question.is_required)

    def test_question_uid_is_unique_when_question_has_no_parent(self):
        a_question = Question.objects.create(text='Uganda Revision 2014 what what?', UID='abc123', answer_type='Text')
        question_with_same_uid = Question(text='haha', UID='abc123', answer_type='Text')
        self.assertRaises(IntegrityError, question_with_same_uid.save)

    def test_editing_self_does_not_raise_integrity_error(self):
        question = Question.objects.create(text='question text', UID='abc123', answer_type='Text')
        UID = question.UID
        question.text="haha"
        question.save()
        self.failUnless(question.id)
        self.assertEqual(UID, Question.objects.get(text=question.text).UID)

    def test_child_question_uid_is_parent_question_uid(self):
        parent_question = Question.objects.create(text='question text', UID='abc123', answer_type='Text')
        child_question_with_same_uid = Question(text='revised text', UID='abc123', answer_type='Text', parent=parent_question)
        child_question_with_same_uid.save()
        self.failUnless(child_question_with_same_uid.id)

    def test_parent_automatically_transfer_UID_to_child(self):
        parent_question = Question.objects.create(text='question text', UID='abc123', answer_type='Text')
        child_question_without_uid = Question.objects.create(text='revised text', answer_type='Text', parent=parent_question)
        child_question_with_different_uid = Question.objects.create(text='revised text', answer_type='Text',
                                                                    UID='different uid', parent=parent_question)
        self.assertEqual(parent_question.UID, child_question_without_uid.UID)
        self.assertEqual(parent_question.UID, child_question_with_different_uid.UID)

    def test_question_can_get_its_answers(self):
        self.assertEqual(2, len(self.question1.all_answers()))
        self.assertIn(self.question1_answer, self.question1.all_answers())
        self.assertIn(self.question1_answer_2, self.question1.all_answers())

    def test_question_knows_if_it_is_first_in_its_group(self):
        question2 = Question.objects.create(text='question 2', UID='C00004', answer_type='Number')
        question3 = Question.objects.create(text='question 3', UID='C00005', answer_type='Number')
        self.sub_group = QuestionGroup.objects.create(subsection=self.sub_section_1, name="subgroup",
                                                      parent=self.parent_group)
        self.sub_group.question.add(question2, question3)

        QuestionGroupOrder.objects.create(question=self.question1, question_group=self.parent_group, order=1)
        QuestionGroupOrder.objects.create(question=question2, question_group=self.parent_group, order=2)
        QuestionGroupOrder.objects.create(question=question3, question_group=self.parent_group, order=3)

        self.assertTrue(self.question1.is_first_in_group())
        self.assertTrue(question2.is_first_in_group())
        self.assertFalse(question3.is_first_in_group())

    def test_question_knows_if_its_in_a_sub_group(self):
        question2 = Question.objects.create(text='question 2', UID='C00004', answer_type='Number')
        self.sub_group = QuestionGroup.objects.create(subsection=self.sub_section_1, name="subgroup",
                                                      parent=self.parent_group)
        self.sub_group.question.add(question2)

        self.assertTrue(question2.is_in_subgroup())

        question3 = Question.objects.create(text='question 3', UID='C00005', answer_type='Number')
        self.assertFalse(question3.is_in_subgroup())

        question4 = Question.objects.create(text='question 3', UID='C00077', answer_type='Number')
        self.parent_group.question.add(question4)
        self.assertFalse(question4.is_in_subgroup())

    def test_question_knows_if_it_is_last_in_its_group(self):
        question2 = Question.objects.create(text='question 2', UID='C00004', answer_type='Number')
        question3 = Question.objects.create(text='question 3', UID='C00005', answer_type='Number')
        self.sub_group = QuestionGroup.objects.create(subsection=self.sub_section_1, name="subgroup",
                                                      parent=self.parent_group)
        self.sub_group.question.add(question2, question3)

        QuestionGroupOrder.objects.create(question=self.question1, question_group=self.parent_group, order=1)
        QuestionGroupOrder.objects.create(question=question2, question_group=self.parent_group, order=2)
        QuestionGroupOrder.objects.create(question=question3, question_group=self.parent_group, order=3)

        self.assertFalse(self.question1.is_last_in_group())
        self.assertFalse(question2.is_last_in_group())
        self.assertTrue(question3.is_last_in_group())

    def test_question_knows_option_has_options(self):
        question = Question.objects.create(text='what do you drink?', UID='C_2013', answer_type='MultiChoice')
        QuestionOption.objects.create(text='tusker lager', question=question,
                                      instructions="Pick your favorite beer?")
        self.assertTrue(question.has_question_option_instructions())

        question = Question.objects.create(text='what do you drink?', UID='C_2014', answer_type='MultiChoice')
        QuestionOption.objects.create(text='tusker lager', question=question)
        self.assertFalse(question.has_question_option_instructions())

    def test_question_knows_latest_answer_for_draft_given_group_and_country(self):
        question1 = Question.objects.create(text='question1', UID='C00015', answer_type='Number', is_primary=True)
        question2 = Question.objects.create(text='question2', UID='C00016', answer_type='Number')
        question3 = Question.objects.create(text='question3', UID='C00017', answer_type='Number')
        self.parent_group.question.add(question1, question2)

        group2 = QuestionGroup.objects.create(subsection=self.sub_section_1, name="group2")
        group2.question.add(question3)

        question1_answer = NumericalAnswer.objects.create(question=question1, country=self.country,
                                                          status=Answer.DRAFT_STATUS, response=23, version=1)
        question2_answer = NumericalAnswer.objects.create(question=question2, country=self.country,
                                                          status=Answer.DRAFT_STATUS, response=1, version=1)
        question3_answer = NumericalAnswer.objects.create(question=question3, country=self.country,
                                                          status=Answer.SUBMITTED_STATUS, response=11, version=1)

        answer_group1 = AnswerGroup.objects.create(grouped_question=self.parent_group, row=1)
        answer_group1.answer.add(question1_answer, question2_answer)

        answer_group2 = AnswerGroup.objects.create(grouped_question=group2, row=1)
        answer_group2.answer.add(question3_answer)

        country_2 = Country.objects.create(name="Uganda 2")
        question1_answer_2 = NumericalAnswer.objects.create(question=question1, country=country_2,
                                                            status=Answer.DRAFT_STATUS, response=23, version=1)
        question2_answer_2 = NumericalAnswer.objects.create(question=question2, country=country_2,
                                                            status=Answer.DRAFT_STATUS, response=1, version=1)
        answer_group_2 = AnswerGroup.objects.create(grouped_question=self.parent_group, row=2)
        answer_group_2.answer.add(question1_answer_2, question2_answer_2)

        self.assertEqual(question1_answer, question1.latest_answer(self.parent_group, self.country))
        self.assertEqual(question2_answer, question2.latest_answer(self.parent_group, self.country))
        self.assertEqual(question3_answer, question3.latest_answer(group2, self.country))

        self.assertEqual(question1_answer_2, question1.latest_answer(self.parent_group, country_2))
        self.assertEqual(question2_answer_2, question2.latest_answer(self.parent_group, country_2))

    def test_none_if_no_latest_answer_exists_for_given_group_and_country(self):
        question1 = Question.objects.create(text='question1', UID='C00015', answer_type='Number', is_primary=True)
        question2 = Question.objects.create(text='question2', UID='C00016', answer_type='Number')
        self.parent_group.question.add(question1, question2)
        self.assertIsNone(question1.latest_answer(self.parent_group, self.country))
        self.assertIsNone(question2.latest_answer(self.parent_group, self.country))

    def test_get_next_uid_given_given_largest_uid_question(self):
        self.assertEqual('00004', Question.next_uid())

    def test_get_next_uid_given_given_largest_uid_is_9th(self):
        Question.objects.create(text='question 3', UID='C00009', answer_type='Number')
        self.assertEqual('00010', Question.next_uid())

    def test_knows_can_be_deleted(self):
        question = Question.objects.create(text='what do you drink?', UID='C_2014', answer_type='MultiChoice')
        self.assertTrue(question.can_be_deleted())

    def test_knows_can_not_be_deleted_when_answered(self):
        question = Question.objects.create(text='what do you drink?', UID='C_2014', answer_type='MultiChoice')
        country = Country.objects.create(name="Peru")
        Answer.objects.create(question=question, country=country, status="Submitted")
        self.assertFalse(question.can_be_deleted())

    def test_question_can_get_nth_option(self):
        question = Question.objects.create(text='what do you drink?', UID='C_2013', answer_type='MultiChoice', is_primary=True)
        option1 = QuestionOption.objects.create(text='tusker lager', question=question)
        option2 = QuestionOption.objects.create(text='tusker lite', question=question)
        option3 = QuestionOption.objects.create(text='tusker malt', question=question)
        self.assertEqual(option1, question.get_option_at(1))
        self.assertEqual(option2, question.get_option_at(2))
        self.assertEqual(option3, question.get_option_at(3))

    def test_knows_multichoice(self):
        question1 = Question.objects.create(text='ha', UID='C_2013', answer_type='MultiChoice',)
        question2 = Question.objects.create(text='ha', UID='C_2014', answer_type='Number',)

        self.assertTrue(question1.is_multichoice())
        self.assertFalse(question2.is_multichoice())


class QuestionOptionTest(BaseTest):

    def test_question_option_fields(self):
        question = QuestionOption()
        fields = [str(item.attname) for item in question._meta.fields]
        self.assertEqual(7, len(fields))
        for field in ['id', 'created', 'modified', 'text', 'instructions', 'question_id', 'UID']:
            self.assertIn(field, fields)

    def test_question_store(self):
        question = Question.objects.create(text='what do you drink?', UID='abc123', answer_type='Text')
        question_option = QuestionOption.objects.create(text='tusker lager', question=question)

        self.failUnless(question_option.id)
        self.assertEqual('tusker lager', question_option.text)
        self.assertEqual(question, question_option.question)
        self.assertEqual(None, question_option.instructions)
        self.assertEqual(None, question_option.UID)