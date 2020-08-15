from typing import List
from flask import Flask, render_template, session, redirect
from flask_migrate import Migrate
from models import Category, db, Meal
from config import Config

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

    return render_template('main.html', menu=menu)


@app.route('/cart/')
def show_cart():
    items = session.get("cart", [])
    order_summ = 0
    order = list()
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
    return render_template('cart.html',
                           meals=order,
                           order_summ=order_summ)


@app.route('/addtocart/<item_id>')
def add_item(item_id):
    cart = session.get("cart", [])
    cart.append(item_id)
    session["cart"] = cart
    return redirect('/')


@app.route('/removeitem/<item_id>')
def remove_item(item_id):
    cart = session.get("cart", [])
    cart.remove(item_id)
    session["cart"] = cart
    return redirect('/cart/')


@app.route('/account/')
def show_account():
    return render_template('account.html')


@app.route('/login/')
def login():
    return render_template('login.html')


@app.route('/logout/')
def logout():
    return render_template('login.html')


if __name__ == "__main__":
    app.run(debug=True)
