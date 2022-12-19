import psycopg2
from psycopg2 import errors


def insert(name: str, fields: dict):
    """
    - *name: table name
    - *fields-> dict.
        key -> column name
        value -> value which is inserting into column
    :return: None
    """

    columns = ""
    values = ""
    for key, val in fields.items():
        columns += key + ","
        values += check_value(val) + ","
    query = "INSERT INTO " + name + "(" + columns.removesuffix(",") + ") "
    query += "VALUES (" + values.removesuffix(",") + ") RETURNING id; "
    try:
        execute_commit(query)
    except errors.UniqueViolation:
        pass


def select(name: str, fields: list, where: str = None):
    """
    :param name: str -> name of table
    :param fields: list -> selected fields
    :param where: str -> condition
    :return:
    """
    columns = ""
    for field in fields:
        columns += field + ","
    query = "SELECT " + columns.removesuffix(",") + " FROM " + name
    query = check_where(query, where)
    return execute_fetch(query)


def update(name: str, fields: list, where: str):
    """
    :param name: str -> name of table
    :param fields: list -> pair of column and value. Ex: [("name", "John"),  ... ]
    :param where: str -> condition
    :return: None
    """
    columns = ""
    for col, val in fields:
        columns += col + "="
        columns += check_value(val)
        columns += ','

    query = "UPDATE " + name + " SET " + columns.removesuffix(",") + " " + where
    print(query)
    execute_commit(query)


def check_where(query, where):
    """
    :param query: str -> main query
    :param where: str -> condition
    :return: str ->

    'where' is checked if 'where' is None, nothing is changed else 'query' concanate with 'where'

    """
    if where:
        query += " " + where
    return query


def check_value(val):
    if val is str:
        return "'" + val + "'"
    return str(val)


def execute_commit(query: str):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(query)
    db.commit()
    cursor.close()
    db.close()


def execute_fetch(query: str):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(query)
    return cursor.fetchall()


def get_db():
    db = psycopg2.connect(database="tabrik", user="postgres", password="admin")
    return db


# print(select("groups", ['*']))
# update("groups", [('chat_id', 12), ('joined', True)], "WHERE id=12")
# print(select('groups', ['id'], "WHERE chat_id='868'"))

# try:
#     insert('groups', {'chat_id': -1001835683287, 'joined': True})
# except errors.UniqueViolation:
#     print('Bir xilku jalla')