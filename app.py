from typing import List

from flask import Flask, redirect, render_template, request, session
from flask_migrate import Migrate

from config import Config
from forms import LoginForm, OrderForm, RegisterForm
from models import Category, Meal, User, db

app = Flask(__name__)
db.init_app(app)
migrate = Migrate(app, db)
app.config.from_object(Config)


@app.route('/')
def main():
    menu = dict()
    categories = db.session.query(Category).all()

    for category in categories:
        items = list()
        for meal in category.meals:
            items.append(meal)
        menu[category.title] = items

    return render_template('main.html',
                           menu=menu,
                           is_auth=session.get("is_auth", False))


@app.route('/cart/', methods=['GET', 'POST'])
def show_cart():
    form = OrderForm()
    items = session.get("cart", [])
    is_removed = session.get("is_removed", False)
    is_auth = session.get("is_auth", False)
    session['is_removed'] = False
    order = list()
    order_summ = 0
    meals = [db.session.
             query(Meal).
             get(int(item))
             for item in items]
    for meal in meals:
        d = {'title': meal.title,
             'price': meal.price,
             'meal_id': meal.id
             }
        order.append(d)
        order_summ += meal.price
    if request.method == 'GET':
        return render_template('cart.html',
                               meals_ids=items,
                               meals=order,
                               order_summ=order_summ,
                               form=form,
                               is_removed=is_removed,
                               is_auth=is_auth)
    if request.method == 'POST':
        if form.validate_on_submit():
            session['email'] = form.email.data
            session['name'] = form.name.data
            session['address'] = form.address.data
            session['phone'] = form.phone.data
            user = User.query.filter_by(email=session['email']).first()
            if user:
                return redirect('/auth/')
            else:
                return redirect('/register/')
        else:
            return render_template('cart.html',
                                   meals_ids=items,
                                   meals=order,
                                   order_summ=order_summ,
                                   form=form,
                                   is_removed=is_removed,
                                   is_auth=is_auth)


@app.route('/addtocart/<item_id>')
def add_item(item_id):
    cart = session.get("cart", [])
    cart.append(item_id)
    session["cart"] = cart
    return redirect('/cart/')


@app.route('/removeitem/<item_id>')
def remove_item(item_id):
    cart = session.get("cart", [])
    is_removed = session.get("is_removed", True)
    cart.remove(item_id)
    session["cart"] = cart
    session["is_removed"] = True
    return redirect('/cart/')


@app.route('/account/', methods=['GET', 'POST'])
def show_account():
    if session.get('name'):
        user = User.query.filter_by(email=session['email'])
        user.name = session['name']
        user.address = session['address']
        user.phone = session['phone']
        db.session.commit()
    return render_template('account.html',
                           is_auth=session.get("is_auth", False))


@app.route('/ordered/')
def on_success():
    return render_template('ordered.html')


@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    is_correct = True

    if session.get("is_auth"):
        return redirect('/account/')

    elif request.method == 'POST':
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.password_valid(form.password.data):
            session["user_id"] = user.id
            session["email"] = user.email
            session["is_auth"] = True
            return redirect('/account/')

        else:
            is_correct = False
    return render_template('login.html',
                           form=form,
                           is_auth=False,
                           is_correct=is_correct)


@app.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            # Reieving data
            password = form.password.data
            email = form.email.data

            # Resistering
            user = User(email=email)
            user.password = password
            db.session.add(user)
            db.session.commit()

            # Authorizing
            session["email"] = email
            session["is_auth"] = True
            return redirect('/account/')
    return render_template('register.html', form=form)


@app.route('/logout/')
def logout():
    session.clear()
    return redirect('/login/')


if __name__ == "__main__":
    app.run(debug=True)
