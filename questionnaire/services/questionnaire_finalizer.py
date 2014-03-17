from questionnaire.models import Questionnaire


class QuestionnaireFinalizeService(object):
    FINALIZED_SUCCESSFULLY_MESSAGE = "The questionnaire has been finalized successfully."
    PUBLISHED_MESSAGE = "The questionnaire could not be unlocked because its published."
    IN_PROGRESS_MESSAGE = "The questionnaire is now in progress."
    APPROVED_SUCCESSFULLY_MESSAGE = "The questionnaire has been approved successfully."

    def __init__(self, questionnaire):
        self.questionnaire = questionnaire

    def finalize(self):
        self.questionnaire.status = Questionnaire.FINALIZED
        self.questionnaire.save()
        return self.FINALIZED_SUCCESSFULLY_MESSAGE

    def unfinalize(self):
        if self.questionnaire.status == Questionnaire.PUBLISHED:
            return self.PUBLISHED_MESSAGE
        self.questionnaire.status = Questionnaire.DRAFT
        self.questionnaire.save()
        return self.IN_PROGRESS_MESSAGE

    def approve(self):
        self.questionnaire.status = Questionnaire.PUBLISHED
        self.questionnaire.save()
        return self.APPROVED_SUCCESSFULLY_MESSAGE