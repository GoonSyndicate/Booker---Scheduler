from django.core.management.base import BaseCommand
from reservations.models import Category, Product, Unit, WaterToy, Transaction, Customer, Location, Payment

class Command(BaseCommand):
    help = 'Populates the database with sample data'

    def handle(self, *args, **kwargs):
        # Populating Category Table
        boat_category = Category.objects.create(description="Boat")
        jetski_category = Category.objects.create(description="Jet Ski")

        # Populating Product Table
        tritoon_product = Product.objects.create(name="24' Bennington SVSR Tritoon", category=boat_category)

        # Populating Unit Table
        Unit.objects.create(product=tritoon_product, hull_id="HULL12345", engine_serial_number="ENG12345", availability_status="Available")

        # Populating WaterToy Table
        WaterToy.objects.create(toy_type="water skis")
        WaterToy.objects.create(toy_type="wakeboard")
        WaterToy.objects.create(toy_type="2-person tube")
        WaterToy.objects.create(toy_type="knee-board")

        # Populating Customer Table (just a sample, you can add more fields)
        customer_sample = Customer.objects.create(first_name="John", last_name="Doe", phone_number="1234567890", email="john@example.com")

        # Populating Location Table (just a sample)
        location_sample = Location.objects.create(address="123 Lake St.", description="Main dock")

        # Populating Transaction Table (just a sample, you can add more fields)
        transaction_sample = Transaction.objects.create(date="2023-10-05", start_time="10:00", end_time="14:00", location=location_sample, booking_total_amount=500, customer=customer_sample, unit_id=1, agent_email="lakekeoweeboatrentals@gmail.com", amount_paid=0)

        # Populating Payment Table (just a sample, you can add more fields)
        Payment.objects.create(transaction=transaction_sample, payment_type="Credit Card (Charge)", amount=500, deposit_amount=500, credit_card_type="Visa", card_last_four="1234", expiration_date="01/2025")

        self.stdout.write(self.style.SUCCESS('Database populated with sample data!'))
