from venv import create
from add_specific_items import AddItemForm
from TrashtalkInventoryform import AddFieldForm
import Item
import shelve
from specificItems import *
from create_sku import create_sku

from flask import Flask, render_template, request, redirect, url_for
import jinja2
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
    db.close()

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
                item.set_item_quantity(
                    item.get_item_quantity() + add_field_form.item_quantity.data)
                item_dict[item.get_item_id()] = item
                db['Items'] = item_dict
                db.close()
                return redirect(url_for('retrieve_fields'))

        item = Item.Item(add_field_form.item_brand.data,
                         add_field_form.item_description.data, add_field_form.item_quantity.data)
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
        if len(specific_dict) > 0:
            specific.set_specific_id(list(specific_dict)[-1]+1)
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

        for key in item_dict:
            item = item_dict[key]
            if update_field_form.item_brand.data == item.get_item_brand() and update_field_form.item_description.data == item.get_item_description() and update_field_form.item_quantity.data == item.get_item_quantity():
                item_dict[item.get_item_id()] = item
                db['Items'] = item_dict
                db.close()
                return redirect(url_for('retrieve_fields'))

            elif update_field_form.item_brand.data == item.get_item_brand() and update_field_form.item_description.data == item.get_item_description():
                count = item.get_item_quantity() + update_field_form.item_quantity.data
                item.set_item_quantity(count)
                print(item.get_item_quantity())
                print(item_dict.get(
                    key).get_item_quantity() + update_field_form.item_quantity.data)

                # item.set_item_quantity(update_field_form.item_quantity.data)
                item_dict.pop(id)
                item_dict[item.get_item_id()] = item
                db['Items'] = item_dict
                db.close()
                return redirect(url_for('retrieve_fields'))

            elif update_field_form.item_brand.data != item.get_item_brand() or update_field_form.item_description.data != item.get_item_description():

                item.set_item_brand(update_field_form.item_brand.data)
                item.set_item_description(
                    update_field_form.item_description.data)
                item.set_item_quantity(update_field_form.item_quantity.data)

                db['Items'] = item_dict
                db.close()
                return redirect(url_for('retrieve_fields'))

        item = Item.Item(update_field_form.item_brand.data,
                         update_field_form.item_description.data, update_field_form.item_quantity.data)
        if len(item_dict) > 0:
            item.set_item_id(list(item_dict)[-1]+1)
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
        update_field_form.item_quantity.data = item.get_item_quantity()

        return render_template('updateField.html', form=update_field_form)


@app.route('/admin/Inventory/updateDetails/<int:id>/', methods=['GET', 'POST'])
def update_details(id):
    update_item_form = AddItemForm(request.form)
    if request.method == 'POST' and update_item_form.validate():
        specific_dict = {}
        db = shelve.open('stock.db', 'c')
        specific_dict = db['Details']
        specific = None

        sku = specific_dict[specific.get_sku()]
        specific = Specific(sku,
                            update_item_form.datemanufactured.data, update_item_form.remarks.data)
        specific_dict[specific.get_specific_id()] = specific
        db['Details'] = specific_dict
        db.close()

        return redirect(url_for('retrieve_items', id=id))
    else:
        specific_dict = {}
        db = shelve.open('stock.db', 'r')
        specific_dict = db['Details']
        db.close()

        specific = specific_dict.get(id)
        update_item_form.datemanufactured.data = specific.get_datemanufactured()
        update_item_form.remarks.data = specific.get_remarks()

        return render_template('updateDetails.html', form=update_item_form)


@ app.route('/admin/Inventory/removeItem/<int:id>')
def remove_field(id):
    item_dict = {}
    db = shelve.open('stock.db', 'w')
    item_dict = db['Items']

    item_dict.pop(id)

    db['Items'] = item_dict
    db.close()

    return redirect(url_for('retrieve_fields'))


@app.route('/admin/Inventory/ItemDetails/removeDetail/<int:id>')
def remove_item(id):
    specific_dict = {}
    db = shelve.open('stock.db', 'w')
    specific_dict = db['Details']

    specific_dict.pop(id)

    db['Details'] = specific_dict
    db.close()

    return redirect(url_for('retrieve_items', id=id))


@ app.errorhandler(404)
def page_not_found(e):
    return render_template('error404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
