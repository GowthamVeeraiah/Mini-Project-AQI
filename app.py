from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

DISTRICTS = [
    "Bagalkote","Ballari","Belagavi","Bengaluru Rural","Bengaluru Urban",
    "Bidar","Chamarajanagar","Chikkaballapura","Chikkamagaluru",
    "Chitradurga","Dakshina Kannada","Davanagere","Dharwad","Gadag",
    "Hassan","Haveri","Kalaburagi","Kodagu","Kolar","Koppal","Mandya",
    "Mysuru","Raichur","Ramanagara","Shivamogga","Tumakuru","Udupi",
    "Uttara Kannada","Vijayanagara","Vijayapura","Yadgir"
]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/getAQI", methods=["POST"])
def get_aqi():
    data = request.get_json()
    district = data.get("city")
    disease = data.get("condition")

    if district not in DISTRICTS:
        return jsonify({"error": "Invalid district"})

    # AQI simulation
    today = random.randint(40, 200)
    tomorrow = max(30, today + random.randint(-20, 20))
    next48 = max(30, tomorrow + random.randint(-25, 25))

    if today <= 50:
        status, level = "Safe", "good"
    elif today <= 100:
        status, level = "Caution", "moderate"
    else:
        status, level = "Danger", "poor"

    precautions = {
        "Asthma": ["Carry inhaler", "Wear N95 mask", "Avoid physical exertion"],
        "COPD": ["Avoid outdoor exposure", "Carry oxygen support", "Seek medical help"],
        "Bronchitis": ["Cover mouth", "Avoid cold air", "Limit outdoor time"],
        "Allergic Rhinitis": ["Avoid dust", "Use mask", "Wash face after return"]
    }

    # ✅ Guaranteed hospital list (works for ALL districts)
    hospitals = [
        {
            "name": f"District Government Hospital {district}",
            "address": f"Main Road, {district}, Karnataka"
        },
        {
            "name": f"Medical College Hospital {district}",
            "address": f"Near Bus Stand, {district}, Karnataka"
        },
        {
            "name": f"Taluk Hospital {district}",
            "address": f"Taluk Office Road, {district}, Karnataka"
        }
    ]

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
