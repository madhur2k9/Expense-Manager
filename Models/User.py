class User:
    #Constructor for user class
    def __init__(self, id, email, password, name, date_created, last_login_date, current_balance):
        self._id = id
        self._email = email
        self._password = password
        self._name = name
        self._date_created = date_created
        self._last_login_date = last_login_date
        self._current_balance = current_balance

    # Setter methods
    def set_name(self, name):
        self._name = name

    def set_password(self, password):
        self._password = password
    
    def get_id(self):
        return self._id

    def get_email(self):
        return self._email

    def get_name(self):
        return self._name

    def get_date_created(self):
        return self._date_created

    def get_last_login_date(self):
        return self._last_login_date

    def get_current_balance(self):
        return self._current_balance