from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

KARNATAKA_DISTRICTS = [
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
    city = data.get("city")
    disease = data.get("condition")

    if city not in KARNATAKA_DISTRICTS:
        return jsonify({"error": "Invalid district"})

    # AQI Forecast Simulation
    today = random.randint(40, 180)
    tomorrow = max(20, today + random.randint(-15, 15))
    next48 = max(20, tomorrow + random.randint(-20, 20))

    # Suitability logic
    if today <= 50:
        status = "Safe"
        lung_state = "good"
    elif today <= 100:
        status = "Caution"
        lung_state = "moderate"
    else:
        status = "Unsafe"
        lung_state = "poor"

    # Disease-based precautions
    precautions = {
        "Asthma": [
            "Carry inhaler at all times",
            "Avoid heavy traffic areas",
            "Use N95 mask",
            "Avoid physical exertion"
        ],
        "COPD": [
            "Avoid outdoor exposure",
            "Use oxygen support if prescribed",
            "Wear double-layer mask",
            "Seek medical help if breathless"
        ],
        "Bronchitis": [
            "Cover mouth and nose",
            "Avoid cold air",
            "Use prescribed medication",
            "Limit outdoor duration"
        ],
        "Allergic Rhinitis": [
            "Wear mask",
            "Avoid dusty areas",
            "Use antihistamines if needed",
            "Wash face after returning indoors"
        ]
    }

    # AQI suitability per disease
    suitability_msg = (
        f"AQI level is {status.lower()} for {disease} patients."
        if status != "Unsafe"
        else f"AQI is not suitable for {disease} patients."
    )

    return jsonify({
        "today": today,
        "tomorrow": tomorrow,
        "next48": next48,
        "status": status,
        "lung_state": lung_state,
        "suitability": suitability_msg,
        "precautions": precautions[disease]
    })

if __name__ == "__main__":
    app.run(debug=True)
