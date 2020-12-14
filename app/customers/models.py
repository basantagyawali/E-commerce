from app import app, db, login_manager
from datetime import datetime
from flask_login import UserMixin
from app import bcrypt
import json

@login_manager.user_loader
def load_user(user_id):
    return CustomerUser.query.get(user_id)


class JsonEncodedDict(db.TypeDecorator):
    impl = db.Text

    def process_bind_param(self, value, dialect):
        if value is None:
            return '{}'
        else:
            return json.dumps(value)
    def process_result_value(self, value, dialect):
        if value is None:
            return {}
        else:
            return json.loads(value)

class CustomerUser(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=False)
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(200), unique=False)
    country = db.Column(db.String(50), unique=False)
    state = db.Column(db.String(50), unique=False)
    city = db.Column(db.String(50), unique=False)
    address = db.Column(db.String(50), unique=False)
    contact = db.Column(db.String(50), unique=False)
    zipcode = db.Column(db.String(50), unique=False)
    profile = db.Column(db.String(200), unique=False, default="profile.jpg")
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.now())

    customer_user = db.relationship('CustomerOrder', backref=db.backref('user', lazy=True))

    def __repr__(self):
        return '<USER %r>' % self.username

    def set_hash_password(self, password):
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

class CustomerOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoice = db.Column(db.String(50), unique=True, nullable=False)
    status = db.Column(db.String(50), default="Pending", nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    orders = db.Column(JsonEncodedDict)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer_user.id'), nullable=False)

    def __repr__(self):
        return '<CustomerOrder %r>' % self.invoice
