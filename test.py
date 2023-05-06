import requests

base = "http://127.0.0.1:5000"

r1 = requests.post(
    base + "/mood-captures",
    data={
            "user_id": 123,
            "longitude": -122.4,
            "latitude": 37.8,
            "mood": "sad",
        },
    )
r2 = requests.post(
    base + "/mood-captures",
    data={
            "user_id": 123,
            "longitude": -130.5,
            "latitude": 90,
            "mood": "happy",
        },
    )
r3 = requests.post(
    base + "/mood-captures",
    data={
            "user_id": 123,
            "longitude": -120.2,
            "latitude": -45,
            "mood": "happy",
        },
    )
r4 = requests.post(
    base + "/mood-captures",
    data={
            "user_id": 456,
            "longitude": -122.4,
            "latitude": 37.8,
            "mood": "happy",
        },
    )


r5 = requests.get(base + "/mood-captures/frequency-distribution?user_id=123")

r6 = requests.get(base + "/mood-captures/nearest-happy?user_id=123&latitude=0&longitude=-120")
