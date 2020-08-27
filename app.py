from datetime import datetime
from typing import List, Any, Dict

from flask import Flask, redirect, render_template, request, session
from flask_migrate import Migrate

from config import Config
from forms import LoginForm, OrderForm, RegisterForm
from models import Category, Meal, User, db, Order

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
    
    # show message if item is removed
    session['is_removed'] = False
    
    # Orders to show
    order: List[dict] = []
    order_sum = 0
    
    # Getting the meals from db
    meals = [db.session.
                    query(Meal).
                    get(int(item))
                    for item in items]
    for meal in meals:
        meals_ids = session.get("meals_ids", [])
        d = {'title': meal.title,
                'price': meal.price,
                'meal_id': meal.id
                }
        meals_ids.append(meal.id)
        session["meals_ids"] = meals_ids
        order.append(d)
        order_sum += meal.price

    if request.method == 'GET':
        session['order_sum'] = order_sum
        return render_template('cart.html',
                               meals_ids=items,
                               meals=order,
                               order_sum=order_sum,
                               form=form,
                               is_removed=is_removed,
                               is_auth=is_auth)

    if request.method == 'POST':
        if form.validate_on_submit():
            session['email'] = form.email.data
            session['name'] = form.name.data
            session['address'] = form.address.data
            session['phone'] = form.phone.data
            session['order_sum'] = request.form['order_sum']
            user = User.query.filter_by(email=session['email']).first()
            if user:
                return redirect('/login/')
            else:
                return redirect('/register/')
        else:
            return render_template('cart.html',
                                   meals_ids=items,
                                   meals=order,
                                   order_sum=order_sum,
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
        user = User.query.filter_by(email=session['email']).first()
        user.name = session['name']
        user.address = session['address']
        user.phone = session['phone']
        meals_ids: List[str] = session.get("meals_ids", [])
        
        order_date: datetime = datetime.now()      
        order = Order(order_date=order_date,
                      order_sum=session['order_sum'],
                      user_id=user.id)
        
        meals_ids_set = meals_ids
        # Forming the order list
        for meal_id in meals_ids_set:    
            order.meals.append(
                Meal.query.get(
                    int(meal_id)
                    )
                )
                 
        # Adding the order
        user.orders.append(order)
                      
        # db.session.add(order)
        db.session.commit()
        
        # Removing session name for preventing writing 
        # order twice
        session.pop('name')

    orders_list: List[Dict[str, Any]] = []
    orders = Order.query.all()
    for o in orders:
        meals_list: List[Dict[str, Any]] = [
            {
                'title': meal.title,
                'price': meal.price,
            }
            for meal in o.meals
        ]
        order_item: Dict[str, Any] = {
            'order_date': o.order_date.strftime('%Y-%m-%d'),
            'order_sum': o.order_sum,
            'meals': meals_list,
        }
        orders_list.append(order_item)
    return render_template('account.html',
                           is_auth=session.get("is_auth", False),
                           order_sum=session.get("order_sum", 0),
                           orders=orders_list)


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
            # Recieving data
            password = form.password.data
            email = form.email.data

            # Registering user
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
