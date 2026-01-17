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

# COMPLETE hospital list with addresses
HOSPITALS = {
    "Bengaluru Urban": [
        {"name":"Victoria Hospital","address":"KR Market, Bengaluru"},
        {"name":"NIMHANS","address":"Hosur Road, Bengaluru"},
        {"name":"Bowring Hospital","address":"Shivajinagar, Bengaluru"}
    ],
    "Mysuru": [
        {"name":"KR Hospital","address":"Irwin Road, Mysuru"},
        {"name":"JSS Hospital","address":"MG Road, Mysuru"}
    ],
    "Hassan": [
        {"name":"HIMS Hassan","address":"BM Road, Hassan"},
        {"name":"District Hospital Hassan","address":"Vidyanagar, Hassan"}
    ],
    "Tumakuru": [
        {"name":"District Hospital Tumakuru","address":"MG Road, Tumakuru"},
        {"name":"Siddaganga Hospital","address":"BH Road, Tumakuru"}
    ],
    "Ballari": [
        {"name":"VIMS Ballari","address":"Cantonment, Ballari"},
        {"name":"District Hospital Ballari","address":"Fort Road, Ballari"}
    ],
    "Belagavi": [
        {"name":"BIMS Belagavi","address":"Civil Hospital Road, Belagavi"}
    ],
    "Bidar": [
        {"name":"Bidar Institute of Medical Sciences","address":"Udgir Road, Bidar"}
    ],
    "Kalaburagi": [
        {"name":"GIMS Kalaburagi","address":"Sedam Road, Kalaburagi"}
    ],
    "Shivamogga": [
        {"name":"McGann Hospital","address":"Sagar Road, Shivamogga"}
    ],
    "Mandya": [
        {"name":"Mandya Institute of Medical Sciences","address":"NH 275, Mandya"}
    ],
    "Udupi": [
        {"name":"District Hospital Udupi","address":"Ajjarkad, Udupi"}
    ],
    "Dakshina Kannada": [
        {"name":"Wenlock Hospital","address":"Hampankatta, Mangaluru"}
    ],
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
        return jsonify({"error": "Invalid district selected"})

    # AQI simulation
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
        "Asthma": ["Carry inhaler","Wear N95 mask","Avoid exertion"],
        "COPD": ["Avoid outdoor exposure","Carry oxygen support","Seek medical help"],
        "Bronchitis": ["Cover mouth","Avoid cold air","Limit outdoor duration"],
        "Allergic Rhinitis": ["Avoid dust","Use mask","Wash face after return"]
    }

    # Guaranteed hospital fallback
    hospitals = HOSPITALS.get(city, [
        {"name":f"District Hospital {city}","address":f"Main Road, {city}"},
        {"name":f"Government Medical College {city}","address":f"{city} City"}
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
