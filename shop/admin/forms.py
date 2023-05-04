from wtforms import Form, BooleanField, StringField, PasswordField, validators


class RegistrationForm(Form):
    name = StringField('Имя', [validators.Length(min=4, max=25)])
    username = StringField('Никнейм', [validators.Length(min=4, max=25)])
    email = StringField('Эл. почта', [validators.Length(min=6, max=35), validators.Email()])
    password = PasswordField('Пароль', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Повторите пароль')


class LoginForm(Form):
    email = StringField('Эл. почта', [validators.Length(min=6, max=35), validators.Email()])
    password = PasswordField('Пароль', [validators.DataRequired()])
