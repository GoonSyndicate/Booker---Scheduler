from extensions import db
from datetime import datetime
from flask_login import UserMixin

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

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    hashed_password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), unique=True)
    role = db.Column(db.String(80))
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=True)
    customer = db.relationship('Customer', backref='user', lazy=True) 


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

class ReservationRate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reservation_id = db.Column(db.Integer, db.ForeignKey('reservation.id'), nullable=False)
    item_description = db.Column(db.String(255))
    amount = db.Column(db.Float, nullable=False)

class RateCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    display_to_customers = db.Column(db.Boolean, default=True)
    # Additional fields as necessary

class RateList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    valid_from = db.Column(db.DateTime, nullable=False)
    valid_to = db.Column(db.DateTime, nullable=False)
    # Relationships
    rates = db.relationship('Rate', backref='rate_list', lazy=True)

class Rate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rate_list_id = db.Column(db.Integer, db.ForeignKey('rate_list.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('rate_category.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    # Additional fields as necessary

class AdditionalCharge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    # Additional fields as necessary

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    company_name = db.Column(db.String(120), nullable=True)
    address = db.Column(db.String(120), nullable=False)
    city = db.Column(db.String(80), nullable=False)
    state = db.Column(db.String(80), nullable=False)
    zip_code = db.Column(db.String(20), nullable=False)
    country = db.Column(db.String(80), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    email_address = db.Column(db.String(120), nullable=False)
    tax_exempt = db.Column(db.Boolean, default=False)
    discount_code = db.Column(db.String(80), nullable=True)
    emergency_contact_number = db.Column(db.String(20), nullable=True)

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
    reservation_type = db.Column(db.String(50))  # Daily, Hourly, etc.
    pictures = db.relationship('Picture', backref='craft', lazy=True)
    reservation_rules = db.relationship('ReservationRule', back_populates='craft', lazy=True)
    units = db.relationship('Unit', backref='craft', lazy=True)
    # Additional fields as necessary

    def __repr__(self):
        return f"Craft('{self.name}', Available: {self.current_availability}/{self.max_availability})"

class Picture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    craft_id = db.Column(db.Integer, db.ForeignKey('craft.id'), nullable=False)
    image_url = db.Column(db.String(255))  # URL to the image

class ReservationRule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    craft_id = db.Column(db.Integer, db.ForeignKey('craft.id'), nullable=False)
    rule_description = db.Column(db.Text)  # Description of the rule
    craft = db.relationship('Craft', back_populates='reservation_rules')
    
class Unit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    craft_id = db.Column(db.Integer, db.ForeignKey('craft.id'), nullable=False)
    name = db.Column(db.String(80))  # Name or number of the unit
    
    # Additional fields as necessary

class CustomerInfoField(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    field_name = db.Column(db.String(80), nullable=False)
    field_type = db.Column(db.String(50))  # Text, Checkbox, etc.
    required = db.Column(db.Boolean, default=False)
    # Additional fields as necessary
