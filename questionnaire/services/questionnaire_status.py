from collections import OrderedDict
from questionnaire.models import Region


class QuestionnaireStatusService(object):
    def __init__(self):
        self.regions = Region.objects.order_by('name')

    def region_country_status_map(self):
        region_country_map = OrderedDict()
        for region in self.regions:
            region_country_map.update({region: region.countries.order_by('name')})
        return region_country_map