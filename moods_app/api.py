from flask import Flask, request

from moods_app.db_manager import DBManager
from moods_app.resources.mood import Mood

app = Flask(__name__)

MOODS_TABLE_PATH = "tables/moods.csv"


@app.post("/moods")
def add_mood():
    user_id = int(request.form["user"])
    emotional_state = request.form["emotional_state"]
    longitude = float(request.form["longitude"])
    latitude = float(request.form["latitude"])

    # value checking goes here - not implemented

    # create mood object
    mood = Mood(
        user_id=user_id,
        longitude=longitude,
        latitude=latitude,
        emotional_state=emotional_state,
    )

    # persist mood to database
    db_manager = DBManager(moods_table_path=MOODS_TABLE_PATH)
    db_manager.write_new_mood(mood=mood)

    return "Success", 201


@app.get("/moods/frequency_distribution")
def get_mood_distribution():
    user_id = request.args["user"]
    return f"Hello, user {user_id}!"


@app.route("/moods/nearest-happy")
def get_nearest_happy_location():
    user_id = request.args["user"]
    longitude = request.args["longitude"]
    latitude = request.args["latitude"]
