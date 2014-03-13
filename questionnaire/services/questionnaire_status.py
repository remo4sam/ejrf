from questionnaire.models import Region


class QuestionnaireStatusService(object):
    def __init__(self, questionnaire):
        self.questionnaire = questionnaire

    def region_country_status_map(self):
        statuses = {}
        for region in Region.objects.order_by('name'):
            statuses.update({region: {}})
            for country in region.countries.all():
                statuses[region].update({country: country.get_answer_status_in(self.questionnaire)})
        return statuses