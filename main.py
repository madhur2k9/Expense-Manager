from Helper.Database_Connection import insert_new_user, set_config_file_path, login_user, record_transaction, \
    get_all_transactions, get_all_expenses, get_all_incomes

set_config_file_path('config.ini')

login_register = int(input('Press 1 to Register and 2 for Login'))

# login_register = 0

if login_register == 1:
    name = input('Enter name: ')
    email = input('Enter email address: ')
    password = input('Enter password: ')

    insert_new_user(name,email,password)
elif login_register == 2:
    email = input('Enter email address: ')
    password = input('Enter password: ')
    print('login_user() is ' + str(login_user(email,password)))
    #login_user(email,password)
#
# #record_transaction('expense','purchase','laptop','',1280,6)
# transactions = get_all_expenses(6)
# print(transactions)