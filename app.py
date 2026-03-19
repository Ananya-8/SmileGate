from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sqlite3, json
from datetime import datetime, date

app = Flask(__name__, static_folder='frontend', static_url_path='')
DB = "smilegate.db"

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            enrollment TEXT UNIQUE NOT NULL,
            descriptor TEXT NOT NULL,
            photo TEXT
        )''')
        conn.execute('''CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            enrollment TEXT NOT NULL,
            name TEXT NOT NULL,
            smile_score REAL NOT NULL,
            entry_time TEXT NOT NULL,
            date TEXT NOT NULL
        )''')

init_db()

# ── Serve Frontend ──────────────────────────────────────────
@app.route('/')
def serve_checkin():
    return send_from_directory('frontend', 'index.html')

@app.route('/register')
def serve_register():
    return send_from_directory('frontend', 'register.html')

@app.route('/records')
def serve_records():
    return send_from_directory('frontend', 'records.html')

# ── API Routes ───────────────────────────────────────────────
@app.route('/api/register_student', methods=['POST'])
def register_student():
    data = request.json
    name = data['name']
    enrollment = data['enrollment']
    descriptor = json.dumps(data['descriptor'])
    photo = data.get('photo', '')
    try:
        with get_db() as conn:
            conn.execute(
                'INSERT INTO students (name, enrollment, descriptor, photo) VALUES (?,?,?,?)',
                (name, enrollment, descriptor, photo)
            )
        return jsonify({'success': True, 'message': f'{name} registered successfully!'})
    except sqlite3.IntegrityError:
        return jsonify({'success': False, 'message': 'Enrollment ID already exists!'}), 400

@app.route('/api/students', methods=['GET'])
def get_students():
    with get_db() as conn:
        rows = conn.execute('SELECT name, enrollment, descriptor, photo FROM students').fetchall()
    students = [
        {
            'name': r['name'],
            'enrollment': r['enrollment'],
            'descriptor': json.loads(r['descriptor']),
            'photo': r['photo']
        } for r in rows
    ]
    return jsonify(students)

@app.route('/api/checkin', methods=['POST'])
def checkin():
    data = request.json
    enrollment = data['enrollment']
    name = data['name']
    smile_score = data['smile_score']
    today = date.today().isoformat()
    with get_db() as conn:
        exists = conn.execute(
            'SELECT id FROM attendance WHERE enrollment=? AND date=?',
            (enrollment, today)
        ).fetchone()
        if exists:
            return jsonify({'success': False, 'message': f'{name} is already checked in today!'}), 400
        entry_time = datetime.now().strftime('%H:%M:%S')
        conn.execute(
            'INSERT INTO attendance (enrollment, name, smile_score, entry_time, date) VALUES (?,?,?,?,?)',
            (enrollment, name, smile_score, entry_time, today)
        )
    return jsonify({'success': True, 'entry_time': entry_time, 'message': f'{name} checked in at {entry_time}!'})

@app.route('/api/attendance', methods=['GET'])
def get_attendance():
    with get_db() as conn:
        rows = conn.execute(
            'SELECT * FROM attendance ORDER BY id DESC LIMIT 200'
        ).fetchall()
    return jsonify([dict(r) for r in rows])

@app.route('/api/delete_student/<enrollment>', methods=['DELETE'])
def delete_student(enrollment):
    with get_db() as conn:
        conn.execute('DELETE FROM students WHERE enrollment=?', (enrollment,))
        conn.execute('DELETE FROM attendance WHERE enrollment=?', (enrollment,))
    return jsonify({'success': True, 'message': 'Student deleted.'})

@app.route('/api/stats', methods=['GET'])
def get_stats():
    today = date.today().isoformat()
    with get_db() as conn:
        total_members = conn.execute('SELECT COUNT(*) FROM students').fetchone()[0]
        total_checkins = conn.execute('SELECT COUNT(*) FROM attendance').fetchone()[0]
        today_checkins = conn.execute('SELECT COUNT(*) FROM attendance WHERE date=?', (today,)).fetchone()[0]
        avg_smile_row = conn.execute('SELECT AVG(smile_score) FROM attendance').fetchone()[0]
        avg_smile = round(avg_smile_row or 0)
    return jsonify({
        'total_members': total_members,
        'total_checkins': total_checkins,
        'today_checkins': today_checkins,
        'avg_smile': avg_smile
    })

if __name__ == '__main__':
    import os
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
