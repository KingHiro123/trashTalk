from ParentTime import *
from datetime import datetime


class Specific(Parent):

    def __init__(self, item_id, sku, datemanufactured, remarks):
        Parent.__init__(self, datetime.now())
        self.__item_id = item_id
        self.__sku = sku
        self.__datemanufactured = datemanufactured
        self.__remarks = remarks

    def get_item_id(self):
        return self.__item_id

    def get_sku(self):
        return self.__sku

    def get_datemanufactured(self):
        return self.__datemanufactured

    def get_remarks(self):
        return self.__remarks

    def set_item_id(self, item_id):
        self.__item_id = item_id

    def set_sku(self, sku):
        self.__sku = sku

    def set_datemanufactured(self, datemanufactured):
        self.__datemanufactured = datemanufactured

    def set_remarks(self, remarks):
        self.__remarks = remarks