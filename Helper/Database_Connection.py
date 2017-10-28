from mysql.connector import MySQLConnection, Error
from Helper.Database_Config import read_db_config
import datetime
import Helper.EM_Utility as emu

apath = None

def set_config_file_path(path):
    global apath
    apath= path

def get_config_file_path():
    return apath

def connect():
    """ Connect to MySQL database """

    db_config = read_db_config(get_config_file_path())

    try:
        conn = MySQLConnection(**db_config)

        if conn.is_connected():
            return conn
        else:
            return None

    except Error as e:
        print(e)

# For Registration
def insert_new_user(name, email, password):
    if email_exists(email):
        return False
    else:
        db = connect()
        if db == None:
            print('DB connection failed!')
        else:
            current_date = datetime.datetime.now()
            query = 'INSERT INTO user_accounts (name,email,password, date_created, last_login_date)' \
                    'VALUES (%s,%s,%s,%s,%s)'
            args = (name,email,emu.hash_password(password),current_date,current_date)
            cursor = db.cursor()
            cursor.execute(query,args)
            #print(cursor.lastrowid)
            db.commit()
            cursor.close()
        db.close()
        return True

def email_exists(email):
    query = 'SELECT email from user_accounts WHERE email = %s'
    args = (email,)
    db = connect()
    cursor = db.cursor()
    cursor.execute(query,args)
    row = None
    row = cursor.fetchone()
    db.commit()
    cursor.close()
    db.close()

    if row is not None:
        return True
    return False

# For Login
def login_user(email, password):
    if email_exists(email):
        query = 'SELECT password from user_accounts WHERE email = %s'
        args = (email,)
        db = connect()
        cursor = db.cursor()
        cursor.execute(query, args)
        row = None
        row = cursor.fetchone()
        db.commit()
        cursor.close()
        db.close()

        if row[0] == emu.hash_password(password):
            return True
        return False

    else:
        return False

"""if __name__ == '__main__':
    insert_new_user('asdf','asdf','asdfsa')"""