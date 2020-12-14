from wtforms import StringField, SubmitField, ValidationError, SubmitField, \
                    IntegerField, BooleanField, TextAreaField, DecimalField
from .models import Brand, Category
from flask_wtf import FlaskForm
from wtforms.validators import  InputRequired, DataRequired
from flask_wtf.file import FileAllowed, FileField, FileRequired

class BrandForm(FlaskForm):
    username = StringField()
    name = StringField('Brand', validators=[InputRequired('Brand Name is required')])
    submit = SubmitField('Add Brand')

    def validate_name(self, field):
        brand = Brand.query.filter_by(name=field.data).first()
        if brand:
            raise ValidationError('Brand Name already in use.')


class CategoryForm(FlaskForm):
    name = StringField('Category', validators=[InputRequired('Category Name is required')])
    username = StringField()
    submit = SubmitField('Add Category')

    def validate_name(self, field):
        category = Category.query.filter_by(name=field.data).first()
        if category:
            raise ValidationError('Category Name already in use.')

class AddProductsForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    price = DecimalField('Price', validators=[DataRequired()])
    stock = IntegerField('Stock', validators=[DataRequired()])
    discount = IntegerField('Discount', default=0)
    description = TextAreaField('Description', validators=[DataRequired()])
    colors = TextAreaField('Colors', validators=[DataRequired()])

    image_1 = FileField('Image 1', validators=[FileAllowed(['jpg', 'png', 'gif', 'jpeg'], "wrong format!")])
    image_2 = FileField('Image 2', validators=[FileAllowed(['jpg', 'png', 'gif', 'jpeg'], "wrong format!")])
    image_3 = FileField('Image 3', validators=[FileAllowed(['jpg', 'png', 'gif', 'jpeg'], "wrong format!")])

    submit = SubmitField('Add Products')

    username = StringField()
