# Stem Coding Challenge - Backend REST API (Mood Sensing App)
Author: Doug Klink

This readme covers design and implementation details for the project, as well as installation and usage instructions.

Sections:
- API Definition
- Data Model
- Data Persistence
- Authentication
- Authorization
- Code Structure
- Installation
- Usage/Demo
- Testing


# API Definition
There are 4 endpoints:
1. POST /users
2. POST /mood-captures
3. GET /mood-captures/frequency-distribution
4. GET /mood-captures/nearest-happy-location

Note: I initially tried to limit myself to only implementing the three endpoints in the project spec, but I had to add one more (POST /users) in order to implement authentication.

## 1. POST `/users`
Creates a new user, and returns a unique id and api key they can use for authentication.  No body parameters needed.

### Success Response
HTTP Status 201, and a response with the following parameters:
| Response Parameter | Data Type | Description |
| -- | -- | -- |
| `user_id` | `integer` | The ID for the new user |
| `api_key` | `string` | An api key that can be used to authenticate this user |

## 2. POST `/mood-captures`
Stores a new mood capture for a given user and location. Required body parameters:
| Body Parameter | Data Type | Description |
| -------------- | --------- | ----------- |
| `user_id` | `integer` | Unique identifier for the user to whom this mood capture belongs |
| `latitude` | `float` | Latitude at which the mood was captured, as a decimal in [-90, 90]|
| `longitude` | `float` | Longitude at which the mood was captured, as a decimal in [-180, 180] |
| `mood` | `string` | User's mood, must be one of {happy, sad, neutral}, case insensitive |

### Authentication
The request must contain an authorization header containing the user's API key, in format `x-api-key: <api_key>`

### Success Response
HTTP Status 201, and a response with the following parameters:
| Response Parameter | Data Type | Description |
| -- | -- | -- |
| `mood_capture_id` | `integer` | Unique id for the new mood capture |
| `user_id` | `integer` | user_id of the new mood capture |
| `latitude` | `float` | latitude of the new mood capture |
| `longitude` | `float` | longitude of the new mood capture |
| `mood` | `string` | mood of the new mood capture |

### Error Response
The relevant HTTP Status code and a string describing the problem.


## 3. GET `/mood-captures/frequency-distribution`
Gets a user's moods as a frequency distribution.  Required query parameters:
| Query Parameter | Data Type | Description |
| --------------- | --------- | ----------- |
| user_id | `integer` | Unique identifier for the user |

### Authentication
The request must contain an authorization header containing the user's API key, in format `x-api-key: <api_key>`

### Success Response
HTTP Status 200 and a response with the following parameters:

| Response Parameter | Data Type | Description |
| -- | -- | -- |
| `happy` | integer | The number of 'happy' moods recorded for the provided user |
| `sad` | integer | The number of 'sad' moods recorded for the provided user |
| `neutral` | integer | The number of 'neutral' moods recorded for the provided user |

### Error Response
The relevant HTTP Status code and a string describing the problem.  If no mood captures are found for the user, returns status code 404.

## 4. GET `/mood-captures/nearest-happy-location`
Given a user and a target location, gets the location of their nearest happy mood.  If multiple are equally near, returns one of their locations arbitrarily.  Required query parameters:

| Query Parameter | Data Type | Description |
| -------------- | --------- | ----------- |
| `user_id` | `integer` | Unique identifier for the user |
| `latitude` | `float` | Latitude of the target location, as a decimal in [-90, 90]|
| `longitude` | `float` | Longitude of the target location, as a decimal in [-180, 180] |

### Authentication
The request must contain an authorization header containing the user's API key, in format `x-api-key: <api_key>`

### Success Response
HTTP Status 200, and a response with the following parameters:
| Response Parameter | Data Type | Description |
| -- | -- | -- |
| `latitude` | `float` | Latitude of the nearest happy mood capture |
| `longitude` | `float` | Longitude of the nearest happy mood capture |

### Error Response
The relevant HTTP Status code and a string describing the problem.  If no happy mood captures are found for the user, returns status code 404.



# Data Model

## User
This resource represents a user whose mood captures are being recorded.
| Property | Type | Description |
| -------- | ---- | ----------- |
| `user_id` | `integer` | Unique id of the user |
| `api_key` | `string` | Latitude of user when the mood was captured, as a decimal in [-90, 90] |

## MoodCapture
This resource represents the capture of a user's mood at a particular location.
| Property | Type | Description |
| -------- | ---- | ----------- |
| `user_id` | `integer` | Unique id of the user who's mood was captured |
| `latitude` | `float` | Latitude of user when the mood was captured, as a decimal in [-90, 90] |
| `longitude` | `float` | Longitude of user when the mood was captured, as a decimal in [-180, 180] |
| `mood` | `string/enum` | User's mood, one of "happy", "sad", "neutral".  Represented with an enum wherever possible, lowercase string representation otherwise (e.g. in HTTP responses). |

# Data Persistence
For data persistence, this application uses the `sqlalchemy` ORM with a on-disk `sqlite` database.  The database is stored in the file `moods_app/data/sqlite.db`.  It will automatically be created by the application if it doesn't exist, and will be loaded if it doesn't.  To wipe it, simply delete the file and restart the application (more details below in the "usage" section).

# Authentication
This app uses a minimal authentication scheme.  When a new user is created using `POST /users`, an API key is created for the user and returned.  All other endpoints require `user_id` as a parameter, and an `api_key` in the authentication header.  They are used in conjunction to authenticate the user.

Note that we store the API key unencrypted in our database, as encrypting them wouldn't accomplish anything.  If a third party gains access to our database without our knowledge, they could only use the API keys to read/write to our database, which they already have access to.  So, encrypting them would not prevent them from accessing any additional sensitive data.

There are obviously more sophisticated methods of authentication (OAuth, for example), but for this project I see this scheme as a reasonable tradeoff of security vs complexity.

# Authorization
Each endpoint only reads/writes data for one user.  As such, I chose the simplest authorization scheme, which only allows a user to read/write their own data.  Since the same `user_id` is used for authentication and data access in all our endpoints, the authentication also implicitly serves as authorization.

# Code Structure
- `README.md`: this file; overview of project
- `demo.py`: script to demonstrate api functionality
- `requirements.txt`: dependencies for installation
- `moods_app`: application directory
    - `api.py`: the main flask application.  All the endpoints are in here, and this is the file to launch with flask to start the application.  More info in the "usage" section.
    - `auth.py`: helpers for user authentication
    - `database.py`: helpers for initializing and launching database
    - `input_validation.py`: helpers for validating API input
    - `utils.py`: utilities for performing more complex logic, e.g. nearest neighbor search
    - `.env`: stores config details such as path to database
    - `resources`: directory for database model objects
        - `base.py`: sqlalchemy base entity
        - `user.py`: sqlalchemy user entity
        - `mood_capture.py`: sqlalchemy mood capture entity
    - `data`: directory for persistent data
        - `sqlite.db`: the on-disk persistent database.  May not be present before application has been initialized.
    - `tests`: directory containing all unit tests.  Sub-structure mirrors `moods_app`.

# Installation
In a clean environment, install `python 3.11` and `pip`, then run `pip install -r requirements.txt`.  That's it!

# Usage/Demo
From the project root, launch the api using `flask --app moods_app/api run`.  Then, run `python demo.py` to see the api respond to requests!  Or, make your own requests to the exposed endpoints.  The flask server will tell you where it's running upon launch (default is `127.0.0.1:5000`).

# Tests
Unit tests are located in `moods_app/tests.` To execute the test suite, simply run `pytest` in the project root directory.  I went to lengths to ensure the testing is not just thorough, but also efficient, with a single self-cleaning database connection used across all tests; the details of that can be found in `moods_app/tests/confest.py`.

# Conclusion
Thank you for reading this whole thing!  I look forward to reviewing the project with you, talking through my design decisions, and learning where things could be improved.

All the best,

Doug Klink