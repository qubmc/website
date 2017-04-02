import json


def user_data_to_json(data):
    user_bytes = data
    user_str = str(user_bytes, 'utf-8')
    user_json = json.loads(user_str)
    return user_json
