
def extra_rows(data, given_key, group_id):
    related_keys = filter(lambda key: same_group_data_keys(key, given_key, data, group_id), data.keys())
    row_numbers = []
    for key in related_keys:
        row_number = data.get(key, 0)[0]
        row_numbers.append(row_number)
    row_numbers = list(set(row_numbers))
    row_numbers.sort()
    return row_numbers


def same_group_data_keys(key, given_key, data, group_id):
    return key.startswith(given_key) and key.endswith('response') and __field_belong_group(data[key], group_id)


def clean_list(dirty_list):
    if isinstance(dirty_list, list) and len(dirty_list) > 1:
        dirty_element = _get_first_element(dirty_list)
        old_dirty_list = dirty_list
        dirty_list = dirty_element.split(',')
        dirty_list.extend(old_dirty_list)
    return dirty_list


def clean_data_dict(data):
    new_data = {}
    for key, value in data.items():
        new_data[key] = clean_list(value)
    return new_data


def _get_first_element(dirty_list):
    return dirty_list.pop(0)


def __field_belong_group(data_value, group_id):
    return len(data_value) > 1 and data_value[1] == str(group_id)