from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required
from models import Event
from app import db
from sqlalchemy.sql import extract
from datetime import datetime

main = Blueprint('main', __name__)

@main.route('/')
@login_required
def home():
    # Add content for the homepage
    return render_template('index.html')

@main.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@main.route('/reservations')
@login_required
def reservations():
    # Example: Retrieve and pass reservations data to the template
    # reservations = Reservation.query.all()
    return render_template('reservations.html')  # , reservations=reservations

@main.route('/calendar')
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

@main.route('/reviews')
@login_required
def reviews():
    return render_template('reviews.html')

@main.route('/reports')
@login_required
def reports():
    return render_template('reports.html')

@main.route('/setup_business')
@login_required
def setup_business():
    return render_template('setup_business.html')

@main.route('/setup_products')
@login_required
def setup_products():
    return render_template('setup_products.html')

@main.route('/online_bookings')
@login_required
def online_bookings():
    return render_template('online_bookings.html')

@main.route('/help_resources')
@login_required
def help_resources():
    return render_template('help_resources.html')
