from flask import Flask, request

from moods_app.resources.mood_capture import MoodCapture, Mood
from moods_app.resources.user import User
from moods_app.resources.base import Base
from moods_app import utils
from moods_app import auth
from moods_app.database import get_filesystem_db_engine, init_db, get_scoped_session
from moods_app.input_validation import validate_input


def create_app(test_config=None):
    app = Flask(__name__)
    if test_config is not None:
        app.config.update(test_config)

    # initialize database engine
    if app.config["TESTING"]:
        session = app.config["TEST_DB_SESSION"]
    else:
        engine = get_filesystem_db_engine()
        init_db(engine)
        session = get_scoped_session(engine)

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
        input_error = validate_input(request.form, expected_args={"user_id", "latitude", "longitude", "mood"})
        if input_error is not None:
            return input_error  # message, code
        user_id = int(request.form["user_id"])
        
        # authenticate user
        auth_error = auth.authenticate_user(
            user_id=user_id,
            api_key=request.headers.get("x-api-key"),
            session=session,
        )
        if auth_error is not None:
            return auth_error  # message, code

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
        input_error = validate_input(request.args, expected_args={"user_id"})
        if input_error is not None:
            return input_error  # message, code
        user_id = int(request.args["user_id"])

        # authenticate
        auth_error = auth.authenticate_user(
            user_id=user_id,
            api_key=request.headers.get("x-api-key"),
            session=session,
        )
        if auth_error is not None:
            return auth_error[0], auth_error[1]  # message, code

        # retreive all stored moods for this user
        moods = MoodCapture.get_all_moods_for_user(user_id=user_id, session=session)
        if not moods:
            return "No mood captures found for this user", 404

        return utils.calculate_mood_distribution(moods), 200


    @app.route("/mood-captures/nearest-happy")
    def get_nearest_happy_location():
        input_error = validate_input(request.args, expected_args={"user_id", "latitude", "longitude"})
        if input_error is not None:
            return input_error  # message, code
        user_id = int(request.args["user_id"])
        longitude = float(request.args["longitude"])
        latitude = float(request.args["latitude"])

        # authenticate
        auth_error = auth.authenticate_user(
            user_id=user_id,
            api_key=request.headers.get("x-api-key"),
            session=session,
        )
        if auth_error is not None:
            return auth_error[0], auth_error[1]  # message, code

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
