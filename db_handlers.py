import sqlite3
import bcrypt
from cryptography.fernet import Fernet


def create_table():
    conn = sqlite3.connect("hashx.db")
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS users_data(
                        website text,
                        user_name text,  
                        password text,
                        hash varchar
                        )""")

    cursor.execute('''CREATE TABLE IF NOT EXISTS "__k3y5___" (
                    "_USE_"	TEXT,
                    "_k3y_"	TEXT
                    )''')


    selected = tuple(cursor.execute(f"SELECT * FROM __k3y5___"))

    if not selected:
        key = Fernet.generate_key().decode('utf-8')
        cursor.execute(f"INSERT INTO __k3y5___ VALUES('00001', '{key}')")

    # save changes
    conn.commit()
    # close connection
    conn.close()


def add_or_update(ws, un, pw):

    pw_hash = bcrypt.hashpw(pw.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    conn = sqlite3.connect("hashx.db")
    # create cursor
    cursor = conn.cursor()

    cursor.execute(f"SELECT COUNT(*) from users_data where user_name = '{un}' AND website = '{ws}'")
    cur_result = cursor.fetchone()
    k3y = tuple(cursor.execute("SELECT _k3y_ FROM __k3y5___ WHERE _USE_ = '00001'"))[0][0]
    f = Fernet(k3y)

    # the plaintext is converted to ciphertext
    token = f.encrypt(pw.encode('utf-8')).decode('utf-8')



    sql = None

    if cur_result[0] == 0:
        sql = f'''INSERT INTO users_data VALUES('{ws}', '{un}', '{token}', '{pw_hash}')'''
    else:
        sql = f"UPDATE users_data SET website = '{ws}', user_name = '{un}', password = '{token}', hash = '{pw_hash}' " \
              f"where website = '{ws}' AND user_name = '{un}'"


    cursor.execute(sql)

    # save changes
    conn.commit()
    # close connection
    conn.close()


def get_content():
    conn = sqlite3.connect("hashx.db")
    cursor = conn.cursor()
    # rows = tuple(cursor.execute('SELECT website, user_name, password FROM users_data'))
    rows = tuple(cursor.execute('SELECT website, user_name FROM users_data'))
    conn.close()
    return rows


def remove_entry(ws, un, *extra):
    conn = sqlite3.connect("hashx.db")
    cursor = conn.cursor()
    rows = tuple(cursor.execute(f"SELECT * FROM users_data WHERE (user_name = '{un}' AND website = '{ws}')"))

    if len(rows) == 0:
        raise Exception('No such record found')

    cursor.execute(f"DELETE FROM users_data WHERE (user_name = '{un}' AND website = '{ws}')")
    conn.commit()
    conn.close()


def check(ws, un, pw):
    conn = sqlite3.connect("hashx.db")
    response = tuple(conn.execute(f"SELECT hash FROM users_data WHERE website = '{ws}' AND user_name = '{un}'"))
    conn.close()

    if not response:
        raise Exception('Wrong website/username')
    else:
        hashed_pw = bytes(response[0][0], 'utf-8')
        return bcrypt.checkpw(pw.encode('utf-8'), hashed_pw)


def reveal_password(ws, un):
    conn = sqlite3.connect("hashx.db")
    cursor = conn.cursor()
    response = tuple(cursor.execute(f"SELECT password FROM users_data WHERE website = '{ws}' AND user_name = '{un}'"))
    if not response:
        raise Exception('Wrong details entered')

    k3y = tuple(cursor.execute("SELECT _k3y_ FROM __k3y5___ WHERE _USE_ = '00001'"))[0][0]
    f = Fernet(k3y)

    token = f.decrypt(response[0][0].encode('utf-8')).decode('utf-8')
    conn.close()



    return token



