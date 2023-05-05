# Stem Coding Challenge - Backend REST API (Mood Sensing App)
### Author: Doug Klink

## Resource Definitions
| Resource | Description |
| -------- | ----------- |
| Moods | A user's emotional state at a specified location.  Current supported states: happy, sad, neutral. Location defined using ISO 6709 latitude and longitude.|


## API Definition: Endpoints

| HTTP Method | API Endpoint | Description | 
| ----------- | ------------ | ----------- |
| POST | `/moods` | Creates a new mood capture for a given user and location |
| GET | `/moods/frequency_distribution?user=<user_id>` | Gets a user's moods as a frequency distribution |
| GET | `/moods/nearest-happy?user=<user_id>&location=<longitude>,<latitude>` | Given a user and a location, gets the location of their nearest happy mood |


## Tests
To run the test suite, simply run `pytest` in the project root directory.