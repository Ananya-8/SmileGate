# 😊 SmileGate – Smile-Based Smart Attendance & Access Control System

A full-stack Python/Flask application that grants building or classroom access
only when the webcam recognises a registered student **and** detects a genuine
smile (happy emotion score ≥ 70 %).

---

## 📁 Project Structure

```
smile_attendance/
│
├── app.py                   # Flask web server (all routes & API endpoints)
├── recognize_and_attend.py  # Core recognition + emotion detection engine
├── register_student.py      # CLI registration tool (standalone script)
├── setup_database.py        # Creates the SQLite database and tables
├── requirements.txt         # Python dependencies
│
├── database/
│   └── attendance.db        # SQLite database (auto-created)
│
└── templates/
    ├── index.html           # Live scanner page
    ├── register.html        # Student registration page
    └── attendance_log.html  # Attendance log & student manager
```

---

## 🗄️ Database Schema

**Table: students**

| Column         | Type    | Description                              |
|----------------|---------|------------------------------------------|
| id             | INTEGER | Primary key (auto-increment)             |
| name           | TEXT    | Full name of the student                 |
| enrollment_no  | TEXT    | Unique enrollment / roll number          |
| face_encoding  | TEXT    | 128-float encoding stored as CSV string  |
| registered_at  | TIMESTAMP | Registration timestamp                 |

**Table: attendance**

| Column      | Type    | Description                              |
|-------------|---------|------------------------------------------|
| id          | INTEGER | Primary key (auto-increment)             |
| student_id  | INTEGER | Foreign key → students.id                |
| date        | TEXT    | Date in YYYY-MM-DD format                |
| time        | TEXT    | Time in HH:MM:SS format                  |
| smile_score | REAL    | Happy emotion confidence (0 – 100)       |

---

## ⚙️ Prerequisites

| Requirement      | Notes                                                         |
|------------------|---------------------------------------------------------------|
| Python 3.9+      | 3.10 or 3.11 recommended                                      |
| pip              | Comes with Python                                             |
| cmake            | Required by dlib (used by face_recognition)                   |
| Visual C++ tools | Windows only – install Build Tools for Visual Studio          |
| Working webcam   | Built-in or USB                                               |

### Install system dependencies

**Ubuntu / Debian**
```bash
sudo apt update
sudo apt install -y cmake build-essential libopenblas-dev liblapack-dev \
                   libx11-dev libgtk-3-dev python3-dev
```

**macOS (Homebrew)**
```bash
brew install cmake
```

**Windows**
1. Download and install [CMake](https://cmake.org/download/)
2. Install [Visual Studio Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)

---

## 🚀 Step-by-Step Setup

### Step 1 – Clone / Download the project
```bash
cd ~/Desktop
# If using git:
git clone <your-repo-url> smile_attendance
cd smile_attendance
```

### Step 2 – Create a virtual environment (recommended)
```bash
python -m venv venv

# Activate it:
# macOS / Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate
```

### Step 3 – Install Python dependencies
```bash
pip install -r requirements.txt
```
> ⚠️ `face_recognition` installs `dlib` which compiles C++ code.
> This may take 5–15 minutes. Be patient!

### Step 4 – Set up the database
```bash
python setup_database.py
```
You should see:
```
✅ Database created successfully!
   Location : database/attendance.db
   Tables   : students, attendance
```

### Step 5 – Start the Flask server
```bash
python app.py
```
You should see:
```
✅ Database found.
🚀 Starting Smile Attendance System at http://127.0.0.1:5000
```

### Step 6 – Open the browser
Navigate to: **http://127.0.0.1:5000**

---

## 🎓 How to Use

### Registering a Student (Web UI)
1. Go to **http://127.0.0.1:5000/register**
2. Allow webcam access in the browser
3. Enter the student's full name and enrollment number
4. Click **"Capture Photo"** when the face is clearly visible
5. Click **"Register Student"**

### Registering via CLI (Optional)
```bash
python register_student.py
```
Follow the on-screen prompts.

### Marking Attendance
1. Go to **http://127.0.0.1:5000** (home page)
2. Allow webcam access
3. Click **"Scan Now"** or enable **"Auto"** mode (scans every 3 seconds)
4. The system will:
   - Detect and match the face
   - Measure the smile (happy emotion) score
   - Grant or deny access

### Viewing the Attendance Log
- Go to **http://127.0.0.1:5000/attendance_log**
- Filter records with the search box
- Export to CSV with the Download button
- Delete students from the sidebar

---

## 🔧 Configuration

Open `recognize_and_attend.py` and change these values at the top:

```python
# Minimum happy emotion score (0-100) required for entry
SMILE_THRESHOLD = 70.0   # ← raise to require a bigger smile

# How strictly faces must match (lower = stricter)
FACE_MATCH_TOLERANCE = 0.50   # ← lower for tighter matching
```

---

## 🛠️ Tech Stack

| Layer            | Technology                    |
|------------------|-------------------------------|
| Web server       | Flask 3.0                     |
| Face detection   | OpenCV (Haar cascade)         |
| Face recognition | face_recognition (dlib)       |
| Emotion detection| DeepFace (facial action model)|
| Database         | SQLite 3                      |
| Frontend         | HTML + Bootstrap 5 + Vanilla JS |
| Fonts            | Syne + DM Mono (Google Fonts) |

---

## ❓ Troubleshooting

| Problem                              | Solution                                               |
|--------------------------------------|--------------------------------------------------------|
| `dlib` install fails                 | Make sure cmake and C++ build tools are installed      |
| `No face detected` on registration   | Improve lighting, face camera directly                 |
| `DeepFace` first run is slow         | It downloads model weights (~50 MB) on first use       |
| Webcam not opening                   | Close other apps using the camera; check permissions   |
| `ModuleNotFoundError`                | Ensure your virtualenv is activated before running     |

---

## 📄 License

MIT – free to use and modify for educational purposes.
