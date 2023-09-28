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
    c.execute("SELECT id, day, name, startTime, endTime, description, color FROM events")
    events = c.fetchall()
    conn.close()
    return jsonify(events)

@app.route('/update_event', methods=['PUT'])
def update_event():
    conn = sqlite3.connect('events.db')
    c = conn.cursor()
    data = request.json
    event_id = data['id']
    day = data['day']
    name = data['name']
    startTime = data['startTime']
    endTime = data['endTime']
    description = data['description']
    color = data['color']

    c.execute("UPDATE events SET day = ?, name = ?, startTime = ?, endTime = ?, description = ?, color = ? WHERE id = ?",
              (day, name, startTime, endTime, description, color, event_id))

    conn.commit()
    conn.close()
    return jsonify({"status": "success"})


@app.route('/delete_event', methods=['DELETE'])
def delete_event():
    conn = sqlite3.connect('events.db')
    c = conn.cursor()
    data = request.json
    event_id = data['id']

    c.execute("DELETE FROM events WHERE id = ?", (event_id,))

    conn.commit()
    conn.close()
    return jsonify({"status": "success"})


if __name__ == '__main__':
    conn = sqlite3.connect('events.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS events
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              day integer, name text, startTime text, 
              endTime text, description text, color text)''')
    conn.commit()
    conn.close()
    app.run(debug=True)