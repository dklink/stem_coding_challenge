import requests

base = "http://127.0.0.1:5000"

r = requests.post(
    base + "/moods",
    data={
            "user_id": 123,
            "longitude": -122.4,
            "latitude": 37.8,
            "emotional_state": "sad",
        },
    )
r = requests.post(
    base + "/moods",
    data={
            "user_id": 123,
            "longitude": -130.5,
            "latitude": 90,
            "emotional_state": "happy",
        },
    )
r = requests.post(
    base + "/moods",
    data={
            "user_id": 123,
            "longitude": -120.2,
            "latitude": -45,
            "emotional_state": "happy",
        },
    )
r = requests.post(
    base + "/moods",
    data={
            "user_id": 456,
            "longitude": -122.4,
            "latitude": 37.8,
            "emotional_state": "happy",
        },
    )

# r = requests.get(base + "/moods/frequency-distribution?user_id=1")

r = requests.get(base + "/moods/nearest-happy?user_id=123&latitude=0&longitude=-120")
