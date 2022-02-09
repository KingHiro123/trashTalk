import datetime
class Base:
    def __init__(self):
        self.__date = datetime.datetime.now()

    def set_created_date(self, created_date):
        self.__date = created_date

    def get_created_date(self):
        return self.__date
