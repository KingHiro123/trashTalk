from Base import *
from datetime import datetime

class Cart(Base):
    def __init__(self, user_id, cart_id):
        Base.__init__(self, datetime.now())
        self.total = 0
        self.items = {}