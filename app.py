from flask import Flask, render_template, request, jsonify
import sqlite3
import random
import os
from datetime import# ---------------- IMPORT REQUIRED LIBRARIES ----------------
# Flask → Web framework
# render_template → To load HTML file
# request → To receive JSON data from frontend
# jsonify → To send JSON response back
from flask import Flask, render_template, request, jsonify

# sqlite3 → Lightweight database for storing districts & hospitals
import sqlite3

# random → Used temporarily to simulate AQI data (Replace with real API later)
import random

# os → Used to check if database already exists
import os

# datetime → Used to show last updated time
from datetime import datetime


# ---------------- INITIALIZE FLASK APP ----------------
app = Flask(__name__)

# Database file name
DB_NAME = "breathsafe.db"


# ---------------- DATABASE CONNECTION FUNCTION ----------------
def get_db():
    """
    Creates and returns a database connection.
    row_factory allows us to access columns by name instead of index.
    """
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


# ---------------- DATABASE INITIALIZATION ----------------
def init_db():
    """
    Creates required tables if they do not exist.
    This ensures first-time execution sets up everything automatically.
    """
    conn = get_db()
    cur = conn.cursor()

    # District Table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS districts(
        district_id INTEGER PRIMARY KEY AUTOINCREMENT,
        district_name TEXT UNIQUE
    )
    """)

    # Hospital Table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS hospitals(
        hospital_id INTEGER PRIMARY KEY AUTOINCREMENT,
        hospital_name TEXT,
        address TEXT,
        district_id INTEGER,
        FOREIGN KEY(district_id) REFERENCES districts(district_id)
    )
    """)

    conn.commit()
    conn.close()


# ---------------- SEED INITIAL DATA ----------------
def seed_data():
    """
    Inserts Karnataka districts and one dummy hospital per district.
    This can later be replaced with real hospital data from government APIs.
    """
    conn = get_db()
    cur = conn.cursor()

    districts = [
        "Bagalkote","Ballari","Belagavi","Bengaluru Urban","Bengaluru Rural",
        "Bidar","Chamarajanagar","Chikkaballapura","Chikkamagaluru",
        "Chitradurga","Dakshina Kannada","Davanagere","Dharwad","Gadag",
        "Hassan","Haveri","Kalaburagi","Kodagu","Kolar","Koppal","Mandya",
        "Mysuru","Raichur","Ramanagara","Shivamogga","Tumakuru","Udupi",
        "Uttara Kannada","Vijayanagara","Vijayapura","Yadgir"
    ]

    # Insert districts safely (IGNORE avoids duplicate errors)
    for d in districts:
        cur.execute("INSERT OR IGNORE INTO districts(district_name) VALUES(?)",(d,))
    conn.commit()

    # Fetch inserted districts to link hospitals
    cur.execute("SELECT district_id,district_name FROM districts")
    rows = cur.fetchall()

    # Insert one sample hospital per district
    for r in rows:
        cur.execute("""
        INSERT OR IGNORE INTO hospitals(hospital_name,address,district_id)
        VALUES(?,?,?)
        """,(
            f"District General Hospital {r['district_name']}",
            f"Main Road, {r['district_name']}, Karnataka",
            r["district_id"]
        ))

    conn.commit()
    conn.close()


# ---------------- AUTO DATABASE SETUP ----------------
# If database does not exist → create and seed it
if not os.path.exists(DB_NAME):
    init_db()
    seed_data()


# ---------------- ROUTES ----------------

# Home route → loads frontend page
@app.route("/")
def home():
    return render_template("index.html")


# AQI API Route → Receives city and disease condition
@app.route("/getAQI", methods=["POST"])
def get_aqi():
    """
    This function:
    1. Receives district & disease from frontend
    2. Fetches hospitals for that district
    3. Simulates AQI data (temporary)
    4. Returns structured JSON response
    """

    # Receive JSON data from frontend
    data = request.get_json()
    district = data.get("city")
    disease = data.get("condition")

    conn = get_db()
    cur = conn.cursor()

    # Find district ID
    cur.execute("SELECT district_id FROM districts WHERE district_name=?",(district,))
    row = cur.fetchone()

    if not row:
        return jsonify({"error":"District not found"})

    district_id = row["district_id"]

    # Fetch hospitals for selected district
    cur.execute("SELECT hospital_name,address FROM hospitals WHERE district_id=?",(district_id,))
    hospitals = [dict(r) for r in cur.fetchall()]
    conn.close()

    # ---------------- SIMULATED AQI DATA ----------------
    # Replace this entire section with real AQI API integration later
    today = random.randint(40,200)
    next24 = [random.randint(40,200) for _ in range(8)]

    # AQI Classification Logic
    if today <= 50:
        status,level="Good","good"
    elif today <=100:
        status,level="Moderate","moderate"
    else:
        status,level="Unhealthy","poor"

    # Disease-based precaution dictionary
    precautions = {
        "Asthma":[
            "Carry inhaler at all times",
            "Avoid outdoor exercise",
            "Use N95 mask",
            "Stay hydrated"
        ],
        "COPD":[
            "Limit outdoor exposure",
            "Avoid traffic areas",
            "Use oxygen support if prescribed",
            "Consult doctor if breathlessness increases"
        ],
        "Bronchitis":[
            "Avoid cold air",
            "Wear protective mask",
            "Avoid dusty areas",
            "Take steam inhalation"
        ],
        "Allergic Rhinitis":[
            "Avoid pollen & dust",
            "Wash face after outdoor exposure",
            "Use antihistamines if prescribed",
            "Keep windows closed during high pollution"
        ]
    }

    # Final JSON response sent to frontend
    return jsonify({
        "today":today,
        "status":status,
        "level":level,
        "trend":next24,
        "pm25":random.randint(10,150),
        "pm10":random.randint(20,180),
        "co":random.randint(1,10),
        "no2":random.randint(10,120),
        "temp":random.randint(20,35),
        "humidity":random.randint(40,85),
        "wind":random.randint(5,25),
        "conditionWeather":random.choice(["Clear","Cloudy","Hazy"]),
        "hospitals":hospitals,
        "precautions":precautions.get(disease,[]),
        "updated":datetime.now().strftime("%I:%M %p")
    })


# Run the Flask app
if __name__=="__main__":
    app.run(debug=True) datetime

app = Flask(__name__)
DB_NAME = "breathsafe.db"

# ---------------- DATABASE ----------------
def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS districts(
        district_id INTEGER PRIMARY KEY AUTOINCREMENT,
        district_name TEXT UNIQUE
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS hospitals(
        hospital_id INTEGER PRIMARY KEY AUTOINCREMENT,
        hospital_name TEXT,
        address TEXT,
        district_id INTEGER,
        FOREIGN KEY(district_id) REFERENCES districts(district_id)
    )
    """)

    conn.commit()
    conn.close()

def seed_data():
    conn = get_db()
    cur = conn.cursor()

    districts = [
        "Bagalkote","Ballari","Belagavi","Bengaluru Urban","Bengaluru Rural",
        "Bidar","Chamarajanagar","Chikkaballapura","Chikkamagaluru",
        "Chitradurga","Dakshina Kannada","Davanagere","Dharwad","Gadag",
        "Hassan","Haveri","Kalaburagi","Kodagu","Kolar","Koppal","Mandya",
        "Mysuru","Raichur","Ramanagara","Shivamogga","Tumakuru","Udupi",
        "Uttara Kannada","Vijayanagara","Vijayapura","Yadgir"
    ]

    for d in districts:
        cur.execute("INSERT OR IGNORE INTO districts(district_name) VALUES(?)",(d,))
    conn.commit()

    cur.execute("SELECT district_id,district_name FROM districts")
    rows = cur.fetchall()

    for r in rows:
        cur.execute("""
        INSERT OR IGNORE INTO hospitals(hospital_name,address,district_id)
        VALUES(?,?,?)
        """,(
            f"District General Hospital {r['district_name']}",
            f"Main Road, {r['district_name']}, Karnataka",
            r["district_id"]
        ))

    conn.commit()
    conn.close()

if not os.path.exists(DB_NAME):
    init_db()
    seed_data()

# ---------------- ROUTES ----------------
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/getAQI", methods=["POST"])
def get_aqi():
    data = request.get_json()
    district = data.get("city")
    disease = data.get("condition")

    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT district_id FROM districts WHERE district_name=?",(district,))
    row = cur.fetchone()

    if not row:
        return jsonify({"error":"District not found"})

    district_id = row["district_id"]

    cur.execute("SELECT hospital_name,address FROM hospitals WHERE district_id=?",(district_id,))
    hospitals = [dict(r) for r in cur.fetchall()]
    conn.close()

    today = random.randint(40,200)
    next24 = [random.randint(40,200) for _ in range(8)]

    if today <= 50:
        status,level="Good","good"
    elif today <=100:
        status,level="Moderate","moderate"
    else:
        status,level="Unhealthy","poor"

    precautions = {
        "Asthma":[
            "Carry inhaler at all times",
            "Avoid outdoor exercise",
            "Use N95 mask",
            "Stay hydrated"
        ],
        "COPD":[
            "Limit outdoor exposure",
            "Avoid traffic areas",
            "Use oxygen support if prescribed",
            "Consult doctor if breathlessness increases"
        ],
        "Bronchitis":[
            "Avoid cold air",
            "Wear protective mask",
            "Avoid dusty areas",
            "Take steam inhalation"
        ],
        "Allergic Rhinitis":[
            "Avoid pollen & dust",
            "Wash face after outdoor exposure",
            "Use antihistamines if prescribed",
            "Keep windows closed during high pollution"
        ]
    }

    return jsonify({
        "today":today,
        "status":status,
        "level":level,
        "trend":next24,
        "pm25":random.randint(10,150),
        "pm10":random.randint(20,180),
        "co":random.randint(1,10),
        "no2":random.randint(10,120),
        "temp":random.randint(20,35),
        "humidity":random.randint(40,85),
        "wind":random.randint(5,25),
        "conditionWeather":random.choice(["Clear","Cloudy","Hazy"]),
        "hospitals":hospitals,
        "precautions":precautions.get(disease,[]),
        "updated":datetime.now().strftime("%I:%M %p")
    })

if __name__=="__main__":
    app.run(debug=True)
