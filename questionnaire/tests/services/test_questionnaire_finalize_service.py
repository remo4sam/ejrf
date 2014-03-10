from questionnaire.models import Questionnaire
from questionnaire.services.questionnaire_finalizer import QuestionnaireFinalizeService
from questionnaire.tests.base_test import BaseTest


class QuestionnaireFinalizeServiceTest(BaseTest):

    def setUp(self):
        self.draft_questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English", description="From dropbox as given by Rouslan", year=2013, status=Questionnaire.DRAFT)
        self.finalized_questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English", description="From dropbox as given by Rouslan", year=2013, status=Questionnaire.DRAFT)

    def test_finalizes_questionnaire_when_finalize_is_called(self):
        message = QuestionnaireFinalizeService(self.draft_questionnaire).finalize()
        self.assertEqual(Questionnaire.FINALIZED, self.draft_questionnaire.status)
        self.assertNotEqual(Questionnaire.DRAFT, self.draft_questionnaire.status)
        self.assertEqual(message, "The questionnaire has been finalized successfully.")

    def test_unfinalizes_questionnaire_when_unfinalize_is_called(self):
        message = QuestionnaireFinalizeService(self.finalized_questionnaire).unfinalize()
        self.assertNotEqual(Questionnaire.FINALIZED, self.finalized_questionnaire.status)
        self.assertEqual(Questionnaire.DRAFT, self.finalized_questionnaire.status)
        self.assertEqual(message, "The questionnaire is now in progress.")

    def test_unfinalize_returns_error_message_if_published_to_regions(self):
        questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English",  year=2013, status=Questionnaire.PUBLISHED)
        message = QuestionnaireFinalizeService(questionnaire).unfinalize()
        self.assertNotEqual(Questionnaire.DRAFT, questionnaire.status)
        self.assertEqual(Questionnaire.PUBLISHED, questionnaire.status)
        self.assertEqual(message, "The questionnaire could not be unlocked because its published.")
