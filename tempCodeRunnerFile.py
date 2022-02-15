# @app.route('/admin/Inventory/ItemDetails/<int:id>/AddItem', methods=['GET', 'POST'])
# def add_item(id):
#     add_item_form = AddItemForm(request.form)
#     if request.method == 'POST' and add_item_form.validate():
#         specific_dict = {}
#         db = shelve.open('stock.db', 'c')

#         try:
#             specific_dict = db['Items']
#         except:
#             print("Error in retrieving Items from stock.db.")

#         specific = Specific(add_item_form.datemanufacture.data,
#                             add_item_form.remarks.data)
#         specific_dict[specific.get_serial_number()] = specific
#         db['Items'] = specific_dict
#         db.close()
#         return redirect(url_for('retrieve_fields'))
