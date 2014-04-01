import copy
from questionnaire.models import QuestionGroupOrder


class QuestionReIndexer(object):
    EXPECTED_KEYS = ["Number", "Date", "MultiChoice", "Text"]
    def __init__(self, data):
        self.data = data
        self.cleaned_data = self.clean_data_posted()

    def reorder_questions(self):
        for order_object, posted_value in self.get_old_orders().items():
            order_object.order = int(posted_value[1]) + 1
            order_object.save()

    def get_old_orders(self):
        orders = {}
        for posted_order_values in dict(self.cleaned_data).values():
            orders.update({QuestionGroupOrder.objects.get(id=posted_order_values[0]): posted_order_values})
        return orders

    def clean_data_posted(self):
        data  = copy.deepcopy(self.data)
        clean_keys = filter(lambda key: self.is_allowed(key), data.keys())
        cleaned_data = (dict((key, self.clean_values(value)) for key, value in data.iteritems() if key in clean_keys))
        return cleaned_data

    def is_allowed(self, key):
        for name in self.EXPECTED_KEYS:
            if key.startswith(name):
                return True

    def clean_values(self, value):
        value = filter(None, value)
        return value.split(",")