class Parent:
    def __init__(self, created_date):
        self.__created_date = created_date

    def set_created_date(self, created_date):
        self.__created_date = created_date

    def get_time(self):
        return self.__created_date