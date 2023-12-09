from django.db import models

class Category(models.Model):
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.description

class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Unit(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    hull_id = models.CharField(max_length=50, unique=True)
    engine_serial_number = models.CharField(max_length=50, unique=True)
    AVAILABILITY_CHOICES = (
        ('Available', 'Available'),
        ('Maintenance', 'Under Maintenance'),
        ('Booked', 'Booked'),
    )
    availability_status = models.CharField(max_length=12, choices=AVAILABILITY_CHOICES, default='Available')

    def __str__(self):
        return f"{self.product.name} - {self.hull_id}"

class WaterToy(models.Model):
    toy_type = models.CharField(max_length=50)

    def __str__(self):
        return self.toy_type

class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    company_name = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=10)
    country = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(max_length=100)
    previous_customer = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Location(models.Model):
    address = models.CharField(max_length=255)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.description

class Transaction(models.Model):
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    booking_total_amount = models.DecimalField(max_digits=8, decimal_places=2)
    tax_amount = models.DecimalField(max_digits=8, decimal_places=2)
    type = models.CharField(max_length=50)
    invoice_number = models.CharField(max_length=50)
    amount_paid = models.DecimalField(max_digits=8, decimal_places=2)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    agent_email = models.EmailField(max_length=100)
    discount_code = models.CharField(max_length=50, blank=True)
    discount_amount = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    subtotal = models.DecimalField(max_digits=8, decimal_places=2)
    emergency_contact_number = models.CharField(max_length=15)
    can_text = models.BooleanField(default=False)
    life_jacket_sizes = models.CharField(max_length=255, blank=True)
    customer_comments = models.TextField(blank=True)
    office_notes = models.TextField(blank=True)

    def __str__(self):
        return self.invoice_number

class ReservationToys(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    toy = models.ForeignKey(WaterToy, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.transaction.invoice_number} - {self.toy.toy_type}"

class MaintenanceLog(models.Model):
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    date_of_maintenance = models.DateField()
    description = models.TextField()
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"{self.unit.product.name} - {self.date_of_maintenance}"

class Payment(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    payment_type = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    deposit_amount = models.DecimalField(max_digits=8, decimal_places=2)
    credit_card_type = models.CharField(max_length=50)
    card_last_four = models.CharField(max_length=4)
    expiration_date = models.DateField()
    security_code = models.CharField(max_length=4, blank=True)
    tax_exempt = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.transaction.invoice_number} - {self.amount}"
