from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms import BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired


class WorksForm(FlaskForm):
    content1 = StringField("Title of activity")
    content2 = IntegerField("Team leader")
    content3 = IntegerField("Duration")
    content4 = StringField("list of collaborators")
    content5 = BooleanField("Is finished?")
    submit = SubmitField('Применить')