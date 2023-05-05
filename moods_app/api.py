from flask import Flask, request

from db_manager import DBManager
from resources.mood import Mood

app = Flask(__name__)


@app.post("/moods")
def add_mood():
    user_id = request.form["user"]
    emotional_state = request.form["emotional_state"]
    longitude = request.form["longitude"]
    latitude = request.form["latitude"]

    # value checking goes here - not implemented

    # create mood object
    mood = Mood(
        user_id=user_id,
        longitude=longitude,
        latitude=latitude,
        emotional_state=emotional_state,
    )

    # persist mood to database
    db_manager = DBManager()
    db_manager.write_mood(mood=mood)

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
