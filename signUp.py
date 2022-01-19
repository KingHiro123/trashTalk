class Signup:
    count_id = 0

    def __init__(self, username, email, password, confirmpass):
        Signup.count_id += 1
        self.__user_id = Signup.count_id
        self.__username = username
        self.__email = email
        self.__password = password
        self.__confirmpass = confirmpass


    def get_user_id(self):
        return self.__user_id

    def get_username(self):
        return self.__username

    def get_password(self):
        return self.__password

    def get_email(self):
        return self.__email

    def get_confirmpass(self):
        return self.__confirmpass


    def set_user_id(self, user_id):
        self.__user_id = user_id

    def set_username(self, username):
        self.__username = username

    def set_email(self, email):
        self.__email = email

    def set_password(self, password):
        self.__password = password

    def set_confirmpass(self, confirmpass):
        self.__confirmpass = confirmpass

