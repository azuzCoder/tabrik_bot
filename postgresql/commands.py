import psycopg2


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
        values += check(val) + ","
    query = "INSERT INTO " + name + "(" + columns.removesuffix(",") + ") VALUES (" + values.removesuffix(",") + ") RETURNING id;"
    print(query)

    db = get_db()
    idx = execute_fetch(db, query)[0][0]
    close(db)
    return idx


def select(name: str, fields: list, where: str = None):
    columns = ""
    for field in fields:
        columns += field + ","
    query = "SELECT " + columns.removesuffix(",") + " FROM " + name

    query = check_where(query, where)

    db = get_db()
    data = execute_fetch(db, query)
    close(db)
    return data


def update(name: str, fields: list, where: str):
    columns = ""
    for col, val in fields:
        columns += col + "="
        columns += check(val)
        # if val is str:
        #     columns += "'" + val + "'"
        # else:
        #     columns += str(val)
        columns += ','

    query = "UPDATE " + name + " SET " + columns.removesuffix(",")
    query = check_where(query, where)

    db = get_db()
    execute_commit(db, query)
    close(db)


def check(val):
    if type(val) == str:
        return '\'' + val + '\''
    return str(val)


def get_db():
    return psycopg2.connect(database="tabrik", user="postgres", password="admin")


def check_where(query, where):
    if where is not None:
        query += " " + where
    return query


def execute_commit(db, query: str):
    cursor = db.cursor()
    cursor.execute(query)
    db.commit()


def execute_fetch(db, query: str):
    cursor = db.cursor()
    cursor.execute(query)
    db.commit()
    return cursor.fetchall()


def close(db):
    db.cursor().close()
    db.close()


# print(select("groups", ['*']))
# update("name", [('id', 12)], "WHERE id=12")