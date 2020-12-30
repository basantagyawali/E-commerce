from app import app, db, bcrypt
from flask import render_template, request, flash, redirect, url_for, session, make_response, abort 
from .forms import CustomerRegisterForm, CustomerLoginForm
from flask_login import logout_user, login_required, login_user, current_user
from ..products.models import Products, Brand, Category
from .models import CustomerUser, CustomerOrder
import secrets
import pdfkit
from . import bp

@bp.route('/register', methods=['POST', 'GET'])
def customerRegister():
    form = CustomerRegisterForm()
    if request.method == "POST" and form.validate_on_submit():
        user = CustomerUser(name= form.username.data, username=form.username.data, email=form.email.data,
                country=form.country.data,state=form.state.data,city=form.city.data,
                contact=form.contact.data, address=form.address.data, zipcode=form.zipcode.data)
        user.set_hash_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f"Welcome {form.username.data}  Thankyou for registering ", "success")
        return redirect(url_for('customers.customerLogin'))
    return render_template('customer/register.html', form=form, title="Customer Register")

@bp.route('/login', methods=['POST', 'GET'])
def customerLogin():
    form = CustomerLoginForm()
    if form.validate_on_submit():
        user = CustomerUser.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash("You are logged in successfully", "success")
            return redirect(url_for('index'))
        else:
            flash("Invalid Username and Password", "danger")
    return render_template('customer/login.html', title='Login', form=form)

@bp.route("/logout")
@login_required
def CustomerLogout():
    logout_user()
    flash("You are logged out successfully ", "success")
    return redirect(url_for('customers.customerLogin'))

@bp.route("/getOrder")
@login_required
def getOrder():
    if current_user.is_authenticated:
        customer_id= current_user.id
        invoice = secrets.token_hex(5)
        try:
            order = CustomerOrder(invoice=invoice, customer_id=customer_id, orders=session['Shoppingcart'])
            db.session.add(order)
            db.session.commit()
            session.pop('Shoppingcart')
            flash("Your order has been sent successfully", "success")
            return redirect(url_for('customers.orders', invoice=invoice))
        except Exception as e:
            print(e)
            flash("Something went wrong while getting order", "danger")
            abort(500)
    flash(u"Please first create your account", "danger")
    return redirect(url_for('customers.customerLogin'))

@bp.route("/orders/<invoice>")
@login_required
def orders(invoice):
    if current_user.is_authenticated:
        grandtotal = 0
        subtotal = 0
        customer_id = current_user.id
        customer = CustomerUser.query.filter_by(id=customer_id).first()
        orders = CustomerOrder.query.filter_by(customer_id=customer.id).order_by(CustomerOrder.id.desc()).first()
        for _key, product in orders.orders.items():
            discount = (product['discount']/1000) * float(product['price'])
            subtotal += float(product['price']) * int(product['quantity'])
            subtotal -= discount
            tax = ("%.2f" % (0.06 * float(subtotal)))
            grandtotal = float("%.2f" % (1.06 * subtotal ))
    else:
        return redirect(url_for('customers.customerLogin'))
    return render_template('customer/order.html', invoice=invoice, tax=tax, subtotal=subtotal, \
        grandtotal=grandtotal, customer=customer, orders=orders)

@bp.route("/getPDF/<invoice>", methods=['POST'])
@login_required
def getPDF(invoice):
    if current_user.is_authenticated:
        grandtotal = 0
        subtotal = 0
        customer_id = current_user.id
        if request.method == 'POST':
            customer = CustomerUser.query.filter_by(id=customer_id).first()
            orders = CustomerOrder.query.filter_by(customer_id=customer.id).order_by(CustomerOrder.id.desc()).first()
            for _key, product in orders.orders.items():
                discount = (product['discount']/1000) * float(product['price'])
                subtotal += float(product['price']) * int(product['quantity'])
                subtotal -= discount
                tax = ("%.2f" % (0.06 * float(subtotal)))
                grandtotal = float("%.2f" % (1.06 * subtotal ))
            rendered = render_template('customer/pdf.html', invoice=invoice, tax=tax, grandtotal=grandtotal, \
                    customer=customer, orders=orders)
            pdf = pdfkit.from_string(rendered, False)
            response = make_response(pdf)
            response.headers['content-Type'] ='application/pdf'
            response.headers['content-Disposition'] = 'inline; filename='+ invoice +'.pdf' #attached(means download ) in place of inline(shows)
            return response
    return request(url_for('customers.orders'))
