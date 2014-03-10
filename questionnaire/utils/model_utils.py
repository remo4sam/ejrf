import re

INITIAL_UID = 1
MAX_UID_LENGTH = 5


def largest_uid(cls):
    uid_numbers = []
    all_question_uids = cls.objects.all().values_list('UID', flat=True)
    for uid in all_question_uids:
        uid_numbers.extend([int(num[0]) for num in re.findall(r'(\d+)|([\+-]?\d+)', uid)])
    return max(uid_numbers) if len(uid_numbers) > 0 else INITIAL_UID


def stringify(uid):
    return "0" * (MAX_UID_LENGTH - len(str(uid))) + str(uid)


def map_question_type_with(orders, mapping, option=''):
    for order in orders:
        order_dict = {'option': option, 'order': order}
        mapping[order.question.answer_type].append(order_dict)


def reindex_orders_in(cls, **kwargs):
    objects = cls.objects.filter(**kwargs).order_by('order')
    for index, object_ in enumerate(objects):
        object_.order = index + 1
        object_.save()