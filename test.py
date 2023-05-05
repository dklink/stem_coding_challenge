import requests

base = "http://127.0.0.1:5000"

r = requests.post(
    base + "/moods",
    data={
            "user": 123,
            "longitude": -122.4,
            "latitude": 37.8,
            "emotional_state": "sad",
        },
    )
#r = requests.get(base + "/moods/frequency-distribution?user=123")

print(r)
