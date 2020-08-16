from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, Email


class OrderForm(FlaskForm):
    name = StringField('Ваше имя',
                       [InputRequired(message='Как вас зовут?'),
                        Length(min=1,
                               max=30,
                               message='Это точно ваше имя?')])
    address = StringField('Адрес',
                          [InputRequired(message='Введите адрес.')])
    email = StringField('Элекстронная почта',
                        [Email(message='Введите валидный адрес'),
                         InputRequired(message='Обязательное поле.')])
    phone = StringField('Телефон',
                        [InputRequired(message='Обязательное поле.'),
                         Length(min=6,
                                max=12,
                                message='Невалидный номер')])


class AuthForm(FlaskForm):
    email = StringField('Элекстронная почта',
                        [Email(message='Введите валидный адрес'),
                         InputRequired(message='Обязательное поле.')])
    password = PasswordField('Пароль',
                             [InputRequired(name='Введите Пароль')])
