import sqlite3

# Connect to the existing SQLite database
conn = sqlite3.connect('events.db')
c = conn.cursor()

# Create new tables for Boats, JetSkis, Accessories, Bookings, Calendar, and Maintenance
c.execute('''
CREATE TABLE IF NOT EXISTS Boats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    hull_id TEXT,
    registration_number TEXT,
    engine_serial_number TEXT,
    make TEXT,
    model TEXT,
    availability_status TEXT,
    maintenance_status TEXT
);
''')

c.execute('''
CREATE TABLE IF NOT EXISTS JetSkis (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    hull_id TEXT,
    registration_number TEXT,
    engine_serial_number TEXT,
    make TEXT,
    model TEXT,
    availability_status TEXT,
    maintenance_status TEXT
);
''')

c.execute('''
CREATE TABLE IF NOT EXISTS Accessories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT,
    availability_status TEXT
);
''')

c.execute('''
CREATE TABLE IF NOT EXISTS Bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    start_time TEXT,
    end_time TEXT
);
''')

c.execute('''
CREATE TABLE IF NOT EXISTS Calendar (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    boat_id INTEGER,
    jet_ski_id INTEGER,
    booking_id INTEGER,
    status TEXT,
    FOREIGN KEY(boat_id) REFERENCES Boats(id),
    FOREIGN KEY(jet_ski_id) REFERENCES JetSkis(id),
    FOREIGN KEY(booking_id) REFERENCES Bookings(id)
);
''')

c.execute('''
CREATE TABLE IF NOT EXISTS Maintenance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    boat_id INTEGER,
    jet_ski_id INTEGER,
    scheduled_date TEXT,
    FOREIGN KEY(boat_id) REFERENCES Boats(id),
    FOREIGN KEY(jet_ski_id) REFERENCES JetSkis(id)
);
''')

# Insert sample data (optional)
c.execute("INSERT INTO Boats (hull_id, registration_number, engine_serial_number, make, model, availability_status, maintenance_status) VALUES ('HULL123', 'REG123', 'ENG123', 'Make1', 'Model1', 'available', 'none')")
c.execute("INSERT INTO JetSkis (hull_id, registration_number, engine_serial_number, make, model, availability_status, maintenance_status) VALUES ('HULL124', 'REG124', 'ENG124', 'Make2', 'Model2', 'available', 'none')")
c.execute("INSERT INTO Accessories (type, availability_status) VALUES ('2-person tube', 'available')")

# Commit changes and close the connection
conn.commit()
conn.close()
