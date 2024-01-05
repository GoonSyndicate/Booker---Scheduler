from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from models import User, Customer, Reservation, Craft
from forms import LoginForm, SignupForm, BookingForm

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.hashed_password, form.password.data):
            login_user(user)
            return redirect(url_for('main.dashboard'))
        else:
            flash('Invalid username or password', 'error')
    return render_template('login.html', form=form)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash('password')
        new_user = User(username=form.username.data, hashed_password=hashed_password)
        db.session.add(new_user)
        try:
            db.session.commit()
            flash('Account created successfully!', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash(str(e), 'error')
    return render_template('signup.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/make_reservation', methods=['GET', 'POST'])
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

@auth.route('/view_reservations', methods=['GET'])
@login_required
def view_reservations():
    all_reservations = Reservation.query.all()
    return render_template('view_reservations.html', reservations=all_reservations)

@auth.route('/edit_reservation/<int:reservation_id>', methods=['GET', 'POST'])
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

@auth.route('/cancel_reservation/<int:reservation_id>', methods=['POST'])
@login_required
def cancel_reservation(reservation_id):
    reservation = Reservation.query.get_or_404(reservation_id)
    db.session.delete(reservation)
    db.session.commit()
    flash('Reservation cancelled successfully!', 'success')
    return redirect(url_for('auth.view_reservations'))