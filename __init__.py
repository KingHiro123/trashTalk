from flask import Flask, render_template, url_for, redirect, request
from Forms import Signup_Form, Login_Form
import shelve, signUp, Login


app = Flask(__name__)

@app.route("/")
def home():
    return render_template("Home_Admin.html")

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

        #test code
        signup_dict = db['signUp']
        signup = signup_dict[sign_up.get_user_id()]
        print(signup.get_username(), "was stored in user.db successfully with user_id ==",
              signup.get_user_id())

        db.close()

        return redirect(url_for('home'))
    return render_template('signUp.html', form=Signup)

#@app.route('/login', methods=['GET', 'POST'])
#def login():
#    Login = Login_Form(request.form)
#    if request.method == 'POST' and Login.validate():
#        if Login.username.data == 'signup.db' and Login.password.data == 'signup.db':

#    return render_template('Login.html', form=Login)

@app.route('/account')
def acc_list():
    signup_dict = {}
    db = shelve.open('sign_up.db', 'r')
    signup_dict = db['signUp']
    db.close()

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
    app.run()

