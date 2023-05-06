# Stem Coding Challenge - Backend REST API (Mood Sensing App)
Author: Doug Klink

## Resource Definitions
| Resource | Description |
| -------- | ----------- |
| MoodCaptures | A user's mood at a specified location.  Supported moods: happy, sad, neutral. Location defined using ISO 6709 latitude and longitude.|

Note: in any real application, we would need a `Users` resource and a database table to back it.  It has been omitted here to keep implementation lightweight.


## API Definition: Endpoints

| HTTP Method | API Endpoint | Description |
| ----------- | ------------ | ----------- |
| POST | `/mood-captures` | Creates a new mood capture for a given user and location |
| GET | `/mood-captures/frequency_distribution?user_id=<user_id>` | Gets a user's moods as a frequency distribution |
| GET | `/mood-captures/nearest-happy?user_id=<user_id>&latitude=<latitude>&longitude=<longitude>` | Given a user and a location, gets the location of their nearest happy mood |


## Tests
To run the test suite, simply run `pytest` in the project root directory.
