import sqlite3
from datetime import datetime, timedelta

# Connect to the existing SQLite database
conn = sqlite3.connect('events.db')
c = conn.cursor()

# Insert sample data into Boats
boats_data = [
    ('HULL123', 'REG123', 'ENG123', 'Yamaha', '242X', 'available', 'none'),
    ('HULL124', 'REG124', 'ENG124', 'Bayliner', 'Element E16', 'available', 'none'),
    # Add more as needed
]
c.executemany("INSERT INTO Boats (hull_id, registration_number, engine_serial_number, make, model, availability_status, maintenance_status) VALUES (?, ?, ?, ?, ?, ?, ?)", boats_data)

# Insert sample data into JetSkis
jetskis_data = [
    ('JSK123', 'JSKREG123', 'JSENG123', 'Sea-Doo', 'Spark', 'available', 'none'),
    ('JSK124', 'JSKREG124', 'JSENG124', 'Yamaha', 'EX', 'available', 'none'),
    # Add more as needed
]
c.executemany("INSERT INTO JetSkis (hull_id, registration_number, engine_serial_number, make, model, availability_status, maintenance_status) VALUES (?, ?, ?, ?, ?, ?, ?)", jetskis_data)

# Insert sample data into Accessories
accessories_data = [
    ('2-person tube', 'available'),
    ('Wakeboard', 'available'),
    # Add more as needed
]
c.executemany("INSERT INTO Accessories (type, availability_status) VALUES (?, ?)", accessories_data)

# Insert sample data into Bookings (let's assume user_id is 1 for now)
current_time = datetime.now()
booking_data = [
    (1, current_time, current_time + timedelta(hours=4)),
    # Add more as needed
]
c.executemany("INSERT INTO Bookings (user_id, start_time, end_time) VALUES (?, ?, ?)", booking_data)

# Insert sample data into Maintenance
maintenance_data = [
    (1, None, '2023-11-25'),  # Scheduled maintenance for boat with id 1
    (None, 1, '2023-11-26'),  # Scheduled maintenance for jet ski with id 1
    # Add more as needed
]
c.executemany("INSERT INTO Maintenance (boat_id, jet_ski_id, scheduled_date) VALUES (?, ?, ?)", maintenance_data)

# Commit changes to the database
conn.commit()

# Close the database connection
conn.close()
