class Item:
    count_id = 0

    def __init__(self, item_brand, item_description):
        Item.count_id += 1
        self.__item_id = Item.count_id
        self.__item_brand = item_brand
        self.__item_description = item_description

    def set_item_id(self, item_id):
        self.__item_id = item_id

    def set_item_brand(self, item_brand):
        self.__item_brand = item_brand

    def set_item_description(self, item_description):
        self.__item_description = item_description

    def get_item_id(self):
        return self.__item_id

    def get_item_brand(self):
        return self.__item_brand

    def get_item_description(self):
        return self.__item_description
