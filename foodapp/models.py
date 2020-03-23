from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import requests
import json
from ast import literal_eval as le
from foodapp import db


# db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    mail = db.Column(db.String(55), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    address = db.Column(db.String(100))
    orders = db.relationship("Order", back_populates="user")


meals_orders_association = db.Table(
    "meals_orders",
    db.Column("meal_id", db.Integer, db.ForeignKey("meals.id")),
    db.Column("order_id", db.Integer, db.ForeignKey("orders.id"))
)


class Meal(db.Model):
    __tablename__ = 'meals'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(), nullable=False)
    picture = db.Column(db.String(), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"))
    category = db.relationship("Category", back_populates="meals")
    orders = db.relationship("Order", secondary=meals_orders_association, back_populates="meals")


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(32), nullable=False)
    meals = db.relationship("Meal", back_populates="category")


class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    summ = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String, nullable=False)
    meals = db.relationship("Meal", secondary=meals_orders_association, back_populates="orders")
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("User", back_populates="orders")




# @property
# def password(self):
#     raise AttributeError("Вам не нужно знать пароль!")
#
# @password.setter
# def password(self, password):
#     self.password_hash = generate_password_hash(password)
#
# def password_valid(self, password):
#     return check_password_hash(self.password_hash, password)
