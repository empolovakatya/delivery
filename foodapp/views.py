from functools import wraps
import requests
import json
from flask import abort, flash, session, redirect, request, render_template

from foodapp import app, db
from foodapp.models import User, Meal, Order, Category
from foodapp.forms import LoginForm, RegistrationForm


# ------------------------------------------------------
# Декораторы авторизации
# def login_required(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         print("login_required")
#         if not session.get('user'):
#             return redirect('/login')
#         return f(*args, **kwargs)
#     return decorated_function
#
# def admin_only(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         print("admin_only")
#         if session.get('user')["role"] != "admin":
#             abort(403, description="Вам сюда нельзя")
#         return f(*args, **kwargs)
#     return decorated_function

# ------------------------------------------------------
# # Страница админки
# @foodapp.route('/')
# @login_required
# def home():
#     return render_template("page_admin.html")

@app.route('/')
# @login_required
def home():
    return render_template("main.html")


@app.route('/cart/')
# @login_required ?
def cart():
    return render_template("cart.html")


@app.route('/account/')
# @login_required ?
def account():
    return render_template("account.html")


# ------------------------------------------------------
# Страница аутентификации
@app.route("/login/", methods=["GET", "POST"])
def login():
    if session.get("user"):
        return redirect("/")

    form = LoginForm()

    if request.method == "POST":
        if not form.validate_on_submit():
            return render_template("login.html", form=form)

        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password_valid(form.password.data):
            session["user"] = {
                "id": user.id,
                "username": user.username,
                "role": user.role,
            }
            return redirect("/")

        form.username.errors.append("Не верное имя или пароль")

    return render_template("login.html", form=form)


# ------------------------------------------------------
# Страница выхода из админки
@app.route('/logout/', methods=["POST"])
# @login_required
def logout():
    session.pop("user")
    return redirect("/login/")


# ------------------------------------------------------
# Страница добавления пользователя
@app.route("/register/", methods=["GET", "POST"])
# @admin_only
# @login_required
def registration():
    form = RegistrationForm()

    if request.method == "POST":
        if not form.validate_on_submit():
            return render_template("register.html", form=form)

        user = User.query.filter_by(username=form.username.data).first()
        if user:
            form.username.errors.append("Пользователь с таким именем уже существует")
            return render_template("register.html", form=form)

        user = User()
        user.username = form.username.data
        user.password = form.password.data
        user.role = "user"
        db.session.add(user)
        db.session.commit()

        flash(f"Пользователь: {form.username.data} с паролем: {form.password.data} зарегистрирован")
        return redirect("/register/")

    return render_template("register.html", form=form)


# ------------------------------------------------------
@app.route('/ordered/')
# @login_required
def ordered():
    return render_template("ordered.html")


# res = requests.get('https://sheetdb.io/api/v1/459o1nx4znd0i')
# data = json.loads(res.text)
# list_meals=json.loads(data.json)
# print(list_meals)
# with open('data.json', 'r', encoding='utf-8') as filejs:
#     contents = json.load(filejs)
# with app.app_context():
#     for item in data:
#         meal = Meal(title=str(item['title']),
#                     price=int(item['price']),
#                     description=str(item['description']),
#                     picture=str(item['picture']),
#                     category_id=int(item['category_id']))
#         db.session.add(meal)
#     db.session.commit()
#
# print(db.session.query(Meal.id).all())