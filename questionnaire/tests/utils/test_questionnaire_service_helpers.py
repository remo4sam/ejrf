from questionnaire.tests.base_test import BaseTest
from questionnaire.utils.questionnaire_entry_helpers import extra_rows


class QuestionnaireServiceHelperTest(BaseTest):
    def test_get_number_of_extra_rows_supplied_for_an_answer_type(self):
        data = {u'MultiChoice-MAX_NUM_FORMS': u'3', u'MultiChoice-TOTAL_FORMS': u'3',
                     u'MultiChoice-INITIAL_FORMS': u'3', u'MultiChoice-0-response': [1, 0],
                     u'MultiChoice-1-response': [2, 1],  u'MultiChoice-2-response': [3, 2],
                     u'Number-MAX_NUM_FORMS': u'3', u'Number-TOTAL_FORMS': u'3',
                     u'Number-INITIAL_FORMS': u'3', u'Number-0-response': ['22',0],
                     u'Number-1-response': ['44',1],  u'Number-2-response': ['33', 2],
                     u'Text-MAX_NUM_FORMS': u'3', u'Text-TOTAL_FORMS': u'3',
                     u'Text-INITIAL_FORMS': u'3', u'Text-0-response': ['Haha',0],
                     u'Text-1-response': ['Hehe',1],  u'Text-2-response': ['hehehe', 2],
                     u'Date-MAX_NUM_FORMS': u'3', u'Date-TOTAL_FORMS': u'3',
                     u'Date-INITIAL_FORMS': u'3', u'Date-0-response': ['2014-2-2', 0],
                     u'Date-1-response': ['2014-2-2',1],  u'Date-2-response': ['2014-2-2',2],
                     }

        self.assertEqual([[0, 1, 2]], extra_rows(data, 'Number'))
        self.assertEqual([[0, 1, 2]], extra_rows(data, 'MultiChoice'))
        self.assertEqual([[0, 1, 2]], extra_rows(data, 'Date'))
        self.assertEqual([[0, 1, 2]], extra_rows(data, 'Text'))

    def test_get_number_of_extra_rows_supplied_for_an_answer_type_when_there_are_more_than_one_grid_of_the_same_type(self):
        data = {u'MultiChoice-MAX_NUM_FORMS': u'5', u'MultiChoice-TOTAL_FORMS': u'5',
             u'MultiChoice-INITIAL_FORMS': u'5', u'MultiChoice-0-response': [1, 0],
             u'MultiChoice-1-response': [2, 1],  u'MultiChoice-2-response': [3, 2],
             u'MultiChoice-3-response': [5, 0],  u'MultiChoice-4-response': [6, 1],
             u'Number-MAX_NUM_FORMS': u'3', u'Number-TOTAL_FORMS': u'3',
             u'Number-INITIAL_FORMS': u'3', u'Number-0-response': ['22',0],
             u'Number-1-response': ['44',1],  u'Number-2-response': ['33', 2],
             u'Text-MAX_NUM_FORMS': u'5', u'Text-TOTAL_FORMS': u'5',
             u'Text-INITIAL_FORMS': u'3', u'Text-0-response': ['Haha',0],
             u'Text-1-response': ['Hehe',1],  u'Text-2-response': ['hehehe', 2],
             u'Text-3-response': ['Hehe',0],  u'Text-4-response': ['hehehe', 1],
             u'Date-MAX_NUM_FORMS': u'3', u'Date-TOTAL_FORMS': u'3',
             u'Date-INITIAL_FORMS': u'3', u'Date-0-response': ['2014-2-2', 0],
             u'Date-1-response': ['2014-2-2',1],  u'Date-2-response': ['2014-2-2',2],
             }

        self.assertEqual([[0, 1, 2]], extra_rows(data, 'Number'))
        self.assertEqual([[0, 1, 2], [0,1]], extra_rows(data, 'MultiChoice'))
        self.assertEqual([[0, 1, 2]], extra_rows(data, 'Date'))
        self.assertEqual([[0, 1, 2], [0,1]], extra_rows(data, 'Text'))
