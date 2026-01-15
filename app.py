from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/getAQI", methods=["POST"])
def get_aqi():
    data = request.get_json()
    city = data.get("city")
    condition = data.get("condition")

    # Simulated AQI (works without API key)
    aqi = random.randint(40, 160)

    if aqi <= 50:
        advice = "Good air quality. Safe for patients."
    elif aqi <= 100:
        advice = "Moderate air quality. Avoid heavy outdoor activity."
    else:
        advice = "Poor air quality. Stay indoors."

    return jsonify({
        "aqi": aqi,
        "advice": advice
    })

if __name__ == "__main__":
    app.run()
