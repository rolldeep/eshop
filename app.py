from flask import Flask, render_template, session
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
        for meal in category.orders:
            items.append(meal)
        menu[category] = items

    cart = session.get("cart", [])
    # cart.append(item_id)

    return render_template('main.html', menu=menu)


@app.route('/cart/')
def show_cart():
    return render_template('cart.html')


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
    from data.importer import read_csv

    data = read_csv()

    for row in data['categories']:
        if row[1] != 'title':
            continue
        cat = Category(title=row[1])
        db.session.add(cat)
    db.session.commit()

    for row in data['items']:
        cat = db.session.query(Category).get(int(row[0]))
        item = Meal(title=row[1],
                    price=row[2],
                    description=row[3],
                    picture=row[4],
                    category=cat)
    db.session.commit()
    app.run(debug=True)
