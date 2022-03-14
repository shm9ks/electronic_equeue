from wtforms.validators import DataRequired
from wtforms import StringField, SubmitField
from flask_wtf import FlaskForm

class getTicet_F(FlaskForm):
    last_name = StringField('Фамилия', validators=[DataRequired()])
    submit = SubmitField('Зарегестрироваться')