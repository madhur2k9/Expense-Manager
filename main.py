from Helper.Database_Connection import insert_new_user, set_config_file_path, login_user

set_config_file_path('config.ini')

login_register = int(input('Press 1 to Register and 2 for Login'))

if login_register == 1:
    name = input('Enter name')
    email = input('Enter email address')
    password = input('Enter password')

    insert_new_user(name,email,password)
elif login_register == 2:
    email = input('Enter email address')
    password = input('Enter password')
    print('login_user() is ' + str(login_user(email,password)))
    #login_user(email,password)