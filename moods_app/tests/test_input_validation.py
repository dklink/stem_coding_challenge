import pytest
from moods_app.input_validation import validate_input

def test_user_id_ok():
    assert validate_input({"user_id": "12345"}) is None

def test_user_id_numeric():
    message, code = validate_input({"user_id": "text"})

    assert message == "'user_id' must be an integer"
    assert code == 400

def test_supported_moods():
    assert validate_input({"mood": "happy"}) is None
    assert validate_input({"mood": "sad"}) is None
    assert validate_input({"mood": "neutral"}) is None

def test_unsupported_moods():
    message, code = validate_input({"mood": "angry"})

    assert message == "Provided mood is not supported"
    assert code == 400

def test_mood_case_insensitivity():
    assert validate_input({"mood": "HaPpY"}) is None


def test_lat_ok():
    assert validate_input({"latitude": "-89.99"}) is None
    assert validate_input({"latitude": "0"}) is None
    assert validate_input({"latitude": "89.99"}) is None

def test_lon_ok():
    assert validate_input({"longitude": "-179.99"}) is None
    assert validate_input({"longitude": "0"}) is None
    assert validate_input({"longitude": "179.99"}) is None

@pytest.mark.parametrize("variable", ["latitude", "longitude"])
def test_latlon_numeric(variable):
    message, code = validate_input({variable: "text"})

    assert message == f"'{variable}' must be numeric"
    assert code == 400

@pytest.mark.parametrize("value", ["-90.01", "90.01"])
def test_lat_domain(value):
    message, code = validate_input({"latitude": value})

    assert message == "'latitude' must be in range [-90, 90]"
    assert code == 400

@pytest.mark.parametrize("value", ["-180.01", "180.01"])
def test_lon_domain(value):
    message, code = validate_input({"longitude": value})

    assert message == "'longitude' must be in range [-180, 180]"
    assert code == 400
