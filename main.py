from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required
from models import Event
from app import db
from sqlalchemy.sql import extract
from datetime import datetime
from forms import BookingForm

main = Blueprint('main', __name__)

@main.route('/')
@login_required
def home():
    # Add content for the homepage
    return render_template('index.html')


@main.route('/make_reservation', methods=['GET', 'POST'])
@login_required
def make_reservation():
    form = BookingForm()
    if form.validate_on_submit():
        customer = Customer(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            company_name=form.company_name.data,
            address=form.address.data,
            city=form.city.data,
            state=form.state.data,
            zip_code=form.zip_code.data,
            country=form.country.data,
            phone_number=form.phone_number.data,
            email_address=form.email_address.data,
            tax_exempt=form.tax_exempt.data,
            discount_code=form.discount_code.data,
            emergency_contact_number=form.emergency_contact_number.data
        )
        db.session.add(customer)
        db.session.commit()

        reservation = Reservation(
            product_id=form.craft.data,
            customer_id=customer.id,
            start_datetime=form.start_time.data,
            end_datetime=form.end_time.data,
            status='New'  # or any default status you want to set
        )
        db.session.add(reservation)
        db.session.commit()

        flash('Reservation created successfully!', 'success')
        return redirect(url_for('auth.view_reservation'))
    return render_template('make_reservation.html', form=form)

@main.route('/view_reservations', methods=['GET'])
@login_required
def view_reservations():
    all_reservations = Reservation.query.all()
    return render_template('view_reservations.html', reservations=all_reservations)

@main.route('/edit_reservation/<int:reservation_id>', methods=['GET', 'POST'])
@login_required
def edit_reservation(reservation_id):
    reservation = Reservation.query.get_or_404(reservation_id)
    form = BookingForm(obj=reservation)
    if form.validate_on_submit():
        reservation.product_id = form.craft.data
        reservation.start_datetime = form.start_time.data
        reservation.end_datetime = form.end_time.data
        # Update customer details as well
        customer = Customer.query.get_or_404(reservation.customer_id)
        customer.first_name = form.first_name.data
        customer.last_name = form.last_name.data
        # ... update other customer fields ...
        db.session.commit()
        flash('Reservation updated successfully!', 'success')
        return redirect(url_for('auth.view_reservations'))
    return render_template('edit_reservation.html', form=form, reservation_id=reservation_id)

@main.route('/cancel_reservation/<int:reservation_id>', methods=['POST'])
@login_required
def cancel_reservation(reservation_id):
    reservation = Reservation.query.get_or_404(reservation_id)
    db.session.delete(reservation)
    db.session.commit()
    flash('Reservation cancelled successfully!', 'success')
    return redirect(url_for('auth.view_reservations'))

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



@main.route('/help_resources')
@login_required
def help_resources():
    return render_template('help_resources.html')
