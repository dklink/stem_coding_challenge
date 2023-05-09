"""
This script runs a demo of hitting the api endpoints a few different ways.
To launch the api, run `flask --app api run` in the "moods_app" directory
"""
import requests

if __name__ == "__main__":
    base_url = "http://127.0.0.1:5000"  # default flask port

    print("First, we'll create a new user, with POST /users.  Here's the response:")
    user_response = requests.post(base_url + "/users")
    assert user_response.status_code == 200
    print(
        f"\tStatus code: {user_response.status_code}; Response: {user_response.json()}"
    )
    print(
        "Put that api key somewhere safe, you'll need it to authenticate the other endpoints!"
    )
    user1 = user_response.json()
    print()

    print(
        f"Now, we'll add some mood captures for user {user1['user_id']} using POST /mood-captures"
    )
    r1 = requests.post(
        base_url + "/mood-captures",
        data={
            "user_id": user1["user_id"],
            "longitude": 10.3,
            "latitude": 15.2,
            "mood": "sad",
        },
        headers={"x-api-key": user1["api_key"]},
    )
    r2 = requests.post(
        base_url + "/mood-captures",
        data={
            "user_id": user1["user_id"],
            "longitude": 0.1,
            "latitude": 16.2,
            "mood": "happy",
        },
        headers={"x-api-key": user1["api_key"]},
    )
    r3 = requests.post(
        base_url + "/mood-captures",
        data={
            "user_id": user1["user_id"],
            "longitude": 0,
            "latitude": 14,
            "mood": "happy",
        },
        headers={"x-api-key": user1["api_key"]},
    )
    r4 = requests.post(
        base_url + "/mood-captures",
        data={
            "user_id": user1["user_id"],
            "longitude": -10,
            "latitude": 15.2,
            "mood": "happy",
        },
        headers={"x-api-key": user1["api_key"]},
    )
    print("And here's what we got back:")
    for response in [r1, r2, r3, r4]:
        print(f"\tStatus code: {response.status_code}; Response: {response.json()}")
    print()

    print(
        f"Now, let's get the distribution of user {user1['user_id']}'s moods using GET /mood-captures/frequency-distribution"
    )
    r5 = requests.get(
        base_url + f"/mood-captures/frequency-distribution?user_id={user1['user_id']}",
    )
    assert r5.status_code == 401
    print(f"\tStatus code: {r5.status_code}; Response: {r5.text}")
    print(
        "Oops, we forgot to include the user's api key in the headers!  Let's try again."
    )
    r6 = requests.get(
        base_url + f"/mood-captures/frequency-distribution?user_id={user1['user_id']}",
        headers={"x-api-key": user1["api_key"]},
    )
    print(f"\tStatus code: {r6.status_code}; Response: {r6.json()}")
    print()
    target_lat = 20
    target_lon = 0
    print(
        f"Finally, let's find the user's nearest location to {target_lat} latitude, {target_lon} longitude."
    )
    print("We'll use GET /mood-captures/nearest-happy-location to do this.")
    print("Hint: the answer should be (16.2, 0.1).")
    r7 = requests.get(
        base_url + f"/mood-captures/nearest-happy-location?user_id={user1['user_id']}",
        headers={"x-api-key": user1["api_key"]},
    )
    assert r7.status_code == 400
    print(f"\tStatus code: {r7.status_code}; Response: {r7.text}")
    print("Oops, we forgot to include the target location!  Let's try again.")
    r8 = requests.get(
        base_url
        + f"/mood-captures/nearest-happy-location?user_id={user1['user_id']}&latitude={target_lat}&longitude={target_lon}",
        headers={"x-api-key": user1["api_key"]},
    )
    print(f"\tStatus code: {r8.status_code}; Response: {r8.json()}")
    print()

    print("That's all, folks!")
