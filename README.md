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

### Success Response
HTTP Status 201, and a response with the following parameters:
| Response Parameter | Data Type | Description |
| -- | -- | -- |
| `id` | `integer` | The ID for the new mood capture |
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
| `latitude` | `float` | latitude of the target location, as a decimal in [-90, 90]|
| `longitude` | `float` | longitude of the target location, as a decimal in [-180, 180] |

### Success Response
HTTP Status 200, and a response with the following parameters:
| Response Parameter | Data Type | Description |
| -- | -- | -- |
| `latitude` | `float` | latitude of the nearest happy mood capture |
| `longitude` | `float` | longitude of the nearest happy mood capture |

### Error Response
The relevant HTTP Status code and a string describing the problem.  If no happy mood captures are found for the user, returns status code 404.


# Resource Definitions
| Resource | Description |
| -------- | ----------- |
| `MoodCapture` | A user's mood at a specified location.  Supported moods: happy, sad, neutral. Location defined using ISO 6709 latitude and longitude.|

Note: in any real application, we would need a `User` resource and a database table to back it.  It has been omitted here to keep implementation lightweight, as it isn't strictly necessary to implement the desired functionality.



## Data Persistence

## Authentication

## Authorization

## Installation

## Usage

## Tests
Tests for all python modules are located in `moods_app/tests.`
To run the test suite, simply run `pytest` in the project root directory.
