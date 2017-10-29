from flask import Flask, request, jsonify, session
from Helper.Database_Connection import insert_new_user, set_config_file_path, login_user, record_transaction, \
    get_all_transactions, get_all_expenses, get_all_incomes, get_user_id, get_user
from Models.User import User

set_config_file_path('config.ini')

app = Flask(__name__)

user = None

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/register', methods = ['POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        message = 'Account successfully created!' if insert_new_user(name,email,password) else 'Email already exists'
        status = {'message': message}
        return jsonify(status)

@app.route('/login', methods = ['POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        result = login_user(email,password)
        if result:
            global user
            user = get_user()
            session['id'] = user.get_id()
            message = 'Login successful! :)'
        else:
            message = 'Invalid ID password combo :('
        status = {'message': message}
        return jsonify(status)

@app.route('/logout', methods=['GET'])
def logout():
    session.pop('id')
    global user
    user = None

@app.route('/getBalance', methods=['GET'])
def get_balance():
    global user
    if user is not None:
        return jsonify({'new_balance': user.get_current_balance()})
    return jsonify({"message":"Please login!"})



if __name__ == '__main__':
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    app.run()
