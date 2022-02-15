
from flask import Flask, render_template, url_for, redirect, request, flash, session
from flask_rbac import RBAC
from Forms import Signup_Form, Login_Form, CreateVoucherForm
import shelve, signUp, Voucher
from flask_login import current_user, login_required, login_user, logout_user, LoginManager

import hashlib


app = Flask(__name__)
login_manager = LoginManager(app)
@login_manager.user_loader
def load_user(user_id):
    db = shelve.open('sign_up.db', 'r')
    signup_dict = db['signUp']
    db.close()

    return signup_dict.get(user_id)

app.config['SECRET_KEY'] = 'bananaisagoodfruit'
@app.route("/")
def home():
    return render_template("Home_Admin.html", current_user=current_user)

#Log in

@app.route('/login', methods=['GET','POST'])

def login():

    login = Login_Form(request.form)
    if request.method == "POST" and login.validate():
        users_dict = {}
        
        try:
            db = shelve.open('sign_up.db', 'r')
            users_dict = db['signUp']

            attempted_username = request.form['username']
            attempted_password = request.form['password']

            for key in users_dict:
                user = users_dict[key]
                
                #the admin is still being tested, once the group has their code integrated
                if attempted_username == 'admin' and attempted_password == 'password':
                    login_user(user)
                    return redirect(url_for('home'))
                else:
                    if login.username.data != user.get_username() or login.password.data != user.get_password():
                        flash(f'Invalid username or password! Please check your login details and try again.', 'warning')

                        return redirect(url_for('login'))
                
            login_user(user)
            flash(f'Successfully logged in!', 'success')
            db.close()

            print(user)
            return redirect(url_for('home', current_user=current_user))   

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
                        flash('This username has already been used.')

                        return redirect(url_for('signup'))

                    elif sign_up.email.data == user.get_email():
                        flash('This email has already been used.')

                        return redirect(url_for('signup'))
                    
            s_up = signUp.Signup(sign_up.username.data, sign_up.email.data, sign_up.password.data, sign_up.confirmpass.data)

            flash(f'Account created for {sign_up.username.data}!', 'success')
            if len(signup_dict) > 0:
                s_up.set_user_id(list(signup_dict)[-1]+1) 

            signup_dict[s_up.get_user_id()] = s_up
            db['signUp'] = signup_dict
            db.close()

            return redirect(url_for('acc_list'))
        else:
            s_up = signUp.Signup(sign_up.username.data, sign_up.email.data, sign_up.password.data, sign_up.confirmpass.data)

            flash(f'Account created for {sign_up.username.data}!', 'success')
            signup_dict[s_up.get_user_id()] = s_up
            db['signUp'] = signup_dict
            db.close()

            return redirect(url_for('acc_list'))

    return render_template('Signup_Tryouts.html', form=sign_up)

#Logout
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

#Authentication
@app.route('/login_authentication', methods=['GET', 'POST'])
def auth():
    if request.method == 'GET':
        if current_user.is_authenticated:
            return render_template("Home_Admin.html")
        else:
            return render_template("Login.html")


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

if __name__ == "__main__":
    app.run(debug=True)
