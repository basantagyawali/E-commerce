from . import bp
from .forms import LoginForm
from .models import AdminUser
from app.products.models import Products, Brand, Category
from flask import render_template, redirect, url_for, session, request, flash
from functools import wraps
from app.customers.models import CustomerOrder, CustomerUser


def orders():
    return CustomerOrder.query.all()

def product():
    return Products.query.all()

def users():
    return CustomerUser.query.all()
    
def is_admin_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        # checking admin login or not
        if 'admin_logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('admin.admin_login'))
    return wrap

def not_admin_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'admin_logged_in' in session:
            return redirect(url_for('admin.home'))
        else:
            return f(*args, **kwargs)
    return wrap

def wrappers(func, *args, **kwargs):
    def wrapped():
        return func(*args, **kwargs)
    return wrapped

@bp.route('/admin_login', methods=['GET', 'POST'])
@not_admin_logged_in
def admin_login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        admin = AdminUser.query.filter_by(email=form.email.data).first()
        if admin is not None and admin.check_password(form.password.data) :
            session['admin_logged_in'] = True
            session['admin_uid'] = admin.id
            session['admin_name'] = admin.name
            flash(f"Welcome {admin.username} ! you have successfully logged in", "success")
            return redirect(url_for('admin.home'))
        flash(u"Invalid Username or Password", "danger")
        return redirect(url_for('admin.admin_login'))
    return render_template('admin/login.html', form=form, title="Admin Login")

@is_admin_logged_in
def admin():
    admin = AdminUser.query.filter_by(name=session['admin_name']).first()
    return admin

@bp.route('/admin_out', methods=['POST'])
@is_admin_logged_in
def admin_logout():
    if 'admin_logged_in' in session:
        session.clear()
        return redirect(url_for('index'))
    return redirect(url_for('index'))

@bp.route('/home')
@is_admin_logged_in
def home():
    return render_template('admin/index.html', title='Admin Page', products=product(), \
                admin=admin(), orders=orders(), users=users())

@bp.route('/brands')
@is_admin_logged_in
def brands():
    brand = Brand.query.order_by(Brand.id.desc()).all()
    return render_template('admin/brand.html', title='Admin Page', brands=brand, \
        admin=admin(), orders=orders(), users=users())

@bp.route('/category')
@is_admin_logged_in
def category():
    categories = Category.query.order_by(Category.id.desc()).all()
    return render_template('admin/brand.html', title='Admin Page', categories=categories, \
        admin=admin(), orders=orders(), users=users())

@bp.route('/checkOrders')
@is_admin_logged_in
def check_orders():
    return render_template('admin/orders.html', title='Admin Page', \
        admin=admin(), orders=orders(), users=users())

@bp.route('/users')
@is_admin_logged_in
def user():
    return render_template('admin/users.html', title='Admin Page', \
        admin=admin(), orders=orders(), users=users())
