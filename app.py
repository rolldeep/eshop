from typing import List
from flask import Flask, render_template, session, redirect, request
from flask_migrate import Migrate
from models import Category, db, Meal, User
from config import Config
from forms import OrderForm, AuthForm, RegisterForm

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


@app.route('/cart/', methods=['GET', 'POST'])
def show_cart():
    form = OrderForm()
    items = session.get("cart", [])
    is_removed = session.get("is_removed", False)
    is_logged = session.get("is_logged", False)
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
                               is_logged=is_logged)
    if request.method == 'POST':
        if form.validate_on_submit():
            return redirect('/ordered/')
        else:
            return render_template('cart.html',
                                   meals_ids=items,
                                   meals=order,
                                   order_summ=order_summ,
                                   form=form,
                                   is_removed=is_removed,
                                   is_logged=is_logged)


@app.route('/addtocart/<item_id>')
def add_item(item_id):
    cart = session.get("cart", [])
    cart.append(item_id)
    session["cart"] = cart
    return redirect('/')


@app.route('/removeitem/<item_id>')
def remove_item(item_id):
    cart = session.get("cart", [])
    is_removed = session.get("is_removed", True)
    cart.remove(item_id)
    session["cart"] = cart
    session["is_removed"] = True
    return redirect('/cart/')


@app.route('/auth/', methods=['GET', 'POST'])
def auth():
    form = AuthForm()
    is_correct = False
    if request.method == 'GET':
        return render_template('auth.html',
                               form=form,
                               is_correct=is_correct)
    elif request.method == 'POST':
        user = User.query.filter_by(email=form.email).first()
        if user and user.password_valid(form.password):
            session["user_id"] = user.id
            session["email"] = user.email
            return redirect('/account/')
        else:
            is_correct = False
            return render_template('auth.html',
                                   form=form,
                                   is_correct=is_correct)


@app.route('/account/', methods=['GET', 'POST'])
def show_account():
    return render_template('account.html')


@app.route('/ordered/')
def on_success():
    return render_template('ordered.html')


@app.route('/login/')
def login():
    return render_template('login.html')


@app.route('/logout/')
def logout():
    return render_template('login.html')


@app.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'GET':
        return render_template('register.html', form=form)
    elif request.method == 'POST':
        if form.validate_on_submit():
            password = form.password.data
            email = form.email.data
            user = User(email=email)
            user.password = password
            db.session.add(user)
            db.session.commit()
            session["email"] = email
            return redirect('/account/')


if __name__ == "__main__":
    app.run(debug=True)
