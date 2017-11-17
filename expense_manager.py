from flask import Flask, request, jsonify, session
from Helper.Database_Connection import *
from flask_cors import *
from Models.User import User

set_config_file_path('config.ini')

app = Flask(__name__)
cors = CORS(app)
user = None

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/register', methods = ['POST'])
@cross_origin()
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        message = 'Account successfully created!' if insert_new_user(name,email,password) else 'Email already exists'
        status = {'message': message, "status":200}
        return jsonify(status),200

@app.route('/login', methods = ['POST'])
@cross_origin()
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
            status = {'message': message}
            return jsonify(status), 200
        else:
            message = 'Invalid ID password combo :('
            status = {'message': message}
            return jsonify(status),401

@app.route('/logout', methods=['GET'])
@cross_origin()
def logout():
    session.pop('id')
    global user
    user = None
    return jsonify({"message": "Logout successful!"}),200

@app.route('/getBalance', methods=['GET'])
@cross_origin()
def get_balance():
    global user
    if user is not None:
        return jsonify({'new_balance': user.get_current_balance()}),200
    return jsonify({"message":"Please login!"}),401

#transac_type, category, title, description, amount, user_id

@app.route('/recordTransaction', methods=['POST'])
@cross_origin()
def recordTransaction():
    global user

    if user is not None:
        try:
            if (str(request.form["transaction_type"]).lower() == 'income'):
                transaction_type = True
            elif (str(request.form["transaction_type"]).lower() == 'expense'):
                transaction_type = False
            else:
                response = jsonify({'message':'Invalid transaction type.', 'status_code':400})
                return response,400

            category = str(request.form["category"])
            title = str(request.form["title"])
            description = str(request.form["description"])
            amount = str(request.form["amount"])
            user_id = str(user.get_id())

            record_transaction(transaction_type, category, title, description, amount, user_id, user.get_current_balance())
            response = jsonify({'message': 'Transaction recorded.'})
            return response,200
        except Exception as ex:
            return jsonify({"message": str(ex)}),400
    else:
        return jsonify({"message": "Please login!"}),401

@app.route('/getTransactions', methods=['GET'])
@cross_origin()
def getTransactions():
    global user

    if user is not None:
        try:
            response = {"transactions":get_all_transactions(user.get_id()), "current_balance": user.get_current_balance()}
            #response = get_all_expenses(user.get_id())
            return jsonify(response),200
        except Exception as ex:
            return jsonify({'message':str(ex)}),500
    return jsonify({'message':"Please login!"}),401

if __name__ == '__main__':
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    app.run(debug=True)
