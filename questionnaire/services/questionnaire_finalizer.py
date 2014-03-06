from questionnaire.models import Questionnaire


class QuestionnaireFinalizeService(object):
    def __init__(self, questionnaire):
        self.questionnaire = questionnaire

    def finalize(self):
        self.questionnaire.status = Questionnaire.FINALIZED
        self.questionnaire.save()

    def unfinalize(self):
        self.questionnaire.status = Questionnaire.DRAFT
        self.questionnaire.save()
