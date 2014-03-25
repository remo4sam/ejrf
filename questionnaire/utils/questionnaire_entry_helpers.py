
def extra_rows(data, given_key, group_id):
    related_keys = filter(lambda key: same_group_data_keys(key, given_key, data, group_id), data.keys())
    row_numbers = []
    for key in related_keys:
        row_number = data.get(key, 0)[1]
        row_numbers.append(row_number)
    row_numbers = list(set(row_numbers))
    row_numbers.sort()
    return row_numbers

def same_group_data_keys(key, given_key, data, group_id):
    return key.startswith(given_key) and key.endswith('response') and len(data[key]) > 1 and \
           data[key][-1] == str(group_id)


def clean_list(dirty_list):
    if isinstance(dirty_list, list) and len(dirty_list) > 1 :
        dirty_element = dirty_list.pop(1)
        dirty_list.extend(dirty_element.split(','))
    return dirty_list


def clean_data_dict(data):
    new_data = {}
    for key, value in data.items():
        new_data[key] = clean_list(value)
    return new_data