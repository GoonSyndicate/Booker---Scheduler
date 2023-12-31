# Generated by Django 4.2.6 on 2023-10-05 20:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("reservations", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Customer",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("first_name", models.CharField(max_length=50)),
                ("last_name", models.CharField(max_length=50)),
                ("company_name", models.CharField(blank=True, max_length=100)),
                ("address", models.CharField(max_length=255)),
                ("city", models.CharField(max_length=50)),
                ("state", models.CharField(max_length=50)),
                ("zip_code", models.CharField(max_length=10)),
                ("country", models.CharField(max_length=50)),
                ("phone_number", models.CharField(max_length=15)),
                ("email", models.EmailField(max_length=100)),
                ("previous_customer", models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name="Location",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("address", models.CharField(max_length=255)),
                ("description", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="WaterToy",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("toy_type", models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name="Unit",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("hull_id", models.CharField(max_length=50, unique=True)),
                ("engine_serial_number", models.CharField(max_length=50, unique=True)),
                (
                    "availability_status",
                    models.CharField(
                        choices=[
                            ("Available", "Available"),
                            ("Maintenance", "Under Maintenance"),
                            ("Booked", "Booked"),
                        ],
                        default="Available",
                        max_length=12,
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="reservations.product",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Transaction",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateField()),
                ("start_time", models.TimeField()),
                ("end_time", models.TimeField()),
                (
                    "booking_total_amount",
                    models.DecimalField(decimal_places=2, max_digits=8),
                ),
                ("tax_amount", models.DecimalField(decimal_places=2, max_digits=8)),
                ("type", models.CharField(max_length=50)),
                ("invoice_number", models.CharField(max_length=50)),
                ("amount_paid", models.DecimalField(decimal_places=2, max_digits=8)),
                ("agent_email", models.EmailField(max_length=100)),
                ("discount_code", models.CharField(blank=True, max_length=50)),
                (
                    "discount_amount",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=8, null=True
                    ),
                ),
                ("subtotal", models.DecimalField(decimal_places=2, max_digits=8)),
                ("emergency_contact_number", models.CharField(max_length=15)),
                ("can_text", models.BooleanField(default=False)),
                ("life_jacket_sizes", models.CharField(blank=True, max_length=255)),
                ("customer_comments", models.TextField(blank=True)),
                ("office_notes", models.TextField(blank=True)),
                (
                    "customer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="reservations.customer",
                    ),
                ),
                (
                    "location",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="reservations.location",
                    ),
                ),
                (
                    "unit",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="reservations.unit",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ReservationToys",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("quantity", models.PositiveIntegerField()),
                (
                    "toy",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="reservations.watertoy",
                    ),
                ),
                (
                    "transaction",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="reservations.transaction",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Payment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("payment_type", models.CharField(max_length=50)),
                ("amount", models.DecimalField(decimal_places=2, max_digits=8)),
                ("deposit_amount", models.DecimalField(decimal_places=2, max_digits=8)),
                ("credit_card_type", models.CharField(max_length=50)),
                ("card_last_four", models.CharField(max_length=4)),
                ("expiration_date", models.DateField()),
                ("security_code", models.CharField(blank=True, max_length=4)),
                ("tax_exempt", models.BooleanField(default=False)),
                (
                    "transaction",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="reservations.transaction",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="MaintenanceLog",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date_of_maintenance", models.DateField()),
                ("description", models.TextField()),
                (
                    "customer",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="reservations.customer",
                    ),
                ),
                (
                    "unit",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="reservations.unit",
                    ),
                ),
            ],
        ),
    ]
