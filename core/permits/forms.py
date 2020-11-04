from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, FloatField, RadioField, SelectField
from wtforms.validators import DataRequired, Length, InputRequired, NumberRange

from core.models import Permit

LOCATION = [('bwd', 'BWD'), ('hnd', 'HND'), ('cch', 'CCH'), ('syo', 'SYO')]
CHOICES = [('yes', 'Yes'), ('no', 'No')]


class PermitForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=3, message='Title is too short')])
    text = TextAreaField('Findings', validators=[DataRequired(), Length(min=2, message='Description is too short')])
    location = SelectField('Location', choices=LOCATION, default=0)
    mileage = FloatField('Mileage', validators=[InputRequired(message='Please put a mileage'),
                                                            NumberRange(min=1, message='Value must be 1 or above')])
    resolved = RadioField('Was resolved?', choices=CHOICES, validators=[InputRequired()], default=('yes'))
    follow_up = RadioField('Follow Up required?', choices=CHOICES, validators=[InputRequired()], default=('yes'))
    submit = SubmitField('Submit')

