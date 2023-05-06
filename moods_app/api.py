from flask import Flask, request

from moods_app.db_manager import DBManager
from moods_app.resources.mood_capture import MoodCapture, Mood
from moods_app import geo_utils

app = Flask(__name__)

MOOD_CAPTURES_TABLE_PATH = "tables/mood_captures.csv"

@app.post("/mood-captures")
def add_mood_capture():
    # validate args
    message, code = validate_input(request.form)
    if code is not None:
        return message, code

    # construct mood capture object and persist to database
    mood_capture = MoodCapture(
        user_id=int(request.form["user_id"]),
        longitude=float(request.form["longitude"]),
        latitude=float(request.form["latitude"]),
        mood=Mood(request.form["mood"].lower()),
    )
    db_manager = DBManager(mood_captures_table_path=MOOD_CAPTURES_TABLE_PATH)
    db_manager.write_new_mood_capture(mood_capture=mood_capture)

    return "Success", 201


@app.get("/mood-captures/frequency-distribution")
def get_mood_distribution():
    message, code = validate_input(request.args)
    if code is not None:
        return message, code
    user_id = int(request.args["user_id"])

    # retreive all stored moods for this user
    db_manager = DBManager(mood_captures_table_path=MOOD_CAPTURES_TABLE_PATH)
    mood_captures = db_manager.retreive_mood_captures(user_id=user_id)
    if not mood_captures:
        return "No mood captures found for this user", 404

    # calculate and return distribution
    distribution = {key.value: 0 for key in Mood}
    for capture in mood_captures:
        distribution[capture.mood.value] += 1

    return distribution, 200


@app.route("/mood-captures/nearest-happy")
def get_nearest_happy_location():
    message, code = validate_input(request.args)
    if code is not None:
        return message, code
    user_id = int(request.args["user_id"])
    longitude = float(request.args["longitude"])
    latitude = float(request.args["latitude"])

    # retreive all happy mood captures for this user
    db_manager = DBManager(mood_captures_table_path=MOOD_CAPTURES_TABLE_PATH)
    happy_captures = db_manager.retreive_mood_captures(user_id=user_id, mood=Mood.HAPPY)
    if not happy_captures:
        return "No happy mood captures found for this user", 404
    
    # find the nearest of these captures to the input lat/lon
    nearest = geo_utils.nearest_neighbor(
        target=(latitude, longitude),
        locations=[(capture.latitude, capture.longitude) for capture in happy_captures],
    )
    return {"latitude": nearest[0], "longitude": nearest[1]}, 200


def validate_input(args: dict):
    """validates any of user_id, mood, latitude, and longitude that exist in args.
    returns message and error code upon the first problem
    if no problems, return (None, None) tuple
    """
    if "user_id" in args and not args["user_id"].isnumeric():
        return "'user_id' must be an integer", 400
    if "mood" in args:
        try:
            Mood(args["mood"].lower())
        except ValueError:
            return "Provided mood is not supported", 400
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
