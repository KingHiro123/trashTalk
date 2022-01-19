from flask import Flask, render_template, url_for, redirect, request, flash
from flask_rbac import RBAC
from Forms import Signup_Form, Login_Form
import shelve, signUp, Login


app = Flask(__name__)

app.config['SECRET_KEY'] = 'bananaisagoodfruit'
#Home
@app.route("/")
def home():
    return render_template("Home_Admin.html")

#Log in
@app.route('/login', methods=['GET','POST'])
def login():
    login = Login_Form(request.form)
    if request.method == "POST" and login.validate():
        users_dict = {}
        db = shelve.open('sign_up.db', 'w')
        
        try:
            users_dict = db['signUp']
        except IOError:
            print("Error, trying to read")

        username = request.form.get('username')
        password = request.form.get('password')

        for key in users_dict:
            user = users_dict[key]
            
            if login.username.data == user.get_username() and login.password.data == user.get_password():
                flash('You have successfully logged in!')
                db['signUp'] = users_dict
                db.close()
                return redirect(url_for('home'))
            elif login.username.data != user.get_username() or login.password.data != user.get_password():
                flash('Invalid username or password! Please check your login details and try again.')
                db['signUp'] = users_dict
                db.close()
                return redirect(url_for('login'))

    
    return render_template('Login.html', form=login)

#Sign up
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    Signup = Signup_Form(request.form)
    if request.method == 'POST' and Signup.validate():
        signup_dict = {}
        db = shelve.open('sign_up.db', 'c')
        try:
            signup_dict = db['signUp']
        except:
            print("Error in retrieving Users from sign_up.db")

        sign_up = signUp.Signup(Signup.username.data, Signup.email.data, Signup.password.data, Signup.confirmpass.data)
        signup_dict[sign_up.get_user_id()] = sign_up
        db['signUp'] = signup_dict

        for key in signup_dict:
            signin = signup_dict[key]
        
            if Signup.username.data == signin.get_username():
                flash('This username has already been used.')
                db.close()

                return redirect(url_for('signup'))
            elif Signup.email.data == signin.get_email():
                flash('This email has already been used.')
                db.close()

                return redirect(url_for('signup'))
            else:
                flash(f'Account created for {Signup.username.data}!', 'success')
                db['signUp'] = signup_dict
                db.close()

            return redirect(url_for('acc_list'))
    return render_template('signUp.html', form=Signup)

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
