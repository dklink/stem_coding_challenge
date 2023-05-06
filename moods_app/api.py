from flask import Flask, request

from moods_app.db_manager import DBManager
from moods_app.resources.mood import Mood

app = Flask(__name__)

MOODS_TABLE_PATH = "tables/moods.csv"
VALID_EMOTIONAL_STATES = {"happy", "sad", "neutral"}

@app.post("/moods")
def add_mood():
    user_id = request.form["user"]
    emotional_state = request.form["emotional_state"].lower()
    latitude = request.form["latitude"]
    longitude = request.form["longitude"]

    # input validation
    if not user_id.isnumeric():
        return "'user_id' must be an integer", 400
    user_id = int(user_id)
    if emotional_state not in VALID_EMOTIONAL_STATES:
        return "Invalid emotional state", 400
    try:
        latitude = float(latitude)
        longitude = float(longitude)
    except ValueError:
        return "'latitude' and 'longitude' must be numeric", 400

    # construct mood object and persist to database
    mood = Mood(
        user_id=user_id,
        longitude=longitude,
        latitude=latitude,
        emotional_state=emotional_state,
    )
    db_manager = DBManager(moods_table_path=MOODS_TABLE_PATH)
    db_manager.write_new_mood(mood=mood)

    return "Success", 201


@app.get("/moods/frequency-distribution")
def get_mood_distribution():
    user_id = request.args["user_id"]

    # input validation
    if not user_id.isnumeric():
        return "'user_id' must be an integer", 400
    user_id = int(user_id)

    # retreive all stored moods for this user
    db_manager = DBManager(moods_table_path=MOODS_TABLE_PATH)
    moods = db_manager.get_all_moods_for_user(user_id=user_id)
    if not moods:
        return "User not found", 404

    # calculate and return distribution
    distribution = {state: 0 for state in VALID_EMOTIONAL_STATES}
    for mood in moods:
        distribution[mood.emotional_state] += 1

    return distribution, 200


@app.route("/moods/nearest-happy")
def get_nearest_happy_location():
    user_id = request.args["user"]
    longitude = request.args["longitude"]
    latitude = request.args["latitude"]

    # input validation
    if not user_id.isnumeric():
        return "'user_id' must be an integer", 400
    user_id = int(user_id)
    try:
        latitude = float(latitude)
        longitude = float(longitude)
    except ValueError:
        return "'latitude' and 'longitude' must be numeric", 400

