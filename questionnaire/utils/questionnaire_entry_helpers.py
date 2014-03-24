
def extra_rows(data, given_key):
    data = dict(data)
    related_keys = filter(lambda key: key.startswith(given_key) and key.endswith('response'), data.keys())
    related_keys.sort()
    all_rows = []
    row_numbers = []
    for key in related_keys:
        row_number = data.get(key, 0)[1]
        if int(row_number) == 0 and row_numbers:
            all_rows.append(row_numbers)
            row_numbers = []
        row_numbers.append(row_number)
    all_rows.append(row_numbers)
    return all_rows