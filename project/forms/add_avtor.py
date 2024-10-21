from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import SubmitField


class AvtorsForm(FlaskForm):
    content1 = StringField("Имя")
    content2 = StringField("Фамилия")
    submit = SubmitField('Добавить')
