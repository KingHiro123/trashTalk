from classes.Base import *
from datetime import datetime


class Cart(Base):
    def __init__(self, cart_id):
        Base.__init__(self, datetime.now())
        self.__cart_id = cart_id
        self.items = {}

    def get_cart_id(self):
        return self.__cart_id

    def add_item(self, item_name, quantity, price):
        self.items.update({item_name: [price, quantity]})  # {product_id: [item_name, price, quantity]}
        return self.items

    def get_total(self):
        return self.items
