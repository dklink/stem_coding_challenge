import requests

base = "http://127.0.0.1:5000"


print("First, we'll create a new user, with POST /users.")
response1 = requests.post(base + "/users")
assert response1.status_code == 200
print(f"We got back HTTP code 200.  Excellent!")
user1 = response1.json()
print(f"Our new user has ID {user1['user_id']} and api key {user1['api_key']}.  Dont tell anybody, though!")
print()

print(f"Now, we'll add some mood captures for user {user1['user_id']}")
r1 = requests.post(
    base + "/mood-captures",
    data={
            "user_id": user1["user_id"],
            "longitude": -122.4,
            "latitude": 37.8,
            "mood": "sad",
        },
    headers={"x-api-key": user1["api_key"]}
)
r2 = requests.post(
    base + "/mood-captures",
    data={
            "user_id": user1["user_id"],
            "longitude": -130.5,
            "latitude": 90,
            "mood": "happy",
        },
        headers={"x-api-key": user1["api_key"]}
    )
r3 = requests.post(
    base + "/mood-captures",
    data={
            "user_id": user1["user_id"],
            "longitude": -120.2,
            "latitude": -45,
            "mood": "happy",
        },
        headers={"x-api-key": user1["api_key"]}
    )
r4 = requests.post(
    base + "/mood-captures",
    data={
            "user_id": user1["user_id"],
            "longitude": -122.4,
            "latitude": 37.8,
            "mood": "happy",
        },
        headers={"x-api-key": user1["api_key"]}
    )
print("And here's what we got back:")
for response in [r1, r2, r3, r4]:
    print(f"Status code: {response.status_code}; Response: {response.json()}")
print()

print(f"Now, let's get the distribution of user {user1['user_id']}'s moods:")
r5 = requests.get(
    base + f"/mood-captures/frequen cy-distribution?user_id={user1['user_id']}",
)
print(r5.status_code)
assert r5.status_code == 401
print(f"Status code: {r5.status_code}; Response: {r5.text}")
print("Oops, we forgot to include the user's api key!  Let's try again.")
r6 = requests.get(
    base + f"/mood-captures/frequency-distribution?user_id={user1['user_id']}",
    headers={"x-api-key": user1["api_key"]}
)
print(f"Status code: {r5.status_code}; Response: {r5.json()}")
print("And finally, ")
'''
r7 = requests.get(base + "/mood-captures/nearest-happy?user_id=123&latitude=0&longitude=-120")
'''