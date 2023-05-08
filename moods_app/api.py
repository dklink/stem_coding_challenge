from flask import Flask, request

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from moods_app.resources.mood_capture import MoodCapture, Mood
from moods_app.resources.user import User
from moods_app.resources.base import Base
from moods_app import utils
from moods_app import auth

from moods_app.database import init_db



def create_app(test_config=None):
    app = Flask(__name__)
    if test_config is not None:
        app.config.update(test_config)

    # initialize database engine
    if app.config["TESTING"]:
        session = app.config["TEST_DB_SESSION"]
    else:
        init_db()
        from database import db_session
        session = db_session

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        session.remove()
    
    ### ENDPOINTS ###
    @app.post("/users")
    def add_user():
        """adds a new user to the database, returning the new user's id and api key"""
        new_user = User.create_new_user(session=session)
        return {
            "user_id": new_user.id,
            "api_key": new_user.api_key,
        }

    @app.post("/mood-captures")
    def add_mood_capture():
        # validate args
        message, code = validate_input(request.form)
        if code is not None:
            return message, code
        user_id = int(request.form["user_id"])
        
        # authenticate user
        auth_error = auth.authenticate_user(
            user_id=user_id,
            api_key=request.form["api_key"],
            session=session,
        )

        # construct mood capture object and persist to database
        mood_capture = MoodCapture.create_new_mood_capture(
            user_id=user_id,
            longitude=float(request.form["longitude"]),
            latitude=float(request.form["latitude"]),
            mood=Mood[request.form["mood"].lower()],
            session=session,
        )
    
        return {
            "mood_capture_id": mood_capture.id,
            "user_id": mood_capture.user_id,
            "latitude": mood_capture.latitude,
            "longitude": mood_capture.longitude,
            "mood": mood_capture.mood.name,
        }, 201


    @app.get("/mood-captures/frequency-distribution")
    def get_mood_distribution():
        message, code = validate_input(request.args)
        if code is not None:
            return message, code
        user_id = int(request.args["user_id"])

        # retreive all stored moods for this user
        moods = MoodCapture.get_all_moods_for_user(user_id=user_id, session=session)
        if not moods:
            return "No mood captures found for this user", 404

        # calculate and return distribution
        distribution = {key.name: 0 for key in Mood}
        for mood in moods:
            distribution[mood.name] += 1

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
        happy_locations = MoodCapture.get_locations_of_happy_moods_for_user(user_id=user_id, session=session)
        if not happy_locations:
            return "No happy mood captures found for this user", 404

        # find the nearest of these captures to the input lat/lon
        nearest = utils.nearest_neighbor_latlon(
            target=(latitude, longitude),
            locations=happy_locations,
        )

        return {"latitude": nearest[0], "longitude": nearest[1]}, 200

    return app



def validate_input(args: dict):
    """validates any of user_id, mood, latitude, and longitude that exist in args.
    returns message and error code upon the first problem
    if no problems, returns (None, None) tuple
    """
    if "user_id" in args and not args["user_id"].isnumeric():
        return "'user_id' must be an integer", 400
    if "mood" in args:
        try:
            Mood[args["mood"].lower()]
        except ValueError:
            return "Provided mood is not supported", 400
    if "latitude" in args:
        try:
            latitude = float(args["latitude"])
        except ValueError:
            return "'latitude' must be numeric", 400
        if not (-90 <= latitude <= 90):
            return "'latitude' must be in range [-90, 90]", 400
    if "longitude" in args:
        try:
            longitude = float(args["longitude"])
        except ValueError:
            return "'longitude' must be numeric", 400
        if not (-180 <= longitude <= 180):
            return "'longitude' must be in range [-180, 180]", 400
    if "api_key" in args and not isinstance(args["api_key"], str):
        return "'api_key' must be a string", 400

    return None, None
