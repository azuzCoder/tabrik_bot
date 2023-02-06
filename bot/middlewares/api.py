import requests

BASE_URL = 'http://127.0.0.1:8000/api/v1/'

user = 'users'
group = 'groups'
birthday = 'birthdays'


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
    print(res.text)
    if res.ok:
        return res.json()
    return None


def get_url(pk: int = None, addr: str = None):
    url = BASE_URL + addr
    if pk is None:
        return url
    if not addr.endswith('/'):
        url += '/'
    return url + str(pk)

