from app import db
from datetime import datetime

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    end_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Event('{self.title}', '{self.start_date}', '{self.end_date}')"

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

class Craft(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text)
    max_availability = db.Column(db.Integer)  # Maximum units available for booking
    current_availability = db.Column(db.Integer)  # Currently available units

    def __repr__(self):
        return f"Craft('{self.name}', Available: {self.current_availability}/{self.max_availability})"
