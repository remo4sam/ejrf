from questionnaire.models import Region, Answer


class QuestionnaireStatusService(object):
    def __init__(self, questionnaire):
        self.questionnaire = questionnaire

    def region_country_status_map(self):
        statuses = {}
        for region in Region.objects.order_by('name'):
            statuses.update({region: {}})
            for country in region.countries.all():
                statuses[region].update({country: self.get_answer_status_for(country)})
        return statuses

    def get_answer_status_for(self, country):
        query_params = {'question__question_group__subsection__section__questionnaire': self.questionnaire}
        answers = Answer.objects.filter(country=country, **query_params).select_subclasses()
        if answers.exists():
            return Status.options[answers.latest('modified').status]
        return Status.options[None]


class Status(object):
    options = {
        Answer.SUBMITTED_STATUS: Answer.SUBMITTED_STATUS,
        Answer.DRAFT_STATUS: 'In Progress',
        None: 'Not Started'
    }