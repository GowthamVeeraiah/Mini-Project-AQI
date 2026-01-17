from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

# All Karnataka districts
DISTRICTS = [
    "Bagalkote","Ballari","Belagavi","Bengaluru Rural","Bengaluru Urban",
    "Bidar","Chamarajanagar","Chikkaballapura","Chikkamagaluru",
    "Chitradurga","Dakshina Kannada","Davanagere","Dharwad","Gadag",
    "Hassan","Haveri","Kalaburagi","Kodagu","Kolar","Koppal","Mandya",
    "Mysuru","Raichur","Ramanagara","Shivamogga","Tumakuru","Udupi",
    "Uttara Kannada","Vijayanagara","Vijayapura","Yadgir"
]

# Mock hospital database (exam-safe, realistic)
HOSPITALS = {
    "Bengaluru Urban": ["Victoria Hospital", "NIMHANS", "Bowring Hospital"],
    "Mysuru": ["KR Hospital", "Apollo BGS", "JSS Hospital"],
    "Hassan": ["HIMS Hassan", "District Hospital Hassan"],
    "Tumakuru": ["District Hospital Tumakuru", "Siddaganga Hospital"],
    "Ballari": ["VIMS Ballari", "District Hospital Ballari"],
}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/getAQI", methods=["POST"])
def get_aqi():
    data = request.get_json()
    city = data.get("city")
    disease = data.get("condition")

    if city not in DISTRICTS:
        return jsonify({"error": "Invalid district"})

    # AQI Simulation
    today = random.randint(40, 200)
    tomorrow = max(30, today + random.randint(-20, 20))
    next48 = max(30, tomorrow + random.randint(-25, 25))

    if today <= 50:
        status = "Safe"
        level = "good"
    elif today <= 100:
        status = "Caution"
        level = "moderate"
    else:
        status = "Danger"
        level = "poor"

    precautions = {
        "Asthma": ["Carry inhaler", "Wear N95 mask", "Avoid exertion"],
        "COPD": ["Avoid outdoors", "Carry oxygen support", "Seek medical help"],
        "Bronchitis": ["Cover mouth", "Avoid cold air", "Limit exposure"],
        "Allergic Rhinitis": ["Avoid dust", "Use mask", "Wash face after return"]
    }

    hospitals = HOSPITALS.get(city, [
        f"District Hospital {city}",
        f"Government Medical College {city}"
    ])

    return jsonify({
        "today": today,
        "tomorrow": tomorrow,
        "next48": next48,
        "status": status,
        "level": level,
        "suitability": f"AQI is {status.lower()} for {disease} patients.",
        "precautions": precautions[disease],
        "hospitals": hospitals
    })

if __name__ == "__main__":
    app.run(debug=True)
