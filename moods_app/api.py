from flask import Flask, request

from moods_app.db_manager import DBManager
from moods_app.resources.mood import Mood
from moods_app import geo_utils

app = Flask(__name__)

MOODS_TABLE_PATH = "tables/moods.csv"
VALID_EMOTIONAL_STATES = {"happy", "sad", "neutral"}

@app.post("/moods")
def add_mood():
    # validate args
    message, code = validate_input(request.form)
    if code is not None:
        return message, code

    # construct mood object and persist to database
    mood = Mood(
        user_id=int(request.form["user_id"]),
        longitude=float(request.form["longitude"]),
        latitude=float(request.form["latitude"]),
        emotional_state=request.form["emotional_state"].lower(),
    )
    db_manager = DBManager(moods_table_path=MOODS_TABLE_PATH)
    db_manager.write_new_mood(mood=mood)

    return "Success", 201


@app.get("/moods/frequency-distribution")
def get_mood_distribution():
    message, code = validate_input(request.args)
    if code is not None:
        return message, code
    user_id = int(request.args["user_id"])

    # retreive all stored moods for this user
    db_manager = DBManager(moods_table_path=MOODS_TABLE_PATH)
    moods = db_manager.retreive_moods(user_id=user_id)
    if not moods:
        return "No moods found for this user", 404

    # calculate and return distribution
    distribution = {state: 0 for state in VALID_EMOTIONAL_STATES}
    for mood in moods:
        distribution[mood.emotional_state] += 1

    return distribution, 200


@app.route("/moods/nearest-happy")
def get_nearest_happy_location():
    message, code = validate_input(request.args)
    if code is not None:
        return message, code
    user_id = int(request.args["user_id"])
    longitude = float(request.args["longitude"])
    latitude = float(request.args["latitude"])

    # retreive all happy moods for this user
    db_manager = DBManager(moods_table_path=MOODS_TABLE_PATH)
    happy_moods = db_manager.retreive_moods(user_id=user_id, emotional_state="happy")
    if not happy_moods:
        return "No happy moods found for this user", 404
    
    # find the nearest of these moods to the input lat/lon
    nearest = geo_utils.nearest_neighbor(
        target=(latitude, longitude),
        locations=[(mood.latitude, mood.longitude) for mood in happy_moods],
    )
    return {"latitude": nearest[0], "longitude": nearest[1]}, 200


def validate_input(args: dict):
    """validates any of user_id, emotional_state, latitude, and longitude that exist in args.
    returns message and error code upon the first problem
    if no problems, return (None, None) tuple
    """
    if "user_id" in args and not args["user_id"].isnumeric():
        return "'user_id' must be an integer", 400
    if "emotional_state" in args and args["emotional_state"].lower() not in VALID_EMOTIONAL_STATES:
        return "Invalid emotional state", 400
    if "latitude" in args:
        try:
            latitude = float(args["latitude"])
        except ValueError:
            return "'latitude' must be numeric", 400
        if not (-90 <= latitude <= 90):
            return "latitude must be in range [-90, 90]", 400
    if "longitude" in args:
        try:
            longitude = float(args["longitude"])
        except ValueError:
            return "'longitude' must be numeric", 400
        if not (-180 <= longitude <= 180):
            return "longitude must be in range [-180, 180]", 400
    
    return None, None
