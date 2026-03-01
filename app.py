from flask import Flask, render_template, request, jsonify
import sqlite3
import random
import os
from datetime import datetime

app = Flask(__name__)
DB_NAME = "breathsafe.db"

# ---------------- DB CONNECTION ----------------
def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

# ---------------- CREATE TABLES ----------------
def init_db():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS districts (
        district_id INTEGER PRIMARY KEY AUTOINCREMENT,
        district_name TEXT UNIQUE
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS hospitals (
        hospital_id INTEGER PRIMARY KEY AUTOINCREMENT,
        hospital_name TEXT,
        address TEXT,
        district_id INTEGER,
        FOREIGN KEY (district_id) REFERENCES districts(district_id)
    )
    """)

    conn.commit()
    conn.close()

# ---------------- INSERT DATA ----------------
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
        cur.execute("INSERT OR IGNORE INTO districts(district_name) VALUES(?)", (d,))

    conn.commit()

    cur.execute("SELECT district_id, district_name FROM districts")
    rows = cur.fetchall()

    for r in rows:
        cur.execute("""
        INSERT OR IGNORE INTO hospitals (hospital_name, address, district_id)
        VALUES (?, ?, ?)
        """, (
            f"District Government Hospital {r['district_name']}",
            f"Main Road, {r['district_name']}, Karnataka",
            r['district_id']
        ))

        cur.execute("""
        INSERT OR IGNORE INTO hospitals (hospital_name, address, district_id)
        VALUES (?, ?, ?)
        """, (
            f"Medical College Hospital {r['district_name']}",
            f"Near Bus Stand, {r['district_name']}, Karnataka",
            r['district_id']
        ))

    conn.commit()
    conn.close()

# Initialize DB once
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

    cur.execute("SELECT district_id FROM districts WHERE district_name=?", (district,))
    row = cur.fetchone()

    if not row:
        return jsonify({"error": "District not found"})

    district_id = row["district_id"]

    cur.execute("""
    SELECT hospital_name, address
    FROM hospitals
    WHERE district_id=?
    """, (district_id,))
    hospitals = [dict(r) for r in cur.fetchall()]
    conn.close()

    # AQI Simulation
    today = random.randint(40, 200)
    tomorrow = max(30, today + random.randint(-20, 20))
    next48 = max(30, tomorrow + random.randint(-25, 25))

    if today <= 50:
        status, level = "Good", "good"
    elif today <= 100:
        status, level = "Moderate", "moderate"
    else:
        status, level = "Unhealthy", "poor"

    # Pollutants
    pm25 = round(random.uniform(10, 150), 1)
    pm10 = round(random.uniform(20, 180), 1)
    co = round(random.uniform(1, 10), 1)
    no2 = round(random.uniform(10, 120), 1)

    # Weather
    temp = random.randint(20, 35)
    humidity = random.randint(40, 85)
    wind = random.randint(5, 25)
    condition_weather = random.choice(["Clear", "Cloudy", "Hazy", "Windy"])

    # 24-Hour Trend Data
    trend = [random.randint(40, 200) for _ in range(8)]

    precautions = {
        "Asthma": ["Carry inhaler", "Wear N95 mask", "Avoid exertion"],
        "COPD": ["Avoid outdoor exposure", "Carry oxygen support", "Seek medical help"],
        "Bronchitis": ["Cover mouth", "Avoid cold air", "Limit outdoor time"],
        "Allergic Rhinitis": ["Avoid dust", "Use mask", "Wash face after return"]
    }

    return jsonify({
        "today": today,
        "tomorrow": tomorrow,
        "next48": next48,
        "status": status,
        "level": level,
        "suitability": f"AQI is {status.lower()} for {disease} patients.",
        "precautions": precautions[disease],
        "hospitals": hospitals,
        "pm25": pm25,
        "pm10": pm10,
        "co": co,
        "no2": no2,
        "temp": temp,
        "humidity": humidity,
        "wind": wind,
        "conditionWeather": condition_weather,
        "trend": trend,
        "updated": datetime.now().strftime("%I:%M:%S %p")
    })

if __name__ == "__main__":
    app.run(debug=True)
