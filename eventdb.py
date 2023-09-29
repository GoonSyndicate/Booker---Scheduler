from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)


@app.route('/get_events', methods=['GET'])
def get_events():
    conn = sqlite3.connect('events.db')
    c = conn.cursor()
    c.execute("SELECT * FROM events")
    events = c.fetchall()
    conn.close()
    return jsonify(events)

@app.route('/add_event', methods=['POST'])
def add_event():
    conn = sqlite3.connect('events.db')
    c = conn.cursor()
    data = request.json
    try:
        c.execute("INSERT INTO events (day, name, startTime, endTime, description, color) VALUES (?, ?, ?, ?, ?, ?)",
                  (data['day'], data['name'], data['startTime'], data['endTime'], data['description'], data['color']))
        conn.commit()
        print("Data inserted successfully")
        return jsonify({"status": "success"})
    except sqlite3.Error as e:
        print("SQL error:", e)
        conn.rollback()
        return jsonify({"status": "failed", "reason": str(e)})
    finally:
        conn.close()


@app.route('/update_event', methods=['PUT'])
def update_event():
    conn = sqlite3.connect('events.db')
    c = conn.cursor()
    data = request.json
    try:
        if data['id']:
            c.execute("UPDATE events SET day = ?, name = ?, startTime = ?, endTime = ?, description = ?, color = ? WHERE id = ?",
                      (data['day'], data['name'], data['startTime'], data['endTime'], data['description'], data['color'], data['id']))
            conn.commit()
            print("Data updated successfully")
            return jsonify({"status": "success"})
        else:
            print("No id provided for update. Ignoring.")
            return jsonify({"status": "failed", "reason": "No id provided for update"})
    except sqlite3.Error as e:
        print("SQL error:", e)
        conn.rollback()
        return jsonify({"status": "failed", "reason": str(e)})
    finally:
        conn.close()


@app.route('/delete_event', methods=['DELETE'])
def delete_event():
    conn = sqlite3.connect('events.db')
    c = conn.cursor()
    data = request.json
    try:
        c.execute("DELETE FROM events WHERE id = ?", (data['id'],))
        conn.commit()
        return jsonify({"status": "success"})
    except sqlite3.Error as e:
        print("SQL error:", e)
        conn.rollback()
        return jsonify({"status": "failed", "reason": str(e)})
    finally:
        conn.close()
    
if __name__ == '__main__':
    conn = sqlite3.connect('events.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS events
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  day INTEGER, name TEXT, startTime TEXT, 
                  endTime TEXT, description TEXT, color TEXT)''')
    conn.commit()
    conn.close()
    app.run(debug=True)