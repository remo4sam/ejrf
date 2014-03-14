from collections import OrderedDict
from questionnaire.models import Region


class QuestionnaireStatusService(object):
    def __init__(self, questionnaire):
        self.questionnaire = questionnaire

    def region_country_status_map(self):
        statuses = OrderedDict()
        for region in Region.objects.order_by('name'):
            statuses.update({region: OrderedDict()})
            for country in region.countries.all().order_by('name'):
                statuses[region].update({country: country.get_answer_status_in(self.questionnaire)})
        return statuses