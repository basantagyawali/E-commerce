from app import app, db, login_manager
from datetime import datetime
from flask_login import UserMixin
from app import bcrypt
import json


class AdminUser(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=False)
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(200), unique=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.now())

    def __repr__(self):
        return '<AdminUser %r>' % self.username

    def set_hash_password(self, password):
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)
