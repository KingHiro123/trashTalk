from Base import Base


class Voucher(Base):
    count_id = 0

    def __init__(self, discount, expiry_date, points):
        super().__init__()
        self.__voucher_id = Voucher.count_id
        self.__discount = discount
        self.__expiry_date = expiry_date
        self.__points = points
        self.__claimed = None

    def get_voucher_id(self):
        return self.__voucher_id

    def get_discount(self):
        return self.__discount

    def get_expiry_date(self):
        return self.__expiry_date

    def get_points(self):
        return self.__points

    def get_claimed(self):
        return self.__claimed

    def set_voucher_id(self, voucher_id):
        self.__voucher_id = voucher_id

    def set_discount(self, discount):
        self.__discount = discount

    def set_expiry_date(self, expiry_date):
        self.__expiry_date = expiry_date

    def set_points(self, points):
        self.__points = points

    def set_claimed(self, claimed):
        self.__claimed = claimed
