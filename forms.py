from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, DateTimeField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Length
from wtforms.fields.html5 import DateField

# LoginForm: Used for user authentication
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

# SignupForm: Used for user registration
class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=80)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

# BookingForm: Used for booking crafts
class BookingForm(FlaskForm):
    craft = SelectField('Craft', coerce=int)
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    start_time = DateTimeField('Start Time', format='%Y-%m-%d %H:%M', validators=[DataRequired()])
    end_time = DateTimeField('End Time', format='%Y-%m-%d %H:%M', validators=[DataRequired()])
    submit = SubmitField('Book')

    def __init__(self, *args, **kwargs):
        super(BookingForm, self).__init__(*args, **kwargs)
        # Delayed import and query to avoid application context errors
        from models import Craft  # Import here to avoid circular import
        # Populate the 'craft' choices when the form is instantiated
        self.craft.choices = [(c.id, c.name) for c in Craft.query.all()]

# EventForm: Used for creating and managing events
class EventForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description')
    start_date = DateTimeField('Start Date & Time', format='%Y-%m-%d %H:%M', validators=[DataRequired()])
    end_date = DateTimeField('End Date & Time', format='%Y-%m-%d %H:%M', validators=[DataRequired()])
    color = StringField('Color')
    location = StringField('Location (Optional)')
    submit = SubmitField('Create Event')
