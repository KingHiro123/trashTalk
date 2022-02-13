from cmath import log
from multiprocessing.sharedctypes import Value
from flask import Flask, render_template, url_for, redirect, request, flash
from flask_rbac import RBAC
from Forms import Signup_Form, Login_Form
import shelve, signUp
from flask_login import current_user, login_user, logout_user, LoginManager
import hashlib


app = Flask(__name__)
rbac = RBAC(app)
login_manager = LoginManager(app)
@login_manager.user_loader
def load_user(user_id):
    db = shelve.open('sign_up.db', 'r')
    signup_dict = db['signUp']
    db.close()

    return signup_dict.get(user_id)

app.config['RBAC_USE_WHITE'] = True
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
                
            login_user(user, remember=login.remember.data)
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

        return render_template('Update.html', form=update_signup_form)

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

if __name__ == "__main__":
    app.run(debug=True)
