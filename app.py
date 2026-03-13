"""
========================================================
  Smile-Based Smart Attendance System
  FILE: app.py
  PURPOSE: Flask web server that:
             • Serves the HTML frontend
             • Accepts webcam frames from the browser
             • Calls the recognition engine
             • Returns JSON results
             • Provides routes for registration &
               attendance log viewing
========================================================
"""

from flask import (
    Flask, render_template, request, jsonify, redirect, url_for
)
import sqlite3
import os
import base64
import cv2
import numpy as np
import face_recognition

# Import our custom recognition engine
from recognize_and_attend import process_frame, SMILE_THRESHOLD

# ── App setup ──────────────────────────────────────────────────────────────────
app = Flask(__name__)
app.secret_key = "smile_attendance_secret_key_2024"   # required for sessions

DB_PATH = os.path.join(os.path.dirname(__file__), "database", "attendance.db")


# ── Database helper ────────────────────────────────────────────────────────────
def get_db():
    """Opens and returns a database connection with dict-like row access."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# ══════════════════════════════════════════════════════════════════════════════
#  FRONTEND ROUTES
# ══════════════════════════════════════════════════════════════════════════════

@app.route("/")
def index():
    """Home page – displays the live attendance scanner."""
    return render_template("index.html", smile_threshold=SMILE_THRESHOLD)


@app.route("/register")
def register_page():
    """Student registration page – capture face and save to DB."""
    return render_template("register.html")


@app.route("/attendance_log")
def attendance_log():
    """
    Attendance log page – displays all attendance records joined
    with student information.
    """
    conn = get_db()
    records = conn.execute("""
        SELECT
            s.name,
            s.enrollment_no,
            a.date,
            a.time,
            a.smile_score
        FROM attendance a
        JOIN students s ON a.student_id = s.id
        ORDER BY a.date DESC, a.time DESC
    """).fetchall()

    # Fetch all registered students for the sidebar summary
    students = conn.execute(
        "SELECT id, name, enrollment_no, registered_at FROM students ORDER BY name"
    ).fetchall()
    conn.close()

    return render_template(
        "attendance_log.html",
        records=records,
        students=students
    )


# ══════════════════════════════════════════════════════════════════════════════
#  API ROUTES (called from JavaScript in the browser)
# ══════════════════════════════════════════════════════════════════════════════

@app.route("/api/recognize", methods=["POST"])
def api_recognize():
    """
    Receives a base64-encoded JPEG frame from the browser.
    Passes it to the recognition engine and returns the result as JSON.

    Expected JSON body:
      { "image": "<base64 JPEG string>" }
    """
    data = request.get_json()

    if not data or "image" not in data:
        return jsonify({"status": "error", "message": "No image data received."}), 400

    # Strip the data-URI prefix if present (e.g. "data:image/jpeg;base64,...")
    image_b64 = data["image"]
    if "," in image_b64:
        image_b64 = image_b64.split(",")[1]

    # Decode base64 → raw bytes
    try:
        jpeg_bytes = base64.b64decode(image_b64)
    except Exception:
        return jsonify({"status": "error", "message": "Invalid base64 image."}), 400

    # Run the full recognition + attendance pipeline
    result = process_frame(jpeg_bytes)
    return jsonify(result)


@app.route("/api/register_student", methods=["POST"])
def api_register_student():
    """
    Receives a student's name, enrollment number, and a base64 JPEG frame.
    Generates the face encoding and stores the student in the database.

    Expected JSON body:
      {
        "name": "John Doe",
        "enrollment_no": "CS2024001",
        "image": "<base64 JPEG string>"
      }
    """
    data = request.get_json()

    # ── Validate input ─────────────────────────────────────────────────────────
    name = (data.get("name") or "").strip()
    enrollment_no = (data.get("enrollment_no") or "").strip()
    image_b64 = data.get("image", "")

    if not name or not enrollment_no or not image_b64:
        return jsonify({
            "status": "error",
            "message": "Name, enrollment number, and image are all required."
        }), 400

    # Strip data-URI prefix
    if "," in image_b64:
        image_b64 = image_b64.split(",")[1]

    # ── Decode image ───────────────────────────────────────────────────────────
    try:
        jpeg_bytes = base64.b64decode(image_b64)
        np_arr = np.frombuffer(jpeg_bytes, np.uint8)
        bgr_frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    except Exception as e:
        return jsonify({"status": "error", "message": f"Image decode failed: {e}"}), 400

    if bgr_frame is None:
        return jsonify({"status": "error", "message": "Could not decode image."}), 400

    # ── Generate face encoding ─────────────────────────────────────────────────
    rgb_frame = cv2.cvtColor(bgr_frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_frame)

    if not face_locations:
        return jsonify({
            "status": "error",
            "message": "No face detected in the image. Please try again."
        }), 400

    encodings = face_recognition.face_encodings(rgb_frame, face_locations)
    encoding_str = ",".join(map(str, encodings[0].tolist()))

    # ── Save to database ───────────────────────────────────────────────────────
    try:
        conn = get_db()
        conn.execute(
            "INSERT INTO students (name, enrollment_no, face_encoding) VALUES (?, ?, ?)",
            (name, enrollment_no, encoding_str)
        )
        conn.commit()
        conn.close()
    except sqlite3.IntegrityError:
        return jsonify({
            "status": "error",
            "message": f"Enrollment number '{enrollment_no}' already exists."
        }), 409

    return jsonify({
        "status": "success",
        "message": f"Student '{name}' registered successfully!"
    })


@app.route("/api/students", methods=["GET"])
def api_students():
    """Returns a JSON list of all registered students (without encodings)."""
    conn = get_db()
    rows = conn.execute(
        "SELECT id, name, enrollment_no, registered_at FROM students ORDER BY name"
    ).fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])


@app.route("/api/attendance", methods=["GET"])
def api_attendance():
    """Returns a JSON list of all attendance records (most recent first)."""
    conn = get_db()
    rows = conn.execute("""
        SELECT s.name, s.enrollment_no, a.date, a.time, a.smile_score
        FROM attendance a
        JOIN students s ON a.student_id = s.id
        ORDER BY a.date DESC, a.time DESC
        LIMIT 50
    """).fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])


@app.route("/api/delete_student/<int:student_id>", methods=["DELETE"])
def api_delete_student(student_id):
    """Deletes a student and their attendance records from the database."""
    conn = get_db()
    conn.execute("DELETE FROM attendance WHERE student_id = ?", (student_id,))
    conn.execute("DELETE FROM students WHERE id = ?", (student_id,))
    conn.commit()
    conn.close()
    return jsonify({"status": "success", "message": "Student deleted."})


# ── Run the server ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    # Ensure the database exists before starting
    if not os.path.exists(DB_PATH):
        print("⚠️  Database not found. Run `python setup_database.py` first.")
    else:
        print("✅ Database found.")

    print("🚀 Starting Smile Attendance System at http://127.0.0.1:5000")
    app.run(debug=True, host="0.0.0.0", port=5000)
