from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
def now_utc():
    return datetime.now(timezone.utc)

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

    expenses = db.relationship('Expense', backref='user', lazy=True)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    expenses = db.relationship('Expense', backref='category', lazy=True)


class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    amount = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=now_utc)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
