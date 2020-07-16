from sqlalchemy.sql import func
from src import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer,  primary_key=True, autoincrement=True,
                   unique=True)
    username = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
