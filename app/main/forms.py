from flask_wtf import FlaskForm
from wtforms import DateTimeLocalField
from wtforms.validators import DataRequired

class DateTimeForm(FlaskForm):
    input_date_time = DateTimeLocalField('Date Time', validators=[DataRequired()])
