from flask import Flask, render_template, request
from classes.cart import Cart
import shelve

app = Flask(__name__)


@app.route('/')
def productpage():
    # user_accounts = {}
    # db = shelve.open('user.db', 'r')
    # try:
    # if 'User' in db:
    # user_accounts = db['User']
    # else:
    # db['User'] = user_accounts
    # except:
    # print("Error in retrieving Items from user.db.")
    # db.close()

    # get username of account logged in
    return render_template('productpg.html')  # , username=username)


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

    cart_id = 1
    try:
        product_list = user_cart.get(cart_id)
    except:
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

    cart_id = 1
    try:
        product_list = user_cart.get(cart_id)
    except:
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

    cart_id = 1
    product_list = user_cart.get(cart_id)
    user_cart.pop(cart_id)
    print(product_list)

    # also minus product from itemdb storage
    # specific_dict = {}
    # db = shelve.open('stock.db', 'w')
    # specific_dict = db['Details']

    # print()
    # for key in product_list:      # key is the itemname
    #   specific_dict[key][quantity] -= productlist[key][2]     # make it to int() ?

    # db['Details'] = specific_dict
    # db.close()
    db['Cart'] = user_cart
    db.close()
    return render_template('productpg.html')


if __name__ == '__main__':
    app.run()
