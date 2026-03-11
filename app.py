from flask import Flask, render_template, request, jsonify
import os
import random
import sqlite3
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "breathsafe.db")

app = Flask(__name__)

DISTRICT_HOSPITALS = {
    "Bagalkote": {
        "hospital_name": "District Hospital Bagalkote",
        "address": "Navanagar, Bagalkote, Karnataka"
    },
    "Ballari": {
        "hospital_name": "VIMS District Hospital Ballari",
        "address": "Cantonment Area, Ballari, Karnataka"
    },
    "Belagavi": {
        "hospital_name": "District Hospital Belagavi",
        "address": "Ayodhya Nagar, Belagavi, Karnataka"
    },
    "Bengaluru Urban": {
        "hospital_name": "Bowring and Lady Curzon Hospital",
        "address": "Shivajinagar, Bengaluru Urban, Karnataka"
    },
    "Bengaluru Rural": {
        "hospital_name": "District Hospital Devanahalli",
        "address": "Devanahalli, Bengaluru Rural, Karnataka"
    },
    "Bidar": {
        "hospital_name": "District Hospital Bidar",
        "address": "Near New Bus Stand, Bidar, Karnataka"
    },
    "Chamarajanagar": {
        "hospital_name": "District Hospital Chamarajanagar",
        "address": "Court Road, Chamarajanagar, Karnataka"
    },
    "Chikkaballapura": {
        "hospital_name": "District Hospital Chikkaballapura",
        "address": "KHB Colony, Chikkaballapura, Karnataka"
    },
    "Chikkamagaluru": {
        "hospital_name": "District McGann Hospital",
        "address": "M G Road, Chikkamagaluru, Karnataka"
    },
    "Chitradurga": {
        "hospital_name": "District Hospital Chitradurga",
        "address": "Holalkere Road, Chitradurga, Karnataka"
    },
    "Dakshina Kannada": {
        "hospital_name": "Wenlock District Hospital",
        "address": "Hampankatta, Mangaluru, Karnataka"
    },
    "Davanagere": {
        "hospital_name": "District Hospital Davanagere",
        "address": "Hadadi Road, Davanagere, Karnataka"
    },
    "Dharwad": {
        "hospital_name": "District Hospital Dharwad",
        "address": "College Road, Dharwad, Karnataka"
    },
    "Gadag": {
        "hospital_name": "District Hospital Gadag",
        "address": "K C Rani Road, Gadag, Karnataka"
    },
    "Hassan": {
        "hospital_name": "Hassan Institute District Hospital",
        "address": "B M Road, Hassan, Karnataka"
    },
    "Haveri": {
        "hospital_name": "District Hospital Haveri",
        "address": "PB Road, Haveri, Karnataka"
    },
    "Kalaburagi": {
        "hospital_name": "District Hospital Kalaburagi",
        "address": "Sedam Road, Kalaburagi, Karnataka"
    },
    "Kodagu": {
        "hospital_name": "District Hospital Madikeri",
        "address": "General Thimmaiah Circle, Madikeri, Karnataka"
    },
    "Kolar": {
        "hospital_name": "District Hospital Kolar",
        "address": "Tamaka Road, Kolar, Karnataka"
    },
    "Koppal": {
        "hospital_name": "District Hospital Koppal",
        "address": "Hospet Road, Koppal, Karnataka"
    },
    "Mandya": {
        "hospital_name": "District Hospital Mandya",
        "address": "M C Road, Mandya, Karnataka"
    },
    "Mysuru": {
        "hospital_name": "K R Hospital Mysuru",
        "address": "Sayyaji Rao Road, Mysuru, Karnataka"
    },
    "Raichur": {
        "hospital_name": "District Hospital Raichur",
        "address": "Station Road, Raichur, Karnataka"
    },
    "Ramanagara": {
        "hospital_name": "District Hospital Ramanagara",
        "address": "Ijoor, Ramanagara, Karnataka"
    },
    "Shivamogga": {
        "hospital_name": "McGann District Hospital Shivamogga",
        "address": "Sagar Road, Shivamogga, Karnataka"
    },
    "Tumakuru": {
        "hospital_name": "District Hospital Tumakuru",
        "address": "B H Road, Tumakuru, Karnataka"
    },
    "Udupi": {
        "hospital_name": "District Hospital Udupi",
        "address": "Ajjarkad, Udupi, Karnataka"
    },
    "Uttara Kannada": {
        "hospital_name": "District Hospital Karwar",
        "address": "Civil Hospital Road, Karwar, Karnataka"
    },
    "Vijayanagara": {
        "hospital_name": "District Hospital Hosapete",
        "address": "Hosapete, Vijayanagara, Karnataka"
    },
    "Vijayapura": {
        "hospital_name": "District Hospital Vijayapura",
        "address": "Solapur Road, Vijayapura, Karnataka"
    },
    "Yadgir": {
        "hospital_name": "District Hospital Yadgir",
        "address": "Shahapur Road, Yadgir, Karnataka"
    }
}

DISTRICT_CENTERS = [
    "Bagalkote", "Ballari", "Belagavi", "Bengaluru Urban", "Bengaluru Rural",
    "Bidar", "Chamarajanagar", "Chikkaballapura", "Chikkamagaluru",
    "Chitradurga", "Dakshina Kannada", "Davanagere", "Dharwad", "Gadag",
    "Hassan", "Haveri", "Kalaburagi", "Kodagu", "Kolar", "Koppal", "Mandya",
    "Mysuru", "Raichur", "Ramanagara", "Shivamogga", "Tumakuru", "Udupi",
    "Uttara Kannada", "Vijayanagara", "Vijayapura", "Yadgir"
]


def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS districts(
            district_id INTEGER PRIMARY KEY AUTOINCREMENT,
            district_name TEXT UNIQUE
        )
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS hospitals(
            hospital_id INTEGER PRIMARY KEY AUTOINCREMENT,
            hospital_name TEXT,
            address TEXT,
            district_id INTEGER,
            FOREIGN KEY(district_id) REFERENCES districts(district_id)
        )
        """
    )

    conn.commit()
    conn.close()


def seed_data():
    conn = get_db()
    cur = conn.cursor()

    for district in DISTRICT_CENTERS:
        cur.execute(
            "INSERT OR IGNORE INTO districts(district_name) VALUES(?)",
            (district,),
        )
    conn.commit()

    cur.execute("SELECT district_id, district_name FROM districts")
    rows = cur.fetchall()

    for row in rows:
        district_name = row["district_name"]
        hospital = DISTRICT_HOSPITALS.get(
            district_name,
            {
                "hospital_name": f"District Hospital {district_name}",
                "address": f"Main Road, {district_name}, Karnataka",
            },
        )

        cur.execute(
            """
            INSERT OR IGNORE INTO hospitals(hospital_name, address, district_id)
            VALUES(?, ?, ?)
            """,
            (hospital["hospital_name"], hospital["address"], row["district_id"]),
        )

    conn.commit()
    conn.close()


if not os.path.exists(DB_NAME):
    init_db()
    seed_data()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/health")
def health():
    return {"status": "ok"}


@app.route("/getAQI", methods=["POST"])
def get_aqi():
    data = request.get_json(silent=True) or {}
    district = data.get("city")
    disease = data.get("condition")

    if not district:
        return jsonify({"error": "District is required"}), 400

    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT district_id FROM districts WHERE district_name=?", (district,))
    row = cur.fetchone()

    if not row:
        conn.close()
        return jsonify({"error": "District not found"}), 404

    district_id = row["district_id"]

    cur.execute(
        "SELECT hospital_name, address FROM hospitals WHERE district_id=?",
        (district_id,),
    )
    hospitals = [dict(result) for result in cur.fetchall()]
    conn.close()

    today = random.randint(40, 200)
    next24 = [random.randint(40, 200) for _ in range(8)]

    if today <= 50:
        status, level = "Good", "good"
    elif today <= 100:
        status, level = "Moderate", "moderate"
    else:
        status, level = "Unhealthy", "poor"

    precautions = {
        "Asthma": [
            "Carry inhaler at all times",
            "Avoid outdoor exercise",
            "Use N95 mask",
            "Stay hydrated",
        ],
        "COPD": [
            "Limit outdoor exposure",
            "Avoid traffic areas",
            "Use oxygen support if prescribed",
            "Consult doctor if breathlessness increases",
        ],
        "Bronchitis": [
            "Avoid cold air",
            "Wear protective mask",
            "Avoid dusty areas",
            "Take steam inhalation",
        ],
        "Allergic Rhinitis": [
            "Avoid pollen and dust",
            "Wash face after outdoor exposure",
            "Use antihistamines if prescribed",
            "Keep windows closed during high pollution",
        ],
    }

    return jsonify(
        {
            "today": today,
            "status": status,
            "level": level,
            "trend": next24,
            "pm25": random.randint(10, 150),
            "pm10": random.randint(20, 180),
            "co": random.randint(1, 10),
            "no2": random.randint(10, 120),
            "temp": random.randint(20, 35),
            "humidity": random.randint(40, 85),
            "wind": random.randint(5, 25),
            "conditionWeather": random.choice(["Clear", "Cloudy", "Hazy"]),
            "hospitals": hospitals,
            "precautions": precautions.get(disease, []),
            "updated": datetime.now().strftime("%I:%M %p"),
        }
    )


if __name__ == "__main__":
    app.run(debug=True)
