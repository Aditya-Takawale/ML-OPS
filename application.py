import pickle
import numpy as np
from flask import Flask, request, render_template
from pymongo import MongoClient

app = Flask(__name__)

# Load the trained LightGBM model
model_path = "artifacts/models/lgbm_model.pkl"
with open(model_path, "rb") as file:
    model = pickle.load(file)

# Connect to MongoDB
MONGO_URI = "mongodb://localhost:27017"
client = MongoClient(MONGO_URI)
db = client["hotel_reservation"]  # Database name
collection = db["predictions"]     # Collection name

@app.route("/", methods=["GET", "POST"])
def predict():
    prediction = None

    if request.method == "POST":
        try:
            # Get user input from the form
            lead_time = int(request.form["lead_time"])
            no_of_special_requests = int(request.form["no_of_special_request"])
            avg_price_per_room = float(request.form["avg_price_per_room"])
            arrival_month = int(request.form["arrival_month"])
            arrival_date = int(request.form["arrival_date"])
            market_segment_type = int(request.form["market_segment_type"])
            no_of_week_nights = int(request.form["no_of_week_nights"])
            no_of_weekend_nights = int(request.form["no_of_weekend_nights"])
            type_of_meal_plan = int(request.form["type_of_meal_plan"])
            room_type_reserved = int(request.form["room_type_reserved"])

            # Prepare input for model
            features = np.array([[lead_time, no_of_special_requests, avg_price_per_room,
                                  arrival_month, arrival_date, market_segment_type,
                                  no_of_week_nights, no_of_weekend_nights, type_of_meal_plan,
                                  room_type_reserved]])

            # Make prediction
            prediction = model.predict(features)[0]

            # Store data in MongoDB
            data_entry = {
                "lead_time": lead_time,
                "no_of_special_requests": no_of_special_requests,
                "avg_price_per_room": avg_price_per_room,
                "arrival_month": arrival_month,
                "arrival_date": arrival_date,
                "market_segment_type": market_segment_type,
                "no_of_week_nights": no_of_week_nights,
                "no_of_weekend_nights": no_of_weekend_nights,
                "type_of_meal_plan": type_of_meal_plan,
                "room_type_reserved": room_type_reserved,
                "prediction": int(prediction)  # Convert NumPy int to Python int
            }
            collection.insert_one(data_entry)
            print("✅ Data saved to MongoDB:", data_entry)

        except Exception as e:
            print("❌ Error:", str(e))
            prediction = None

    return render_template("index.html", prediction=prediction)

if __name__ == "__main__":
    app.run(debug=True)
