# Stem Coding Challenge - Backend REST API (Mood Sensing App)
Author: Doug Klink


# API Definition

## 1. POST `/mood-captures`
Stores a new mood capture for a given user and location. Required body parameters:
| Body Parameter | Data Type | Description |
| -------------- | --------- | ----------- |
| `user_id` | `integer` | Unique identifier for the user to whom this mood capture belongs |
| `latitude` | `float` | Latitude at which the mood was captured, as a decimal in [-90, 90]|
| `longitude` | `float` | Longitude at which the mood was captured, as a decimal in [-180, 180] |
| `mood` | `string` | User's mood, must be one of {happy, sad, neutral}, case insensitive |

### Authentication
The request must contain an Authorization header containing the user's API key, in format `Authorization: api_key=<api_key>`

### Success Response
HTTP Status 201, and a response with the following parameters:
| Response Parameter | Data Type | Description |
| -- | -- | -- |
| `mood_capture_id` | `integer` | The ID for the new mood capture |
| `user_id` | `integer` | user_id of the new mood capture |
| `latitude` | `float` | latitude of the new mood capture |
| `longitude` | `float` | longitude of the new mood capture |
| `mood` | `string` | mood of the new mood capture |

### Error Response
The relevant HTTP Status code and a string describing the problem.


## 2. GET `/mood-captures/frequency-distribution`
Gets a user's moods as a frequency distribution.  Required query parameters:
| Query Parameter | Data Type | Description |
| --------------- | --------- | ----------- |
| user_id | `integer` | Unique identifier for the user |

### Authentication
The request must contain an Authorization header containing the user's API key, in format `Authorization: api_key=<api_key>`

### Success Response
HTTP Status 200 and a response with the following parameters:

| Response Parameter | Data Type | Description |
| -- | -- | -- |
| `happy` | integer | The number of 'happy' moods recorded for the provided user |
| `sad` | integer | The number of 'sad' moods recorded for the provided user |
| `neutral` | integer | The number of 'neutral' moods recorded for the provided user |

### Error Response
The relevant HTTP Status code and a string describing the problem.  If no mood captures are found for the user, returns status code 404.

## 3. GET `/mood-captures/nearest-happy`
Given a user and a target location, gets the location of their nearest happy mood.  Required query parameters:

| Query Parameter | Data Type | Description |
| -------------- | --------- | ----------- |
| `user_id` | `integer` | Unique identifier for the user |
| `latitude` | `float` | Latitude of the target location, as a decimal in [-90, 90]|
| `longitude` | `float` | Longitude of the target location, as a decimal in [-180, 180] |

### Authentication
The request must contain an Authorization header containing the user's API key, in format `Authorization: api_key=<api_key>`

### Success Response
HTTP Status 200, and a response with the following parameters:
| Response Parameter | Data Type | Description |
| -- | -- | -- |
| `latitude` | `float` | Latitude of the nearest happy mood capture |
| `longitude` | `float` | Longitude of the nearest happy mood capture |

### Error Response
The relevant HTTP Status code and a string describing the problem.  If no happy mood captures are found for the user, returns status code 404.

## 4. POST `/users`
Creates a new user, and returns a unique id and api key they can use for authentication.  No body parameters needed.

### Success Response
HTTP Status 201, and a response with the following parameters:
| Response Parameter | Data Type | Description |
| -- | -- | -- |
| `user_id` | `integer` | The ID for the new user |
| `api_key` | `string` | An api key that can be used to authenticate this user |

# Data Model

## User
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

Note: in any real application, we would want a `User` resource and a database table to back it.  It has been omitted here to keep implementation lightweight, as it isn't strictly necessary to implement the desired API endpoints.

## Data Persistence
For data persistence, this application uses the `sqlalchemy` ORM with a on-disk `sqlite` database.  The database is stored at `moods_app/persistent_data/sqlite.db` and can be initialized using `moods_app/init_db.py`.

## Authentication
This app uses a minimal authentication scheme.  When a new user is created using `POST /users`, an API key is created for the user and returned.  All other endpoints require `user_id` and `api_key`, which are used in conjunction to authenticate the user.

Note that we store the API key unencrypted in our database, as encrypting them wouldn't accomplish anything.  If a third party gains access to our database without our knowledge, they could only use the API keys to read/write to our database, which they already have access to.  So, encrypting them would not prevent them from accessing any additional sensitive data.

This is not the most sophisticated or secure method of authentication, but I think for this project, this scheme is a reasonable tradeoff of security vs complexity.

## Authorization
Each endpoint only reads/writes data for one user.  As such, I chose the simplest authorization scheme, which allows a user to read/write only their own data.  Since the same `user_id` is used for authentication and data access in all our endpoints, the authentication also implicitly serves as authorization.

## Code Structure

## Installation

## Usage

## Tests
Tests for all python modules are located in `moods_app/tests.`
To run the test suite, simply run `pytest` in the project root directory.
