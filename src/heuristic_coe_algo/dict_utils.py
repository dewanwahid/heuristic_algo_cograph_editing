
def get_key_from_dictionary_for_value(my_dict: dict, val: int):
    for key, value in my_dict.items():
        if val == value:
            return key

    return "key doesn't exist"