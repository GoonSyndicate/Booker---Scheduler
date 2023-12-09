from flask import Flask, request, jsonify, render_template

from flask_cors import CORS  



import sqlite3  

import json


  

app = Flask(__name__)  

CORS(app, resources={r"/add_event": {"origins": "http://localhost:5000"}})


# Initialize database

def initialize_db():

    conn = sqlite3.connect('events.db')  

    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS events

             (id INTEGER PRIMARY KEY AUTOINCREMENT,    

              date TEXT, name TEXT, startTime TEXT,     

              endTime TEXT, description TEXT, color TEXT, availability TEXT)''')



    c.execute('''CREATE TABLE IF NOT EXISTS availability    

             (id INTEGER PRIMARY KEY AUTOINCREMENT,    

              date TEXT, startTime TEXT, endTime TEXT, craft_type TEXT, status TEXT)''')    



    c.execute('''CREATE TABLE IF NOT EXISTS bookings    

             (id INTEGER PRIMARY KEY AUTOINCREMENT,    

              user_id INTEGER, start_date TEXT, end_date TEXT, items TEXT)''')  



    c.execute('''CREATE TABLE IF NOT EXISTS maintenance    

             (id INTEGER PRIMARY KEY AUTOINCREMENT,    

              item_id INTEGER, start_date TEXT, end_date TEXT)''')



    c.execute('''CREATE TABLE IF NOT EXISTS inventory

             (id INTEGER PRIMARY KEY AUTOINCREMENT,

              craft_type_id INTEGER, watercraft_id INTEGER, status TEXT)''')



    c.execute('''CREATE TABLE IF NOT EXISTS watercraft

             (id INTEGER PRIMARY KEY AUTOINCREMENT,

              name TEXT, craft_type_id INTEGER, description TEXT, status TEXT)''')



    conn.commit()

    conn.close()



@app.route('/')
def home():
    return render_template('index.html')



@app.route('/get_events', methods=['GET'])    

def get_events():    

    year = request.args.get('year')    

    month = request.args.get('month')    

    conn = sqlite3.connect('events.db')    

    c = conn.cursor()    

    c.execute("SELECT * FROM events WHERE date LIKE ?", (f"{year}-{int(month)+1}-%",))    

    events = c.fetchall()    

    conn.close()    

    return jsonify(events)    

    

@app.route('/add_event', methods=['POST'])    

def add_event():    

    conn = sqlite3.connect('events.db')    

    c = conn.cursor()    

    data = request.json    

    try:    

        c.execute("INSERT INTO events (date, name, startTime, endTime, description, color, availability) VALUES (?, ?, ?, ?, ?, ?, ?)",    

                  (data['date'], data['name'], data['startTime'], data['endTime'], data['description'], data['color'], data['availability']))    

        conn.commit()    

        return jsonify({"status": "success"})    

    except sqlite3.Error as e:    

        conn.rollback()    

        return jsonify({"status": "failed", "reason": str(e)})    

    finally:    

        conn.close()    



@app.route('/get_availability', methods=['GET'])

def get_availability():

    start_date = request.args.get('start_date')

    end_date = request.args.get('end_date')

    conn = sqlite3.connect('events.db')

    c = conn.cursor()

    c.execute("SELECT * FROM availability WHERE date BETWEEN ? AND ?", (start_date, end_date))

    availability = c.fetchall()

    conn.close()

    return jsonify(availability)



@app.route('/book', methods=['POST'])
def book():
    data = request.json
    conn = sqlite3.connect('events.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO bookings (user_id, start_date, end_date, items) VALUES (?, ?, ?, ?)",
                  (data['user_id'], data['start_date'], data['end_date'], json.dumps(data['items'])))
        conn.commit()
        return jsonify({"status": "success"})
    except sqlite3.Error as e:
        conn.rollback()
        return jsonify({"status": "failed", "reason": str(e)})
    finally:
        conn.close()




@app.route('/schedule_maintenance', methods=['POST'])

def schedule_maintenance():

    data = request.json

    conn = sqlite3.connect('events.db')

    c = conn.cursor()

    try:

        c.execute("INSERT INTO maintenance (item_id, start_date, end_date) VALUES (?, ?, ?)",

                  (data['item_id'], data['start_date'], data['end_date']))

        conn.commit()

        return jsonify({"status": "success"})

    except sqlite3.Error as e:

        conn.rollback()

        return jsonify({"status": "failed", "reason": str(e)})

    finally:

        conn.close()



if __name__ == '__main__':  

    initialize_db()

    app.run(debug=True)
