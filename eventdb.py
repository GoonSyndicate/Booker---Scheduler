from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

@app.route('/add_event', methods=['POST'])
def add_event():
    conn = sqlite3.connect('events.db')
    c = conn.cursor()
    data = request.json
    day = data['day']
    name = data['name']
    startTime = data['startTime']
    endTime = data['endTime']
    description = data['description']
    color = data['color']
    
    c.execute("INSERT INTO events (day, name, startTime, endTime, description, color) VALUES (?, ?, ?, ?, ?, ?)",
              (day, name, startTime, endTime, description, color))
    
    conn.commit()
    conn.close()
    return jsonify({"status": "success"})

@app.route('/get_events', methods=['GET'])
def get_events():
    conn = sqlite3.connect('events.db')
    c = conn.cursor()
    c.execute("SELECT * FROM events")
    events = c.fetchall()
    conn.close()
    return jsonify(events)

if __name__ == '__main__':
    conn = sqlite3.connect('events.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS events
                 (day integer, name text, startTime text, endTime text, description text, color text)''')
    conn.commit()
    conn.close()
    app.run(debug=True) 