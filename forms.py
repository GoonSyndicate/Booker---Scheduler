from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, DateTimeField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, EqualTo, Length, Optional, Email
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

# BookingForm: Used for booking crafts and collecting customer information
class BookingForm(FlaskForm):
    # Craft selection
    craft = SelectField('Craft', coerce=int, validators=[DataRequired()])
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    start_time = DateTimeField('Start Time', format='%Y-%m-%d %H:%M', validators=[DataRequired()])
    end_time = DateTimeField('End Time', format='%Y-%m-%d %H:%M', validators=[DataRequired()])

    # Customer information fields
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    company_name = StringField('Company Name', validators=[Optional()])
    address = StringField('Address', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired()])
    zip_code = StringField('Zip/Postal Code', validators=[DataRequired()])
    country = SelectField('Country', validators=[DataRequired()])  # You'll need to populate the choices for this field
    phone_number = StringField('Phone Number', validators=[DataRequired()])
    email_address = StringField('Email Address', validators=[DataRequired(), Email()])
    tax_exempt = BooleanField('Tax Exempt')
    discount_code = StringField('Discount/Gift Card Code', validators=[Optional()])
    emergency_contact_number = StringField('Emergency Contact Number', validators=[Optional()])

    # Additional fields as necessary

    submit = SubmitField('Book')

    def __init__(self, *args, **kwargs):
        super(BookingForm, self).__init__(*args, **kwargs)
        # Delayed import and query to avoid application context errors
        from models import Craft  # Import here to avoid circular import
        # Populate the 'craft' choices when the form is instantiated
        self.craft.choices = [(c.id, c.name) for c in Craft.query.all()]
        # Populate the 'country' choices
        self.country.choices = [('USA', 'United States'), ('CAN', 'Canada')]  # Add more countries as needed

# EventForm: Used for creating and managing events
class EventForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description')
    start_date = DateTimeField('Start Date & Time', format='%Y-%m-%d %H:%M', validators=[DataRequired()])
    end_date = DateTimeField('End Date & Time', format='%Y-%m-%d %H:%M', validators=[DataRequired()])
    color = StringField('Color')
    location = StringField('Location (Optional)')
    submit = SubmitField('Create Event')