import random
from faker import Faker
from extensions import db
from models import Event, Business, User, Product, Reservation, ReservationRate, RateCategory, RateList, Rate, AdditionalCharge, Customer, Availability, Maintenance, Craft
from werkzeug.security import generate_password_hash
from app import create_app


# Initialize Faker library
fake = Faker()

# Function to create dummy data for each model
def create_dummy_data():
    
    app = create_app()
    with app.app_context():
        # Create dummy businesses
        for _ in range(5):
            business = Business(
                name=fake.company(),
                description=fake.catch_phrase(),
                address=fake.address(),
                phone=fake.phone_number()
            )
            db.session.add(business)

        # Create dummy users and customers
        for _ in range(10):
            user = User(
                username=fake.user_name(),
                hashed_password=generate_password_hash('password'),
                email=fake.email(),
                role=random.choice(['admin', 'customer', 'staff'])
            )
            db.session.add(user)
            db.session.flush()  # Flush to get the user id for customer foreign key

            customer = Customer(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                company_name=fake.company(),
                address=fake.address(),
                city=fake.city(),
                state=fake.state(),
                zip_code=fake.zipcode(),
                country=fake.country(),
                phone_number=fake.phone_number(),
                email_address=fake.email(),
                tax_exempt=random.choice([True, False]),
                discount_code=fake.bothify(text='???-###'),
                emergency_contact_number=fake.phone_number()
            )
            customer.user.append(user)
            db.session.add(customer)

        # Create dummy events
        for _ in range(5):
            event = Event(
                title=fake.sentence(nb_words=6),
                start_date=fake.future_datetime(end_date="+30d"),
                end_date=fake.future_datetime(end_date="+60d")
            )
            db.session.add(event)

        # Create dummy products
        for _ in range(20):
            product = Product(
                business_id=random.randint(1, 5),
                name=fake.word(),
                description=fake.text(max_nb_chars=200)
            )
            db.session.add(product)

        # Create dummy reservations
        for _ in range(15):
            reservation = Reservation(
                event_id=random.randint(1, 5),
                product_id=random.randint(1, 20),
                customer_id=random.randint(1, 10),
                start_datetime=fake.date_time_this_year(before_now=False, after_now=True).isoformat(),
                end_datetime=fake.date_time_this_year(before_now=False, after_now=True).isoformat(),
                status=random.choice(['confirmed', 'pending', 'cancelled']),
                payment_details=fake.sentence(nb_words=10)
            )
            db.session.add(reservation)

        # Commit all changes to the database
        db.session.commit()

if __name__ == '__main__':
    create_dummy_data()