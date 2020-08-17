from flask_sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash

db = SQLAlchemy()

orders_meals = db.Table(
    'orders_meals',
    db.Column('order_id',
              db.Integer,
              db.ForeignKey('meals.id'),
              primary_key=True),
    db.Column('meal_id',
              db.Integer,
              db.ForeignKey('orders.id'),
              primary_key=True)
)


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    password_hash = db.Column(db.String(1000), nullable=False)
    address = db.Column(db.String(1000), nullable=False)

    orders = db.relationship('Order')

    @property
    def password(self):
        raise AttributeError("Неьзя возвращать пароль")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def password_valid(self, password):
        return check_password_hash(self.password_hash, password)

class Meal(db.Model):
    __tablename__ = 'meals'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255), nullable=False)
    picture = db.Column(db.String(255), nullable=False)
    
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)
    category = db.relationship('Category')
    
    orders = db.relationship('Order',
                             secondary=orders_meals,
                             back_populates='meals'
                             )


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)

    meals = db.relationship('Meal')


class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    order_date = db.Column(db.DateTime, nullable=False)
    order_sum = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(255), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User')
    meals = db.relationship('Meal',
                            secondary=orders_meals,
                            back_populates='orders'
                            )
