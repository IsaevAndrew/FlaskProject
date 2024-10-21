from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField


class OpinionsForm(FlaskForm):
    about = TextAreaField("Отзыв")
    submit = SubmitField('Добавить')
