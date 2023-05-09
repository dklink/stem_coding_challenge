from typing import Optional, Tuple, Set
from moods_app.resources.mood_capture import Mood


def validate_input(args: dict, expected_args: Set[str]) -> Optional[Tuple[str, int]]:
    """validates any of user_id, mood, latitude, and longitude that exist in args.
    Also takes a set of expected args, and ensures they are in 'args'.
    args keys/values are guaranteed to be strings.
    returns message and error code upon the first problem.
    if no problems, returns None.
    """
    for arg in expected_args:
        if arg not in args:
            return f"Missing mandatory parameter: '{arg}'", 400

    if "user_id" in args and not args["user_id"].isnumeric():
        return "'user_id' must be an integer", 400
    if "mood" in args:
        try:
            Mood[args["mood"].lower()]
        except KeyError:
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

    return None
