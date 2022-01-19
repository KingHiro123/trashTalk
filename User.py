class User:
    def __init__(self, user_id, name,address):
        self.__user_id = user_id
        self.__name = name
        self.__address= address

    def get_user_id(self):
        return self.__user_id

    def get_name(self):
        return self.__name

    def get_address(self):
        return self.__address

    
    def set_user_id(self, user_id):
        self.__user_id = user_id

    def set_name(self, name):
        self.__name = name
    
    def set_address(self, address):
        self.__email = address

  