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
    condition = data.get("condition")

    if city not in KARNATAKA_DISTRICTS:
        return jsonify({"error": "Invalid district"})

    # Simulated AQI values
    today_aqi = random.randint(40, 180)
    tomorrow_aqi = max(20, today_aqi + random.randint(-15, 15))
    next_48_aqi = max(20, tomorrow_aqi + random.randint(-20, 20))

    # Suitability logic
    if today_aqi <= 50:
        suitability = "Suitable"
        advice = f"Air quality is good. Safe for {condition} patients."
    elif today_aqi <= 100:
        suitability = "Moderately Suitable"
        advice = f"Moderate air quality. {condition} patients should avoid prolonged outdoor activity."
    else:
        suitability = "Not Suitable"
        advice = f"Poor air quality. {condition} patients are advised to stay indoors."

    return jsonify({
        "today": today_aqi,
        "tomorrow": tomorrow_aqi,
        "next48": next_48_aqi,
        "suitability": suitability,
        "advice": advice
    })

if __name__ == "__main__":
    app.run(debug=True)
