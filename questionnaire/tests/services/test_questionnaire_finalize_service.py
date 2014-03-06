from questionnaire.models import Questionnaire
from questionnaire.services.questionnaire_finalizer import QuestionnaireFinalizeService
from questionnaire.tests.base_test import BaseTest


class QuestionnaireFinalizeServiceTest(BaseTest):

    def setUp(self):
        self.questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English", description="From dropbox as given by Rouslan", year=2013, status=Questionnaire.DRAFT)

    def test_finalizes_questionnaire_when_finalize_is_called(self):
        QuestionnaireFinalizeService(self.questionnaire).finalize()
        self.assertEqual(Questionnaire.FINALIZED, self.questionnaire.status)
        self.assertNotEqual(Questionnaire.DRAFT, self.questionnaire.status)