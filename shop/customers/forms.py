from wtforms import StringField, TextAreaField, PasswordField, SubmitField, validators, ValidationError
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired, FileField
from .models import CustomerUser
from flask import flash


class CustomerRegisterForm(FlaskForm):
    name = StringField(validators=[validators.Length(min=4, max=25), validators.DataRequired()])
    username = StringField('Никнейм', [validators.Length(min=4, max=25), validators.DataRequired()])
    email = StringField('Эл. Почта', [validators.DataRequired(), validators.Email(message='Неверный адрес эл. почты')])
    password = PasswordField('Пароль', [validators.DataRequired(),
                                        validators.EqualTo('confirm', message='Пароли должны совпадать')])
    confirm = PasswordField('Повторите пароль', [validators.DataRequired()])
    # city = StringField('Город', [validators.DataRequired()])
    city = 'Новосибирск'
    profile = FileField('Фото', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'gif'], message='Image only please')])
    submit = SubmitField('Зарегистрироваться')

    def validate_username(self, username):
        if CustomerUser.query.filter_by(username=username.data).first():
            raise ValidationError('Пользователь с таким никнеймом уже существует')

    def validate_email(self, email):
        if CustomerUser.query.filter_by(email=email.data).first():
            raise ValidationError('Этот электронный адрес уже используется!')


class CustomerLoginForm(FlaskForm):
    email = StringField('Эл. Почта', [validators.DataRequired(), validators.Email(message='Неверный email адрес')])
    password = PasswordField('Пароль', [validators.DataRequired()])
    submit_btn = SubmitField('Войти')
