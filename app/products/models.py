from .. import db
from datetime import datetime


class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    stock = db.Column(db.Integer)
    discount = db.Column(db.Integer, default=0)
    description = db.Column(db.Text, nullable=False)
    colors = db.Column(db.Text, nullable=False)

    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category', backref=db.backref('category', lazy=True))

    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'), nullable=False)
    brand = db.relationship('Brand', backref=db.backref('brand', lazy=True))

    image_1 = db.Column(db.String(150), nullable=False, default='image.jpg')
    image_2 = db.Column(db.String(150), nullable=False, default='image.jpg')
    image_3 = db.Column(db.String(150), nullable=False, default='image.jpg')

    def __repr__(self):
        return '<Products %r>' % self.name

class Brand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False, unique=True)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False, unique=True)
