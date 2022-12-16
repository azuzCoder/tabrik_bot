import psycopg2

db = psycopg2.connect(database="tabrik", user="postgres", password="admin")
cursor = db.cursor()


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
        values += val + ","
    query = "INSERT INTO " + name + "(" + columns.removesuffix(",") + ") VALUES (" + values.removesuffix(",") + ");"

    cursor.execute(query)
    db.commit()


def select(name: str, fields: list, where: str = None):
    columns = ""
    for field in fields:
        columns += field + ","
    query = "SELECT " + columns.removesuffix(",") + " FROM " + name

    query = check_where(query, where)

    cursor.execute(query)
    return cursor.fetchall()


def update(name: str, fields: list, where: str):
    columns = ""
    for col, val in fields:
        columns += col + "="
        if val is str:
            columns += "'" + val + "'"
        else:
            columns += str(val)
        columns += ','

    query = "UPDATE " + name + " SET " + columns.removesuffix(",") + " " + where
    print(query)



def check_where(query, where):
    if not where:
        query += " " + where
    return query

# print(select("groups", ['*']))


update("name", [('id', 12)], "WHERE id=12")
