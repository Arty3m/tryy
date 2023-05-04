from flask_wtf.file import FileAllowed, FileRequired
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField, IntegerField, DecimalField, StringField, BooleanField, TextAreaField, \
    validators


# class AddProductForm(FlaskForm):
class AddProductForm(FlaskForm):
    name = StringField('Название', [validators.DataRequired()])
    price = DecimalField('Цена', [validators.DataRequired()])
    discount = IntegerField('Скидка', default=0)
    stock = IntegerField('Stock', [validators.DataRequired()])
    description = TextAreaField('Описание', [validators.DataRequired()])

    image_1 = FileField('Image 1*', validators=[FileAllowed(['jpg', 'png', 'gif', 'jpeg'],
                                                            message='Images only please')])
    image_2 = FileField('Image 2', validators=[FileAllowed(['jpg', 'png', 'gif', 'jpeg'],
                                                           message='Images only please')])
    image_3 = FileField('Image 3', validators=[FileAllowed(['jpg', 'png', 'gif', 'jpeg'],
                                                           message='Images only please')])
