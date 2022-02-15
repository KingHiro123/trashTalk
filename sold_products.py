class Sold_Products():

    def __init__(self, sku, item_id, profit):
        self.__item_id = item_id
        self.__sku = sku
        self.__profit = profit

    def get_item_id(self):
        return self.__item_id

    def get_sku(self):
        return self.__sku

    def get_profit(self):
        return self.__profit

    def set_item_id(self, item_id):
        self.__item_id = item_id

    def set_sku(self, sku):
        self.__sku = sku

    def set_profit(self, profit):
        self.__profit = profit
