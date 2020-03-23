from flask import Flask
from foodapp.config import Config
# from foodapp.models import db
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object(Config)
db=SQLAlchemy(app)

migrate=Migrate(app, db)
from foodapp.models import Order, Category, User, Meal, meals_orders_association

with app.app_context():
    db.create_all()

from foodapp.views import *

