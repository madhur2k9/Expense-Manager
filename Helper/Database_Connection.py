from mysql.connector import MySQLConnection, Error
from Helper.Database_Config import read_db_config
import datetime
import Helper.EM_Utility as emu
import Models.User

apath = None
user = None

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
        query = 'SELECT * from user_accounts WHERE email = %s'
        args = (email,)
        db = connect()
        cursor = db.cursor()
        cursor.execute(query, args)
        row = None
        row = cursor.fetchone()
        db.commit()
        cursor.close()
        db.close()

        if row[2] == emu.hash_password(password):
            global user
            user = Models.User.User(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
            return True
        return False

    else:
        return False

def get_user_id(email):
    if user is not None:
        return user.get_id()
    else:
        return -999

def record_transaction(transac_type, category, title, description, amount, user_id, current_balance):
    query = 'INSERT INTO user_transactions (transaction_type, category, title, description, amount, date_added, user_id)' \
            'VALUES (%s,%s,%s,%s,%s,%s,%s)'
    current_date = datetime.datetime.now()
    args = (transac_type, category, title, description, amount, current_date, user_id)
    db = connect()
    cursor = db.cursor()
    cursor.execute(query,args)
    current_balance = emu.recalc_current_balance(transac_type,amount,current_balance)
    query = "UPDATE user_accounts SET current_balance = %s WHERE id = %s;"
    args = (current_balance, user_id)
    cursor.execute(query,args)
    global user
    user.set_current_balance(current_balance)
    # TO DO Refactor the following 3 lines
    db.commit()
    cursor.close()
    db.close()

def get_all_transactions(user_id):
    response = {"Expenses": get_all_expenses(user_id), "Incomes": get_all_incomes(user_id)}
    return response

def get_all_expenses(user_id):
    query = 'SELECT * from user_transactions WHERE user_id = %s AND transaction_type = %s'
    args = (user_id, 0)
    db = connect()
    cursor = db.cursor()
    cursor.execute(query, args)
    rows = None
    rows = cursor.fetchall()
    db.commit()
    cursor.close()
    db.close()
    transactions = {}
    keys_list = ["id", "transaction_type", "category", "title", "description", "amount", "date_added"]
    expenses = {}
    counter = 0
    for row in rows:
        expenses[counter] = {}
        expenses[counter][keys_list[0]] = row[0]
        expenses[counter][keys_list[1]] = row[1]
        expenses[counter][keys_list[2]] = row[2]
        expenses[counter][keys_list[3]] = row[3]
        expenses[counter][keys_list[4]] = row[4]
        expenses[counter][keys_list[5]] = row[5]
        expenses[counter][keys_list[6]] = row[6]
        print(counter)
        counter += 1
    return expenses

def get_all_incomes(user_id):
    query = 'SELECT * from user_transactions WHERE user_id = %s AND transaction_type = %s'
    args = (user_id, 1)
    db = connect()
    cursor = db.cursor()
    cursor.execute(query, args)
    rows = None
    rows = cursor.fetchall()
    db.commit()
    cursor.close()
    db.close()
    transactions = {}
    keys_list = ["id", "transaction_type", "category", "title", "description", "amount", "date_added"]
    incomes = {}
    counter = 0
    for row in rows:
        incomes[counter] = {}
        incomes[counter][keys_list[0]] = row[0]
        incomes[counter][keys_list[1]] = row[1]
        incomes[counter][keys_list[2]] = row[2]
        incomes[counter][keys_list[3]] = row[3]
        incomes[counter][keys_list[4]] = row[4]
        incomes[counter][keys_list[5]] = row[5]
        incomes[counter][keys_list[6]] = row[6]
        print(counter)
        counter += 1
    return incomes

def get_user():
    if user is not None:
        return user
    else:
        return -999

"""if __name__ == '__main__':
    insert_new_user('asdf','asdf','asdfsa')"""