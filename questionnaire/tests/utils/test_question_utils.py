from questionnaire.models import Question
from questionnaire.tests.base_test import BaseTest
from questionnaire.utils.model_utils import largest_uid


class QuestionUtilTest(BaseTest):
    def setUp(self):
        self.question1 = Question.objects.create(text='B. Number of cases tested',
                                                 instructions="Enter the total numbe", UID='C00003', answer_type='Number')

    def test_get_largest_uid_returns_00001_if_no_quests_exists(self):
        Question.objects.all().delete()
        self.assertEqual(int('00001'), largest_uid(Question))

    def test_get_largest_uid(self):
        self.assertEqual(int('00003'), largest_uid(Question))

    def test_get_largest_uid_given_more_than_one_question(self):
        Question.objects.create(text='question 3', UID='C00005', answer_type='Number')
        self.assertEqual(int('00005'), largest_uid(Question))

    def test_get_largest_uid_given_more_than_one_question_with_letters(self):
        Question.objects.create(text='question 3', UID='C0005b', answer_type='Number')
        Question.objects.create(text='question 3', UID='C00006', answer_type='Number')
        self.assertEqual(int('00006'), largest_uid(Question))
