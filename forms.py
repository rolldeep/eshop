import re

from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField
from wtforms.validators import Email, InputRequired, Length, ValidationError


def password_check(form, field):
    msg = 'Пароль должен содержать латинские буквы в верхнем и нижнем регистре и цифры.'
    pattern1 = re.compile('[a-zA-Z]+')
    pattern2 = re.compile('\\d+')
    if (not pattern1.search(field.data) or
            not pattern2.search(field.data)):
        raise ValidationError(msg)


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


class LoginForm(FlaskForm):
    email = StringField('Элекстронная почта',
                        [Email(message='Введите валидный адрес'),
                         InputRequired(message='Обязательное поле.')])
    password = PasswordField('Пароль',
                             [InputRequired(message='Введите Пароль'),
                              Length(min=8,
                                     message="Пароль должен быть не менее 8 символов")])


class RegisterForm(FlaskForm):
    email = StringField('Элекстронная почта',
                        [Email(message='Введите валидный адрес'),
                         InputRequired(message='Обязательное поле.')])
    password = PasswordField('Пароль',
                             [InputRequired(message='Введите Пароль'),
                              Length(min=8,
                                     message="Пароль должен быть не менее 8 символов"),
                              password_check])
