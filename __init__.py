from flask import Flask, render_template, request, redirect, url_for
from Forms import CreateVoucherForm
import shelve, Voucher
app = Flask(__name__)

@app.route('/')
def home():
    return render_template("admin.html")

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
    app.run()
