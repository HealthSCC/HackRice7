from sqlite3 import dbapi2 as sqlite3

DATABASE_NAME = 'hackrice.db'


def connect_db():
    return sqlite3.connect(DATABASE_NAME)


def init_db():
    """Initializes the database."""
    db = connect_db()
    with open('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()


def crud_db(query_sql, query_args):
    """CRUD operation"""
    db = connect_db()
    cur = db.cursor()
    cur.execute(query_sql, query_args)
    cur.close()
    db.commit()


def query_db(query, args=(), one=False):
    cur = connect_db().cursor().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


def close_db():
    connect_db().close()


if __name__ == '__main__':
    """Create the basic tables in database"""
    init_db()
    # args = (1, 'NULL', '2017-09-27', '2017-09-26', 'Medicine', 12, 'Good')
    # crud_db('INSERT INTO event VALUES (?,?,?,?,?,?,?)', args)
    # args = (2, 'RICE', 'UNIVERSITY')
    # crud_db('INSERT INTO doctor VALUES(?,?,?)', args)
    close_db()
