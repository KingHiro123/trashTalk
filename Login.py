from re import U
import User 

class Login(User.User):
    def __init__(self, user_id, name, address, username,  password):
        super().__init__(user_id, name, address)
        self.__username = username
        self.__password = password

    def get_username(self):
        return self.__username

    def get_password(self):
        return self.__password


    def set_username(self, username):
        self.__username = username

    def set_password(self, password):
        self.__password = password