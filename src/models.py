from sqlalchemy.sql import func
from src import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer,  primary_key=True, autoincrement=True,
                   unique=True)
    username = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)


class Investment(db.Model):
    __tablename__ = "investments"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True,
                   unique=True)
    stock_name = db.Column(db.String(255), nullable=False)
    usd_value = db.Column(db.Float, nullable=False)
    bitcoin_value = db.Column(db.Float)
    is_bitcoin = db.Column(db.Boolean, nullable=False)


class UserInvestment(db.Model):
    __tablename__ = "user_investments"

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    investment_id = db.Column(db.Integer, db.ForeignKey('investments.id'))
    usd_value = db.Column(db.Float, nullable=False)
    id = db.Column(db.Integer, primary_key=True, autoincrement=True,
                   unique=True)
