from flask import redirect, url_for, render_template, session, request, current_app, flash
from .. import app, db
from ..products.models import Products, Brand, Category
from ..routes import brands, categories
from . import bp

def MagerDicts(dict1, dict2):
    if isinstance(dict1, list) and isinstance(dict2, list):
        return dict1+dict2
    elif isinstance(dict1, dict) and isinstance(dict2, dict):
        return dict(list(dict1.items()) + list(dict2.items()))
    return False

@bp.route('/addCart', methods=['POST'])
def addCart():
    try:
        product_id = request.form.get('product_id')
        quantity = request.form.get('quantity')
        color = request.form.get('colors')
        product = Products.query.filter_by(id=product_id).first()
        if product_id and quantity and color and request.method == "POST":
            DictItems = {product_id: {'name': product.name, 'price': str(product.price), 'discount': product.discount,
            'color': color, 'quantity': quantity, 'image': product.image_1,
            'colors': product.colors}}
            if 'Shoppingcart' in session:
                print(session['Shoppingcart'])
                if product_id in session['Shoppingcart']:
                    for key, item in session['Shoppingcart'].items():
                        if int(key) == int(product_id):
                            session.modified = True
                            item['quantity'] = int(item['quantity']) + 1
                else:
                    session['Shoppingcart'] = MagerDicts(session['Shoppingcart'], DictItems)
                    return redirect(request.referrer)
            else:
                session['Shoppingcart'] = DictItems
                return redirect(request.referrer)
    except Exception as e:
        print(e)
    finally:
        return redirect(request.referrer)

@bp.route('/carts')
def getCarts():
    if 'Shoppingcart' not in session or len(session['Shoppingcart']) <=0:
        return redirect(url_for('index'))
    subtotal = 0
    grandtotal = 0
    tax = 0
    for key, product in session['Shoppingcart'].items():
        discount = (product['discount']/1000) * float(product['price'])
        subtotal += float(product['price']) * int(product['quantity'])
        subtotal -= discount
        tax = ("%.2f" % (0.06 * float(subtotal)))
        grandtotal = float("%.2f" % (1.06 * subtotal ))
    return render_template('products/carts.html', tax=tax, grandtotal=grandtotal,
                    brands=brands(), categories=categories())

@bp.route('/updateCart/<int:id>', methods=['POST', 'GET'])
def updateCart(id):
    if 'Shoppingcart' not in session and len(session['Shoppingcart']) <=0:
        return redirect(url_for('index'))
    if request.method == "POST":
        quantity = request.form.get('quantity')
        color = request.form.get('color')
        print(color)
        try:
            session.modified = True
            for key, item in session['Shoppingcart'].items():
                if int(key) == id :
                    item['quantity'] = quantity
                    item['color'] = color
                    flash(u"Item updated successfully", "success")
                    return redirect(url_for('carts.getCarts'))
        except Exception as e:
            print(e)
            return redirect(url_for('getCarts'))

@bp.route('/deleteCart/<int:id>', methods=['POST', 'GET'])
def deleteCart(id):
    if 'Shoppingcart' not in session and len(session['Shoppingcart']) <=0:
        return redirect(url_for('index'))
    try:
        session.modified = True
        for key, item in session['Shoppingcart'].items():
            if int(key) == id :
                session['Shoppingcart'].pop(key, None)
                flash(u"Item deleted successfully", "success")
                return redirect(url_for('carts.getCarts'))
    except Exception as e:
        print(e)
        return redirect(url_for('carts.getCarts'))

@bp.route('/clearCart')
def clearCart():
    try:
        session.pop('Shoppingcart', None)
        return redirect(url_for('index'))
    except Exception as e:
        print(e)
