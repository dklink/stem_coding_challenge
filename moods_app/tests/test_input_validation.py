import pytest
from moods_app.input_validation import validate_input


def test_arg_missing():
    message, code = validate_input({}, expected_args={"argname"})
    assert message == "Missing mandatory parameter: 'argname'"
    assert code == 400


def test_user_id_ok():
    assert validate_input({"user_id": "12345"}, expected_args={"user_id"}) is None


def test_user_id_numeric():
    message, code = validate_input({"user_id": "text"}, expected_args={"user_id"})

    assert message == "'user_id' must be an integer"
    assert code == 400


def test_supported_moods():
    assert validate_input({"mood": "happy"}, expected_args={"mood"}) is None
    assert validate_input({"mood": "sad"}, expected_args={"mood"}) is None
    assert validate_input({"mood": "neutral"}, expected_args={"mood"}) is None


def test_unsupported_moods():
    message, code = validate_input({"mood": "angry"}, expected_args={"mood"})

    assert message == "Provided mood is not supported"
    assert code == 400


def test_mood_case_insensitivity():
    assert validate_input({"mood": "HaPpY"}, expected_args={"mood"}) is None


def test_lat_ok():
    assert validate_input({"latitude": "-89.99"}, expected_args={"latitude"}) is None
    assert validate_input({"latitude": "0"}, expected_args={"latitude"}) is None
    assert validate_input({"latitude": "89.99"}, expected_args={"latitude"}) is None


def test_lon_ok():
    assert validate_input({"longitude": "-179.99"}, expected_args={"longitude"}) is None
    assert validate_input({"longitude": "0"}, expected_args={"longitude"}) is None
    assert validate_input({"longitude": "179.99"}, expected_args={"longitude"}) is None


@pytest.mark.parametrize("variable", ["latitude", "longitude"])
def test_latlon_numeric(variable):
    message, code = validate_input({variable: "text"}, expected_args={variable})

    assert message == f"'{variable}' must be numeric"
    assert code == 400


@pytest.mark.parametrize("value", ["-90.01", "90.01"])
def test_lat_domain(value):
    message, code = validate_input({"latitude": value}, expected_args={"latitude"})

    assert message == "'latitude' must be in range [-90, 90]"
    assert code == 400


@pytest.mark.parametrize("value", ["-180.01", "180.01"])
def test_lon_domain(value):
    message, code = validate_input({"longitude": value}, expected_args={"longitude"})

    assert message == "'longitude' must be in range [-180, 180]"
    assert code == 400
