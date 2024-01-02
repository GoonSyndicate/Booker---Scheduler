# app.py

from datetime import datetime
from flask import Flask, request, session, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length
import os
from sqlalchemy.sql import extract


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    content = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Page {self.title}>'


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    end_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Event('{self.title}', '{self.start_date}', '{self.end_date}')"

# Database model definitions
class Business(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text)
    address = db.Column(db.String(120))
    phone = db.Column(db.String(20))

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    hashed_password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), unique=True)
    role = db.Column(db.String(80))

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    business_id = db.Column(db.Integer, db.ForeignKey('business.id'))
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text)

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    start_datetime = db.Column(db.String(80), nullable=False)
    end_datetime = db.Column(db.String(80), nullable=False)
    status = db.Column(db.String(50))
    payment_details = db.Column(db.Text)

    def __repr__(self):
        return f"Reservation('{self.event_id}')"

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    contact_details = db.Column(db.String(120))
    address = db.Column(db.String(120))

class Availability(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    date = db.Column(db.String(80), nullable=False)
    number_of_units = db.Column(db.Integer)
    reserved_units = db.Column(db.Integer)
    available_units = db.Column(db.Integer)

class Maintenance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    start_datetime = db.Column(db.String(80), nullable=False)
    end_datetime = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text)

@app.route('/page/<slug>')
def show_page(slug):
    page = Page.query.filter_by(slug=slug).first_or_404()
    return render_template('page.html', page=page)


def check_conflict(event):
    conflicting_events = Event.query.filter(
        (Event.start_date <= event.end_date) & (Event.end_date >= event.start_date)
    ).all()

    conflicting_reservations = Reservation.query.filter(
        (Reservation.event_id != event.id) &
        (Reservation.event_id.in_([e.id for e in conflicting_events]))
    ).all()

    if conflicting_events or conflicting_reservations:
        return True
    else:
        return False


# Flask-Login user loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Login form
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

# Signup form
class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=80)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.hashed_password, password):
            login_user(user)
            return redirect(url_for('home'))
        else:
            error = 'Invalid username or password'
            return render_template('login.html', form=form, error=error)

    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = SignupForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        confirm_password = form.confirm_password.data

        if password != confirm_password:
            error = 'Passwords do not match'
            return render_template('signup.html', form=form, error=error)

        user = User.query.filter_by(username=username).first()
        if user:
            error = 'Username already exists'
            return render_template('signup.html', form=form, error=error)

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, hashed_password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('signup.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def home():
    # Add content for the homepage
    return render_template('index.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/reservations')
@login_required
def reservations():
    return render_template('reservations.html')


@app.route('/calendar')
@login_required
def calendar():
    # Get the current year and month
    today = datetime.today()
    year = today.year
    month = today.month

    # Query events for the current month and year
    events = Event.query.filter(
        extract('year', Event.start_date) == year,
        extract('month', Event.start_date) == month
    ).all()

    return render_template('calendar.html', events=events)


def create_event(event):
    if not check_conflict(event):
        db.session.add(event)
        db.session.commit()
        return True
    else:
        return False

def create_reservation(reservation):
    if not check_conflict(reservation):
        db.session.add(reservation)
        db.session.commit()
        return True
    else:
        return False


@app.route('/reviews')
@login_required
def reviews():
    return render_template('reviews.html')

@app.route('/reports')
@login_required
def reports():
    return render_template('reports.html')

@app.route('/setup_business')
@login_required
def setup_business():
    return render_template('setup_business.html')

@app.route('/setup_products')
@login_required
def setup_products():
    return render_template('setup_products.html')

@app.route('/online_bookings')
@login_required
def online_bookings():
    return render_template('online_bookings.html')

@app.route('/help_resources')
@login_required
def help_resources():
    return render_template('help_resources.html')

if __name__ == '__main__':
    app.run(debug=True)
