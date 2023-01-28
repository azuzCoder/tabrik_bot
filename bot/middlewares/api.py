import requests

BASE_URL = 'http://127.0.0.1:8000/api/v1/'

''' addrs for USER '''
_user = 'user/'
get_or_update_user = _user  # chat_id is required
get_user_by_id = _user + 'id/'  # id is required
list_users = _user + 'add'  # empty
add_user = _user + 'add'  # data is required


''' addrs for GROUP '''
get_or_update_group = 'group/'  # chat_id is required
get_group_by_id = 'group/id/'  # id is required
list_groups = 'group/add'  # empty
add_group = 'group/add'  # data is required


''' addrs for BIRTHDAY '''
get_birthday = 'birthday/'  # chat_id is required
list_birthdays = 'birthday/add'  # empty
add_birthday = 'birthday/add'


def get(pk: int = None, addr: str = None):
    res = requests.get(get_url(pk, addr))
    return result(res)


def post(addr: str, data: dict):
    res = requests.post(get_url(addr=addr), data)
    return result(res)


def put(pk: int, addr: str, data: dict):
    res = requests.put(get_url(pk, addr), data)
    return result(res)


def result(res):
    if res.ok:
        return res.json()
    print(res)
    return None


def get_url(pk: int = None, addr: str = None):
    url = BASE_URL + addr
    if pk is None:
        return url
    return url + str(pk)


# print(get(1, get_user_by_id))
