import requests

BASE_URL = 'http://127.0.0.1:8000/api/v1/'

'''
    GET, POST, PUT methods for USER
'''


def get_user(chat_id: int):
    url = BASE_URL + 'user/' + str(chat_id)
    res = requests.get(url)
    return result(res)


def get_with_id_user(id: int):
    url = BASE_URL + 'user/id/' + str(id)
    res = requests.get(url)
    return result(res)


def list_users():
    url = BASE_URL + 'user/add'
    res = requests.get(url).json()
    return res


def update_user(data: dict):
    url = BASE_URL + 'user/' + str(data['chat_id'])
    res = requests.put(url, data)
    return result(res)


def add_user(data: dict):
    url = BASE_URL + 'user/add'
    res = requests.post(url, data)
    return result(res)


'''
    GET, POST, PUT methods for GROUP
'''


def get_group(chat_id: int):
    url = BASE_URL + 'group/' + str(chat_id)
    res = requests.get(url)
    return result(res)


def get_with_id_groups(id: int):
    url = BASE_URL + 'group/id/' + str(id)
    res = requests.get(url)
    return result(res)


def list_groups():
    url = BASE_URL + 'group/add'
    res = requests.get(url)
    return res.json()


def add_group(data: dict):
    url = BASE_URL + 'group/add'
    res = requests.post(url, data)
    return result(res)


def update_group(data: dict):
    url = BASE_URL + 'group/' + str(data['chat_id'])
    res = requests.put(url, data)
    return result(res)


'''
    GET, POST, PUT methods for BIRTHDAY
'''


def get_birthday(chat_id: int):
    url = BASE_URL + 'birthday/' + str(chat_id)
    res = requests.get(url)
    return result(res)


def list_birthdays():
    url = BASE_URL + 'birthday/add'
    res = requests.get(url)
    return res.json()


def add_birthday(data: dict):
    url = BASE_URL + 'birthday/add'
    res = requests.post(url, data)
    print(res.text)
    return result(res)


def update_birthday(id: int, data: dict):
    url = BASE_URL + 'birthday/' + str(id)
    res = requests.put(url, data)
    return result(res)


def result(res):
    if res.ok:
        return res.json()
    return None


# print(list_birthdays())
