from . import bp
from .. import db, photos
from flask import render_template, redirect, url_for, request, flash, current_app
from .models import Brand, Category, Products
from .forms import BrandForm, CategoryForm, AddProductsForm
import secrets, os
from app.admin.routes import admin, orders, users
from app.routes import categories, brands

def checkCategoryInProducts(category):
    for cate in categories():
        if category.name == cate.name:
            return False
        else:
            return True

def checkBrandInProducts(brand):
    for bran in brands():
        if brand.name == bran.name:
            return False
        else:
            return True

@bp.route('/addBrand', methods=['POST', 'GET'])
def addBrand():
    form = BrandForm()
    if request.method == 'POST' and form.validate_on_submit():
        brand = Brand(name=form.name.data)
        db.session.add(brand)
        db.session.commit()
        flash(f"The brand {form.name.data} was added to your database", 'success')
        return redirect(url_for('products.addBrand'))
    return render_template('products/addBrand.html', brands='brands', form=form, \
               admin=admin(), orders=orders(), users=users())

@bp.route('/editBrand/<int:id>', methods=['POST', 'GET'])
def editBrand(id):
    brand = Brand.query.get_or_404(id)
    form = BrandForm()
    if request.method == 'POST' and form.validate_on_submit():
        brand.name = form.name.data
        db.session.commit()
        flash(f"The brand has been updated", 'success')
        return redirect(url_for('products.addBrand'))
    form.name.data = brand.name
    return render_template('products/editBrand.html', brands='brands', form=form, title="Edit Brand", \
            admin=admin(), orders=orders(), users=users())


@bp.route('/deleteBrand/<int:id>', methods=['POST'])
def deleteBrand(id):
    brand = Brand.query.get_or_404(id)
    if brand is not None and request.method == 'POST' and checkBrandInProducts(brand) :
        db.session.delete(brand)
        db.session.commit()
        flash(f"The brand {brand.name} has been deleted successfully", 'success')
        return redirect(url_for('admin.brands'))
    flash(f"The brand {brand.name} can't be deleted ", 'warning')
    return redirect(url_for('admin.home'))

@bp.route('/addCategory', methods=['POST', 'GET'])
def addCategory():
    form = CategoryForm()
    if request.method == 'POST' and form.validate_on_submit():
        category = Category(name=form.name.data)
        db.session.add(category)
        db.session.commit()
        flash(f"The category {form.name.data} was added to your database", 'success')
        return redirect(url_for('products.addCategory'))
    return render_template('products/addBrand.html', form=form, admin=admin(), \
            orders=orders(), users=users())

@bp.route('/editCategory/<int:id>', methods=['POST', 'GET'])
def editCategory(id):
    category = Category.query.get_or_404(id)
    form = CategoryForm()
    if request.method == 'POST' and form.validate_on_submit():
        category.name = form.name.data
        db.session.commit()
        flash(f"The category has been updated", 'success')
        return redirect(url_for('products.addCategory'))
    form.name.data = category.name
    return render_template('products/editBrand.html', form=form, title="Edit Category", \
            admin=admin(), orders=orders(), users=users())



@bp.route('/deleteCategory/<int:id>', methods=['POST'])
def deleteCategory(id):
    category = Category.query.get(id)
    if category is not None and request.method == 'POST' and checkCategoryInProducts(category) :
        db.session.delete(category)
        db.session.commit()
        flash(f"The category {category.name} has been deleted successfully", 'success')
        return redirect(url_for('admin.category'))
    flash(f"The category {category.name} can't be deleted ", 'warning')
    return redirect(url_for('admin.home'))

@bp.route('/addProducts', methods=['POST', 'GET'])
def addProducts():
    form = AddProductsForm()
    brands = Brand.query.all()
    categories = Category.query.all()
    if request.method == 'POST' and form.validate_on_submit():
        name = form.name.data
        price = form.price.data
        stock = form.stock.data
        discount = form.discount.data
        description = form.description.data
        colors = form.colors.data
        brand = request.form.get('brand')
        category = request.form.get('category')
        image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + '.')
        image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + '.')
        image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + '.')
        product = Products(name=name, price=price,stock=stock,discount=discount,
                description=description,colors=colors,brand_id=brand,category_id=category,
                image_1=image_1,image_2=image_2,image_3=image_3 )

        db.session.add(product)
        db.session.commit()
        flash(f"The product {name} was added to your database", 'success')
        return redirect(url_for('products.addProducts'))
    return render_template('products/addProducts.html', form=form, title="Add Product", \
        brands=brands, categories=categories, admin=admin(), orders=orders(), users=users())

@bp.route('/editProduct/<int:id>', methods=['POST', 'GET'])
def editProduct(id):
    products = Products.query.get(id)
    form = AddProductsForm()
    brands = Brand.query.all()
    categories = Category.query.all()
    if request.method == 'POST' and form.validate_on_submit():
        products.name = form.name.data
        products.price = form.price.data
        products.stock = form.stock.data
        products.discount = form.discount.data
        products.description = form.description.data
        products.colors = form.colors.data
        products.brand_id = request.form.get('brand')
        products.category_id = request.form.get('category')
        if request.files.get('image_1'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" + products.image_1))
                products.image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + '.')
            except:
                products.image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + '.')

        if request.files.get('image_2'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" + products.image_2))
                products.image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + '.')
            except:
                products.image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + '.')

        if request.files.get('image_3'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" + products.image_3))
                products.image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + '.')
            except:
                products.image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + '.')

        db.session.commit()
        flash(f"The product  was edited ", 'success')
        return redirect(url_for('admin.home'))
    form.name.data = products.name
    form.price.data = products.price
    form.stock.data = products.stock
    form.discount.data = products.discount
    form.description.data = products.description
    form.colors.data = products.colors

    return render_template('products/editProducts.html', form=form, title="Edit Products", \
        brands=brands, categories=categories, product=products, admin=admin(), orders=orders(), users=users())

@bp.route('/deleteProduct/<int:id>', methods=['POST'])
def deleteProduct(id):
    product = Products.query.get_or_404(id)
    if product is not None and request.method == 'POST':
        try:
            os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_1))
            os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_2))
            os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_3))
        except Exception as e:
            print(e)
        db.session.delete(product)
        db.session.commit()
        flash(f"The product {product.name} has been deleted successfully", 'success')
        return redirect(url_for('admin.admin'))
    flash(f"The product {product.name} can't be deleted ", 'warning')
    return redirect(url_for('admin.home'))
