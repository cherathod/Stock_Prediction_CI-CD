from datetime import datetime

from flask import app
from app.db import db 

class RegisteredUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    registered_on = db.Column(db.DateTime, default=datetime.utcnow)
    name = db.Column(db.String(100), nullable=True)
    first_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=True)
    phone_number = db.Column(db.String(15), nullable=True)
    address = db.Column(db.String(255), nullable=True)
    date_of_birth = db.Column(db.Date, nullable=True)
    is_active = db.Column(db.Boolean, default=True)


class LoginAttempt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), nullable=False)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    symbol = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default="Pending")
    date = db.Column(db.DateTime, default=datetime.utcnow)

class StockData(db.Model):
    __tablename__ = 'stock_data'

    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    open_price = db.Column(db.Float, nullable=False)
    change = db.Column(db.Float)
    percent_change = db.Column(db.Float)

    def __repr__(self):
        return f'<StockData {self.symbol}>'
