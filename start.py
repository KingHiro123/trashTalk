import jinja2
from flask import Flask, render_template, request, redirect, url_for
from venv import create
from add_specific_items import AddItemForm
from TrashtalkInventoryform import AddFieldForm
import Item
import shelve
# from sold_products import Sold_Products
from specificItems import *
from create_sku import create_sku
# import os
# import shutil
# import numpy as np
# import pandas as pd
# import calendar
# from datetime import datetime
# from fpdf import FPDF


# import matplotlib.pyplot as plt
# from matplotlib import rcParams
# rcParams['axes.spines.top'] = False
# rcParams['axes.spines.right'] = False

env = jinja2.Environment()


app = Flask(__name__)
headings = ("Item ID", "Item Name", "Item Description", "Item Quantity")


@app.route('/createInventory', methods=['POST', 'GET'])
def create_inventory():
    return render_template('createInventory.html')


@app.route('/', methods=['POST', 'GET'])
def admin():
    return render_template('admin.html')


@app.route('/admin/Inventory')
def retrieve_fields():
    item_dict = {}
    db = shelve.open('stock.db', 'c')
    try:
        item_dict = db['Items']
    except:
        print("Error in retrieving Items from stock.db.")
    print(item_dict)

    # try:
    #     specific_dict = db['Details']
    # except:
    #     print("Error in retrieving Items from stock.db.")
    # db.close()

    # for key in item_dict:
    #     item = item_dict[key]

    # x = 0
    # y = 0
    # i = 0
    # for key in item_dict:
    #     item = item_dict[key]
    # for id in item_dict:
    #     specific_list = []
    #     quantity_list = []
    #     sku_dict = specific_dict.get(id)
    #     if sku_dict is None:
    #         sku_dict = {}
    #     for key in sku_dict:
    #         specific = sku_dict.get(key)
    #         x = len(specific_list)
    #         if y != x+1 and y != x:
    #             quantity_list.append(y)
    #         specific_list.append(specific)
    #         y = len(specific_list)

    item_list = []
    for key in item_dict:
        item = item_dict.get(key)
        item_list.append(item)

    return render_template('Inventory.html', count=len(item_list), item_list=item_list)


@app.route('/admin/Inventory/ItemDetails/<int:id>/', methods=["POST", "GET"])
def retrieve_items(id):
    print(id)
    item_dict = {}
    specific_dict = {}
    db = shelve.open('stock.db', 'c')

    try:
        item_dict = db['Items']
    except:
        print("Error in retrieving Items from stock.db.")

    item = item_dict[id]

    try:
        specific_dict = db['Details']
    except:
        print("Error in retrieving Items from stock.db.")
    db.close()
    print(item_dict)
    print(specific_dict)

    specific_list = []
    sku_dict = specific_dict.get(id)
    if sku_dict is None:
        sku_dict = {}
    for key in sku_dict:
        specific = sku_dict.get(key)
        specific_list.append(specific)
    return render_template('ItemDetails.html',  item=item, count2=len(specific_list), specific_list=specific_list)


@app.route('/admin/Inventory/addField', methods=['GET', 'POST'])
def add_field():
    add_field_form = AddFieldForm(request.form)
    if request.method == 'POST' and add_field_form.validate():
        item_dict = {}
        db = shelve.open('stock.db', 'c')

        try:
            item_dict = db['Items']
        except:
            print("Error in retrieving Items from stock.db.")

        for key in item_dict:
            item = item_dict[key]

            if add_field_form.item_brand.data == item.get_item_brand() and add_field_form.item_description.data == item.get_item_description():
                item_dict[item.get_item_id()] = item
                db['Items'] = item_dict
                db.close()
                return redirect(url_for('retrieve_fields'))

        item = Item.Item(add_field_form.item_brand.data,
                         add_field_form.item_description.data)
        if len(item_dict) > 0:
            item.set_item_id(list(item_dict)[-1]+1)
        item_dict[item.get_item_id()] = item
        db['Items'] = item_dict
        db.close()

        return redirect(url_for('retrieve_fields'))
    return render_template('add_field.html', form=add_field_form)


@app.route('/admin/Inventory/ItemDetails/<int:id>/AddDetail', methods=['GET', 'POST'])
def add_item(id):
    add_item_form = AddItemForm(request.form)
    print("Hello")
    if request.method == 'POST' and add_item_form.validate():
        specific_dict = {}
        sku_dict = {}
        db = shelve.open('stock.db', 'c')

        try:
            specific_dict = db['Details']
            sku_dict = specific_dict[id]
        except:
            print("Error in retrieving Items from stock.db.")

        run = True
        final_string = ""
        while run:
            run = False
            final_string = create_sku()

            for key in sku_dict:
                if final_string == key:
                    run = True

        specific = Specific(id, final_string,
                            add_item_form.datemanufactured.data, add_item_form.remarks.data)
        sku_dict[specific.get_sku()] = specific

        # specific.set_specific_id(max)
        # if len(specific_dict) > 0:
        #     specific.set_specific_id(list(sku_dict)[-1]+1)
        specific_dict[specific.get_item_id()] = sku_dict
        db['Details'] = specific_dict
        db.close()
        return redirect(url_for('retrieve_items', id=id))
    return render_template('add_item.html', form=add_item_form)


@app.route('/admin/Inventory/updateField/<int:id>/', methods=['GET', 'POST'])
def update_field(id):
    update_field_form = AddFieldForm(request.form)
    if request.method == 'POST' and update_field_form.validate():
        item_dict = {}
        db = shelve.open('stock.db', 'c')
        item_dict = db['Items']

        item = item_dict.get(id)
        item.set_item_brand(update_field_form.item_brand.data)
        item.set_item_description(update_field_form.item_description.data)
        item_dict[item.get_item_id()] = item
        db['Items'] = item_dict
        db.close()

        return redirect(url_for('retrieve_fields'))
    else:
        item_dict = {}
        db = shelve.open('stock.db', 'r')
        item_dict = db['Items']
        db.close()

        item = item_dict.get(id)
        update_field_form.item_brand.data = item.get_item_brand()
        update_field_form.item_description.data = item.get_item_description()

        return render_template('updateField.html', form=update_field_form)


@app.route('/admin/Inventory/updateDetails/<int:id>/<sku>', methods=['GET', 'POST'])
def update_details(id, sku):
    update_item_form = AddItemForm(request.form)
    print(id)
    if request.method == 'POST' and update_item_form.validate():
        specific_dict = {}
        db = shelve.open('stock.db', 'c')
        specific_dict = db['Details']
        specific = None

        sku_dict = specific_dict[id]
        specific = sku_dict[sku]
        specific = Specific(
            id, sku, update_item_form.datemanufactured.data, update_item_form.remarks.data)
        sku_dict[sku] = specific
        specific_dict[specific.get_item_id()] = sku_dict
        db['Details'] = specific_dict
        db.close()

        return redirect(url_for('retrieve_items', id=id))
    else:
        specific_dict = {}
        db = shelve.open('stock.db', 'r')
        specific_dict = db['Details']
        db.close()

        sku_dict = specific_dict.get(id)
        specific = sku_dict.get(sku)
        update_item_form.datemanufactured.data = specific.get_datemanufactured()
        update_item_form.remarks.data = specific.get_remarks()

        return render_template('updateDetails.html', form=update_item_form)


@ app.route('/admin/Inventory/removeField/<int:id>')
def remove_field(id):
    item_dict = {}
    specific_dict = {}
    db = shelve.open('stock.db', 'w')
    try:
        item_dict = db['Items']
    except:
        print("Error in retrieving Items from stock.db.")

    try:
        specific_dict = db['Details']
    except:
        print("Error in retrieving Items from stock.db.")

    item_dict.pop(id)
    if id in specific_dict:
        specific_dict.pop(id)

    db['Items'] = item_dict
    db['Details'] = specific_dict
    db.close()

    return redirect(url_for('retrieve_fields'))


@app.route('/admin/Inventory/ItemDetails/<int:id>/removeDetail/<sku>')
def remove_item(id, sku):
    specific_dict = {}
    db = shelve.open('stock.db', 'w')
    specific_dict = db['Details']
    sku_dict = specific_dict[id]
    if sku in sku_dict:
        specific_dict.pop(sku)

    db['Details'] = specific_dict
    db.close()

    return redirect(url_for('retrieve_items', id=id))


@ app.errorhandler(404)
def page_not_found(e):
    return render_template('error404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)

# @app.route('/admin/Inventory/Sold_Products')
# def sold_products():
#     item_dict = {}
#     sold_dict = {}
#     user_cart = {}
#     cart_id = 1
#     db = shelve.open('cart.db', 'c')
#     product_list = user_cart.get(cart_id)
#     user_cart.pop(cart_id)
#     print(product_list)
#     db.close()
#     db = shelve.open('stock.db', 'c')

#     try:
#         item_dict = db['Items']
#     except:
#         print("Error in retrieving Items from stock.db.")

#     try:
#         specific_dict = db['Details']
#     except:
#         print("Error in retrieving Items from stock.db.")

#     try:
#         sold_dict = db['Sold']
#     except:
#         print("Error in retrieving Items from stock.db.")

#     product_list = ['ROG']
#     indiv_profit = 0
#     total_profit = 0

#     for key in item_dict:
#         item = item_dict[key]
#     if sku_dict is None:
#         sku_dict = {}
#     for name, value in product_list.items():
#         item_description = name
#         for key in item_dict:
#             if item.get_item_description() == item_description:
#                 y = key
#                 for key in specific_dict:
#                     sold_sku = sku_dict[y]
#         indiv_profit = value[1] * value[2]
#         total_profit = indiv_profit + total_profit
#         sold_products = Sold_Products(sold_sku, y, total_profit)
#         for key, value in specific_dict.items():
#             if value == sold_sku:
#                 print(key + "key")
#                 print(value + "val")
#                 specific_dict.pop(key)
#                 db['Details'] = specific_dict

#         sold_dict[sold_products.get_sku()] = sold_products
#         db['Sold'] = sold_dict
#         db.close()

#     sold_list = []
#     for key in sold_dict:
#         sold = sold_dict.get(key)
#         sold_list.append(sold)

#     return render_template('items_sold.html', sold_dict=sold_dict, sold_list=sold_list)
