import requests

base = "http://127.0.0.1:5000"
'''
r = requests.post(
    base + "/moods",
    data={
            "user": 123,
            "longitude": -122.4,
            "latitude": 37.8,
            "emotional_state": "sad",
        },
    )
r = requests.post(
    base + "/moods",
    data={
            "user": 123,
            "longitude": -122.4,
            "latitude": 37.8,
            "emotional_state": "happy",
        },
    )
r = requests.post(
    base + "/moods",
    data={
            "user": 123,
            "longitude": -122.4,
            "latitude": 37.8,
            "emotional_state": "happy",
        },
    )
r = requests.post(
    base + "/moods",
    data={
            "user": 456,
            "longitude": -122.4,
            "latitude": 37.8,
            "emotional_state": "happy",
        },
    )
'''
r = requests.get(base + "/moods/frequency-distribution?user_id=1")
