"""Operation for database"""


def crud_db(db, query_sql, query_args):
    """CRUD operation"""
    cur = db.cursor()
    cur.execute(query_sql, query_args)
    cur.close()
    db.commit()


def query_db(db, query, args=(), one=False):
    cur = db.cursor().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv
