
import jinja2
from flask import Flask, render_template, url_for, redirect, request, flash, session
from classes.cart import Cart
from venv import create
from add_specific_items import AddItemForm
from TrashtalkInventoryform import AddFieldForm
from Base_Rachel import *
from datetime import datetime
from Forms import Signup_Form, Login_Form, CreateVoucherForm
from forms_Rachel import CreateFaqForm, CreateFeedbackForm
from flask_session import Session
import shelve, signUp, Voucher, Faq, Feedback, Item, Feedback
from flask_login import current_user, login_required, login_user, logout_user, LoginManager
from specificItems import *
from flask_socketio import SocketIO, join_room, leave_room, emit
from create_sku import create_sku
import hashlib

app = Flask(__name__)
login_manager = LoginManager(app)
env = jinja2.Environment()
headings = ("Item ID", "Item Name", "Item Description", "Item Quantity")

app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = 'Thisisthefinaltimeiamtouchingcodeforawhile'


Session(app)
socketio = SocketIO(app, manage_session=False)

#update account list design 
#profile for customer
#

@login_manager.user_loader
def load_user(user_id):
    db = shelve.open('sign_up.db', 'r')
    signup_dict = db['signUp']
    db.close()

    return signup_dict.get(user_id)

#Affan's code
@app.route('/')
def productpage():
    
    print('helo')
    
    return render_template('productpg.html')  # , username=username)
    
#Joana's Code
#@app.route("/admin")
#def home():
    
#    return render_template("Home_Admin.html", current_user=current_user)

#Account Management
@app.route('/account')
def acc_list():
    signup_dict = {}
    try:
        db = shelve.open('sign_up.db', 'r')
        signup_dict = db['signUp']
        db.close()
    except IOError:
        print("Error has occurred while trying to read.")
    except:
        print('An unknown error has occurred.')
    
    acc_list = []
    for key in signup_dict:
        list = signup_dict.get(key)
        acc_list.append(list)

    return render_template('Acc_Man.html', count=len(acc_list), acc_list=acc_list)

#view
@app.route('/ViewUser/<int:id>', methods=['POST'])
def view_user(id):
    user_dict = {}
    db = shelve.open('sign_up.db', 'r')
    user_dict = db['signUp']
    db.close()

    acc_list = []
    for id in user_dict:
        list = user_dict.get(id)
        acc_list.append(list)

    return redirect(url_for('acc_list'))
#update
@app.route('/Update/<int:id>/', methods=['GET', 'POST'])
def update_signup(id):
    update_signup_form = Signup_Form(request.form)
    if request.method == 'POST' and update_signup_form.validate():
        user_dict = {}
        db = shelve.open('sign_up.db', 'w')
        user_dict = db['signUp']

        list = user_dict.get(id)
        list.set_username(update_signup_form.username.data)
        list.set_email(update_signup_form.email.data)
        list.set_password(update_signup_form.password.data)
        list.set_confirmpass(update_signup_form.confirmpass.data)

        db['signUp'] = user_dict
        db.close()

        return redirect(url_for('acc_list'))
    else:
        user_dict = {}
        db = shelve.open('sign_up.db', 'r')
        user_dict = db['signUp']
        db.close()

        list = user_dict.get(id)
        update_signup_form.username.data = list.get_username()
        update_signup_form.email.data = list.get_email()
        update_signup_form.password.data = list.get_password()
        update_signup_form.confirmpass.data = list.get_confirmpass()

        return render_template('Update_nameList.html', form=update_signup_form)

#delete
@app.route('/deleteUser/<int:id>', methods=['POST'])
def delete_user(id):
    user_dict = {}
    db = shelve.open('sign_up.db', 'w')
    user_dict = db['signUp']

    user_dict.pop(id)

    db['signUp'] = user_dict
    db.close()

    return redirect(url_for('acc_list'))

#Log in
@app.route('/login', methods=['GET','POST'])
  
def login():

    login = Login_Form(request.form)
    if request.method == "POST" and login.validate():
        users_dict = {}
        
        try:
            db = shelve.open('sign_up.db', 'r')
            users_dict = db['signUp']

            for key in users_dict:
                user = users_dict[key]
                
                attempted_username = request.form['username']
                attempted_password = request.form['password']

                #the admin is still being tested, once the group has their code integrated
                if attempted_username == 'admin' and attempted_password == 'password':
                    login_user(user)

                    return redirect(url_for('acc_list'))
                else:
                    if login.username.data != user.get_username() or login.password.data != user.get_password():
                        flash(f'Invalid username or password! Please check your login details and try again.', 'warning')
                        return redirect(url_for('login'))
                
            flash(f'Successfully logged in!', 'success')
            db.close()
            login_user(user)
        
            return redirect(url_for('productpage', current_user=current_user))   

        except IOError:
            print("Error, it does not exist")
    

    return render_template('Login_Tryouts.html', form=login)

#Sign up
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    sign_up = Signup_Form(request.form)
    if request.method == 'POST' and sign_up.validate():
        signup_dict = {}
        db = shelve.open('sign_up.db', 'c')

        try:
            signup_dict = db['signUp']
        except:
            print("Error in retrieving Users from sign_up.db")

        if len(signup_dict) > 0:
            for key in signup_dict:
                    user = signup_dict[key]

                    if sign_up.username.data == user.get_username():
                        flash('This username has already been used.', 'warning')

                        return redirect(url_for('signup'))

                    elif sign_up.email.data == user.get_email():
                        flash('This email has already been used.', 'warning')

                        return redirect(url_for('signup'))

            s_up = signUp.Signup(sign_up.username.data, sign_up.email.data, sign_up.password.data, sign_up.confirmpass.data)

            flash(f'Account created for {sign_up.username.data}!', 'success')
            if len(signup_dict) > 0:
                s_up.set_user_id(list(signup_dict)[-1]+1) 

            signup_dict[s_up.get_user_id()] = s_up
            db['signUp'] = signup_dict
            db.close()

            return redirect(url_for('productpage'))
        else:
            s_up = signUp.Signup(sign_up.username.data, sign_up.email.data, sign_up.password.data, sign_up.confirmpass.data)

            flash(f'Account created for {sign_up.username.data}!', 'success')
            signup_dict[s_up.get_user_id()] = s_up
            db['signUp'] = signup_dict
            db.close()

            return redirect(url_for('productpage'))

    return render_template('Signup_Tryouts.html', form=sign_up)

#Logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('productpage'))

#Authentication
@app.route('/login_authentication', methods=['GET', 'POST'])
def auth():
    if request.method == 'GET':
        if current_user.is_authenticated:
            return render_template("productpg.html")
        else:
            return render_template("Login.html")




#Reegan's Code
@app.route('/rewards')
def rewards():
    vouchers_dict = {}
    db = shelve.open('voucher.db', 'r')
    vouchers_dict = db['Vouchers']
    db.close()

    vouchers_list = []
    for key in vouchers_dict:
        voucher = vouchers_dict.get(key)
        vouchers_list.append(voucher)
    print(vouchers_list)
    return render_template('rewards.html', count=len(vouchers_list), vouchers_list=vouchers_list)

@app.route('/claimedRewards')
def claimed_rewards():
    current_user_id = 0
    vouchers_dict = {}
    db = shelve.open('voucher.db', 'r')
    vouchers_dict = db['Vouchers']
    db.close()

    vouchers_list = []
    for key in vouchers_dict:
        voucher = vouchers_dict.get(key)
        vouchers_list.append(voucher)

    return render_template('claimedRewards.html', count=len(vouchers_list), vouchers_list=vouchers_list)

@app.route('/claimVoucher/<int:id>', methods=['GET', 'POST'])
@login_required
def claim_voucher(id):

        vouchers_dict = {}
        db = shelve.open('voucher.db', 'c')

        try:
            vouchers_dict = db['Vouchers']
        except:
            print("Error in retrieving Vouchers from voucher.db.")
        print(vouchers_dict)
        print(id)
        voucher = vouchers_dict[id]
        voucher.set_claimed(current_user.get_id())
        vouchers_dict[id] = voucher
        db['Vouchers'] = vouchers_dict

        db.close()

        return redirect(url_for('retrieve_vouchers'))

@app.route('/createVoucher', methods=['GET', 'POST'])
def create_voucher():
    create_voucher_form = CreateVoucherForm(request.form)
    if request.method == 'POST' and create_voucher_form.validate():
        vouchers_dict = {}
        db = shelve.open('voucher.db', 'c')

        try:
            vouchers_dict = db['Vouchers']
        except:
            print("Error in retrieving Vouchers from voucher.db.")

        voucher = Voucher.Voucher(create_voucher_form.discount.data, create_voucher_form.expiry_date.data, create_voucher_form.points.data)
        voucher_list = []
        for key in vouchers_dict:
            id = voucher.get_voucher_id()
            voucher_list.append(id)
        count_id = len(voucher_list) + 1
        voucher.set_voucher_id(count_id)
        vouchers_dict[voucher.get_voucher_id()] = voucher
        db['Vouchers'] = vouchers_dict

        db.close()

        return redirect(url_for('retrieve_vouchers'))
    return render_template('createVoucher.html', form=create_voucher_form)

@app.route('/retrieveVoucher', methods=['GET','POST'])
def retrieve_vouchers():
    vouchers_dict = {}
    db = shelve.open('voucher.db', 'r')
    vouchers_dict = db['Vouchers']
    db.close()

    vouchers_list = []
    for key in vouchers_dict:
        voucher = vouchers_dict.get(key)
        vouchers_list.append(voucher)

    return render_template('retrieveVoucher.html', count=len(vouchers_list), vouchers_list=vouchers_list)

@app.route('/updateVoucher/<int:id>/',methods=['GET','POST'])
def update_voucher(id):
    update_voucher_form = CreateVoucherForm(request.form)
    if request.method =="POST" and update_voucher_form.validate():
        vouchers_dict = {}
        db = shelve.open('voucher.db','w')
        vouchers_dict = db['Vouchers']

        voucher = vouchers_dict.get(id)
        voucher.set_discount(update_voucher_form.discount.data)
        voucher.set_expiry_date(update_voucher_form.expiry_date.data)
        voucher.set_points(update_voucher_form.points.data)

        db['Vouchers'] = vouchers_dict
        db.close()

        return redirect(url_for('retrieve_vouchers'))
    else:
        vouchers_dict = {}
        db = shelve.open('voucher.db', 'r')
        vouchers_dict = db['Vouchers']
        db.close()

        voucher = vouchers_dict.get(id)
        update_voucher_form.discount.data = voucher.get_discount()
        update_voucher_form.expiry_date.data = voucher.get_expiry_date()
        update_voucher_form.points.data = voucher.get_points()

        return render_template('updateVoucher.html', form=update_voucher_form)

@app.route('/deleteVoucher/<int:id>',methods=['POST'])
def delete_voucher(id):
    vouchers_dict = {}
    db = shelve.open('voucher.db','w')
    vouchers_dict = db['Vouchers']

    vouchers_dict.pop(id)

    db['Vouchers'] = vouchers_dict
    db.close()

    return redirect(url_for('retrieve_vouchers'))

#affan's code
@app.route('/addtocart/', methods=['GET', 'POST'])
def addtocart():
    user_cart = {}
    db = shelve.open('cart.db', 'c')

    try:
        if 'Cart' in db:
            user_cart = db['Cart']
        else:
            db['Cart'] = user_cart
    except:
        print("Error in retrieving Items from cart.db.")
        
    if current_user.is_authenticated:
        cart_id = current_user.get_username()
    else:
        cart_id = 1
    c = Cart(cart_id)
    c.add_item(item_name=request.json['name'], quantity=1, price=request.json['price'])
    print(c.get_total())

    try:
        cart = user_cart.get(cart_id)
        cart.update(c.get_total())
        user_cart[cart_id] = cart
    except:
        user_cart[cart_id] = (c.get_total())

    print(user_cart.get(cart_id))
    db['Cart'] = user_cart

    db.close()
    print('Add cart successful')
    return 's'


@app.route('/usercart')
def usercart():
    user_cart = {}
    db = shelve.open('cart.db', 'r')
    try:
        if 'Cart' in db:
            user_cart = db['Cart']
        else:
            db['Cart'] = user_cart
    except:
        print("Error in retrieving Items from cart.db.")
    db.close()

    if current_user.is_authenticated:
        cart_id = current_user.get_username()
    else:
        cart_id = 1
    product_list = user_cart.get(cart_id)

    if product_list == None:
        product_list = {"No products yet": [0, 0]}

    print(product_list)

    return render_template('usercart.html', product_list=product_list)


@app.route('/additem/<itemname><int:quantity>', methods=['POST'])
def additem(itemname, quantity):
    user_cart = {}
    db = shelve.open('cart.db', 'w')
    user_cart = db['Cart']

    if current_user.is_authenticated:
        cart_id = current_user.get_username()
    else:
        cart_id = 1
    quantity += 1
    product_list = user_cart.get(cart_id)
    product_list[itemname][1] = int(quantity)
    print(product_list)
    user_cart[cart_id] = product_list
    db['Cart'] = user_cart

    db.close()
    return render_template('usercart.html', product_list=product_list)


@app.route('/removeitem/<itemname><int:quantity>', methods=['POST'])
def removeitem(itemname, quantity):
    user_cart = {}
    db = shelve.open('cart.db', 'w')
    user_cart = db['Cart']

    if current_user.is_authenticated:
        cart_id = current_user.get_username()
    else:
        cart_id = 1
    quantity -= 1
    product_list = user_cart.get(cart_id)
    if quantity == 0:
        product_list.pop(itemname)
    else:
        product_list[itemname][1] = int(quantity)
    print(product_list)
    user_cart[cart_id] = product_list
    db['Cart'] = user_cart

    db.close()
    return render_template('usercart.html', product_list=product_list)


@app.route('/mice')
def mice():
    return render_template('mice.html')


@app.route('/audio')
def audio():
    return render_template('audio.html')


@app.route('/keyboards')
def keyboards():
    return render_template('keyboards.html')


@app.route('/monitors')
def monitors():
    return render_template('monitors.html')


@app.route('/rogmonitor')
def rogmonitor():
    return render_template('ROGmonitor.html')


@app.route('/razerkraken')
def razerkraken():
    return render_template('razerkraken.html')


@app.route('/logimouse')
def logimouse():
    return render_template('logimouse.html')


@app.route('/vipermini')
def vipermini():
    return render_template('vipermini.html')


@app.route('/corsairkeyboard')
def corsairkeyboard():
    return render_template('corsairkeyboard.html')


@app.route('/infopage')
def infopage():
    user_cart = {}
    db = shelve.open('cart.db', 'r')
    try:
        if 'Cart' in db:
            user_cart = db['Cart']
        else:
            db['Cart'] = user_cart
    except:
        print("Error in retrieving Items from cart.db.")
    db.close()
    
    if current_user.is_authenticated:
        cart_id = current_user.get_username()
    else:
        cart_id = 1
        
    product_list = user_cart.get(cart_id)
    
    if product_list == None:
        product_list = {"No products yet": [0, 0]}

    print(product_list)
    return render_template('infopage.html', product_list=product_list)


@app.route('/paymentpage')
def paymentpage():
    user_cart = {}
    db = shelve.open('cart.db', 'r')
    try:
        if 'Cart' in db:
            user_cart = db['Cart']
        else:
            db['Cart'] = user_cart
    except:
        print("Error in retrieving Items from cart.db.")
    db.close()

    if current_user.is_authenticated:
        cart_id = current_user.get_username()
    else:
        cart_id = 1
        
    product_list = user_cart.get(cart_id)
    
    if product_list == None:
        product_list = {"No products yet": [0, 0]}

    print(product_list)

    vouchers_dict = {}
    db = shelve.open('voucher.db', 'r')
    vouchers_dict = db['Vouchers']
    db.close()

    vouchers_list = []
    for key in vouchers_dict:
        voucher = vouchers_dict.get(key)
        vouchers_list.append(voucher)

    print(vouchers_list)
    return render_template('paymentpage.html', product_list=product_list, vouchers_list=vouchers_list)


@app.route('/complete')
def completeorder():
    user_cart = {}
    db = shelve.open('cart.db', 'w')
    user_cart = db['Cart']
    
    if current_user.is_authenticated:
        cart_id = current_user.get_username()
    else:
        cart_id = 1
    product_list = user_cart.get(cart_id)
    user_cart.pop(cart_id)
    
    db['Cart'] = user_cart
    db.close()
    
    item_dict = {}
    db = shelve.open('stock.db', 'w')
    item_dict = db['Items']

    #for key in item_dict:
    #item = item_dict[key]

    #for name, value in product_list.items():
    #  sold_quantity = value
    # if item.get_item_description() == name:
    #      int(item.get_item_quantity()) -= int(sold_quantity)
    #      item.set_item_quantity(quantity)

    db['Items'] = item_dict
    db.close()
    return render_template('productpg.html')


#Josh's Code
@app.route('/createInventory', methods=['POST', 'GET'])
def create_inventory():
    return render_template('createInventory.html')


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


#Rachel's code
@app.route('/support')
def custmain():
    return render_template('custmain.html')


@app.route('/createfaq', methods=['GET', 'POST'])
def create_faq():
    create_faq_form = CreateFaqForm(request.form)
    if request.method == 'POST' and create_faq_form.validate():
        faq_dict = {}
        db = shelve.open('faq.db', 'c')

        try:
            faq_dict = db['FAQ']

        except:
            print("Error in retrieving data")

        faq = Faq.Faq(create_faq_form.question.data, create_faq_form.answer.data)
        faq_dict[faq.get_question_id()] = faq
        db['FAQ'] = faq_dict

        faq_dict = db['FAQ']
        faq = faq_dict[faq.get_question_id()]
        print(faq.get_question(), faq.get_answer(), "was stored in faq.db successfully with id: ", faq.get_question_id())

        db.close()

        return redirect(url_for('acc_list'))
    return render_template('createfaq.html', form=create_faq_form)


@app.route('/custfaq')
def cust_faq():
    faq_dict = {}
    db = shelve.open('faq.db', 'r')
    faq_dict = db['FAQ']
    db.close()
    faq_list = []

    for key in faq_dict:
        faq = faq_dict.get(key)

        faq_list.append(faq)
    return render_template('custfaq.html', count=len(faq_list), faq_list=faq_list)


@app.route('/retrievefaq')
def retrieve_faq():
    faq_dict = {}
    db = shelve.open('faq.db', 'r')
    faq_dict = db['FAQ']
    db.close()
    faq_list = []

    for key in faq_dict:
        faq = faq_dict.get(key)

        faq_list.append(faq)
    return render_template('retrievefaq.html', count=len(faq_list), faq_list=faq_list)


@app.route('/updatefaq/<int:id>/', methods=['GET', 'POST'])
def update_faq(id):
    update_faq_form = CreateFaqForm(request.form)
    if request.method == 'POST' and update_faq_form.validate():
        faq_dict = {}
        db = shelve.open('faq.db', 'w')
        faq_dict = db['FAQ']

        faq = faq_dict.get(id)
        faq.set_question(update_faq_form.question.data)
        faq.set_answer(update_faq_form.answer.data)

        db['FAQ'] = faq_dict
        db.close()

        return redirect(url_for('retrieve_faq'))
    else:
        faq_dict = {}
        db = shelve.open('faq.db', 'r')
        faq_dict = db['FAQ']
        db.close()

        faq = faq_dict.get(id)
        update_faq_form.question.data = faq.get_question()
        update_faq_form.answer.data = faq.get_answer()

        return render_template('updatefaq.html', form=update_faq_form)


@app.route('/deletefaq/<int:id>', methods=['POST'])
def delete_faq(id):
    faq_dict = {}
    db = shelve.open('faq.db', 'w')
    faq_dict = db['FAQ']

    faq_dict.pop(id)

    db['FAQ'] = faq_dict
    db.close()

    return redirect(url_for('retrieve_faq'))


@app.route('/createfeedback', methods=['GET', 'POST'])
def create_feedback():
    create_feedback_form = CreateFeedbackForm(request.form)
    if request.method == 'POST' and create_feedback_form.validate():
        feedback_dict = {}
        db = shelve.open('feedback.db', 'c')

        try:
            feedback_dict = db['Feedback']

        except:
            print("Error in retrieving data")

        feedback = Feedback.Feedback(create_feedback_form.name.data, create_feedback_form.subject.data, create_feedback_form.content.data)
        feedback_dict[feedback.get_feedback_id()] = feedback
        db['Feedback'] = feedback_dict

        feedback_dict = db['Feedback']
        feedback = feedback_dict[feedback.get_feedback_id()]
        print(feedback.get_name(), feedback.get_subject(), feedback.get_content(), "was stored in feedback.db successfully with id: ", feedback.get_feedback_id())

        db.close()

        return redirect(url_for('acc_list'))
    return render_template('createfeedback.html', form=create_feedback_form)


@app.route('/retrievefeedback')
def retrieve_feedback():
    feedback_dict = {}
    db = shelve.open('feedback.db', 'r')
    feedback_dict = db['Feedback']
    db.close()
    feedback_list = []

    for key in feedback_dict:
        feedback = feedback_dict.get(key)

        feedback_list.append(feedback)
    return render_template('retrievefeedback.html', count=len(feedback_list), feedback_list=feedback_list)


@app.route('/deletefeedback/<int:id>', methods=['POST'])
def delete_feedback(id):
    feedback_dict = {}
    db = shelve.open('feedback.db', 'w')
    feedback_dict = db['Feedback']

    feedback_dict.pop(id)

    db['Feedback'] = feedback_dict
    db.close()

    return redirect(url_for('retrieve_feedback'))


@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        print()
        username = request.form['username']
        room = request.form['room']
        session['username'] = username
        session['room'] = room
        return render_template('chat.html', session=session)
    else:
        if session.get('username') is not None:
            print()
            return render_template('chat.html', session=session)
        else:
            return redirect(url_for('index'))


@socketio.on('join', namespace='/chat')
def join():
    room = session.get('room')
    join_room(room)
    emit('status', {'msg': session.get('username') + ' has entered the room.'}, room=room)


@socketio.on('text', namespace='/chat')
def text(message):
    room = session.get('room')
    emit('message', {'msg': session.get('username') + ' : ' + message['msg']}, room=room)


@socketio.on('left', namespace='/chat')
def left(message):
    room = session.get('room')
    username = session.get('username')
    leave_room(room)
    session.clear()
    emit('status', {'msg': username + ' has left the room.'}, room=room)

if __name__ == '__main__':
    socketio.run(app)

if __name__ == '__main__':
    app.run(debug=True)