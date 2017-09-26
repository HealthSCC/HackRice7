import sqlite3

'''
conn = sqlite3.connect('HACKRICE.db')
cursor = conn.cursor()
cursor.execute('CREATE TABLE test (id varchar(20) PRIMARY KEY, pw varchar(20))')
cursor.execute('INSERT INTO test (id, pw) VALUES (\'roy7wt\', \'123456\')')
cursor.close()
conn.commit()
conn.close()
'''

DATABASE_NAME = 'HACKRICE.db'


def get_db():
    return sqlite3.connect(DATABASE_NAME)


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


def crud_db(query, args=()):
    get_db().cursor().execute(query, args)
    get_db().commit()


if __name__ == '__main__':
    conn = sqlite3.connect(DATABASE_NAME)
    cur = conn.cursor()
    args = ('rice@rice.edu.cn', '123456', 'RICE', 'RICE')
    # cur.execute('insert into patient values (\'rice@rice.edu\',\'123456\',\'RICE\',\'RICE\')')
    cur.execute('insert into patient values (?,?,?,?)', args)
    values = cur.execute('select * from patient').fetchall()
    for value in values:
        print value

    cur.close()
    conn.commit()
    conn.close()