import json


def user_data_to_json(data):
    user_bytes = data
    user_str = str(user_bytes, 'utf-8')
    user_json = json.loads(user_str)
    return user_json


def banners_objectlist_to_urllist(object_list):
    url_list = []
    for banner in object_list:
        url_list.append(banner.image_url)
    return url_list


def quotes_objectlist_to_quotelist(object_list):
    quote_list = []
    for quote in object_list:
        quote_list.append(quote.quote)
    return quote_list
