from app import app
from flask import render_template, request
from .products.models import Products, Brand, Category


def brands():
    brands = Brand.query.join(Products, (Brand.id == Products.brand_id)).all()
    return brands

def categories():
    categories = Category.query.join(Products, (Category.id == Products.category_id)).all()
    return categories

@app.route('/')
@app.route('/index')
def index():
    page = request.args.get('page', 1, type=int)
    products = Products.query.filter(Products.stock>0).order_by(Products.id.desc()).paginate(page=page, per_page=4)
    return render_template('index.html', products=products, brands=brands(), categories=categories())

@app.route('/product/<int:id>')
def single_page(id):
    product = Products.query.filter_by(id=id).first_or_404()
    return render_template('products/single_page.html', product=product, brands=brands(), categories=categories())

@app.route('/brand/<int:id>')
def get_brand(id):
    page = request.args.get('page', 1, type=int)
    get_bran = Category.query.filter_by(id=id).first_or_404()
    brand = Products.query.filter_by(brand=get_bran).paginate(page=page, per_page=4)
    return render_template('index.html', brand=brand, brands=brands(), categories=categories(), get_bran=get_bran)

@app.route('/category/<int:id>')
def get_category(id):
    page = request.args.get('page', 1, type=int)
    get_cat = Category.query.filter_by(id=id).first_or_404()
    category = Products.query.filter_by(category=get_cat).paginate(page=page, per_page=4)
    return render_template('index.html', category=category, categories=categories(), brands=brands(), get_cat=get_cat)
