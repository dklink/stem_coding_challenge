from moods_app.utils import nearest_neighbor_latlon, calculate_mood_distribution
from moods_app.resources.mood_capture import Mood
import random

def test_nearest_neigbor_no_locations():
    result = nearest_neighbor_latlon((0, 0), [])
    assert result is None


def test_nearest_neighbor():
    target = (10, 10)
    locations = [(45, 37), (-90, 0), (11, 11)]

    result = nearest_neighbor_latlon(target, locations)

    assert result == (11, 11)


def test_mood_distribution_empty():
    assert calculate_mood_distribution([]) == {
        "happy": 0,
        "sad": 0,
        "neutral": 0,
    }


def test_mood_distribution():
    moods = [Mood.happy] * 10 + [Mood.sad] * 2 + [Mood.neutral] * 55
    random.shuffle(moods)

    assert calculate_mood_distribution(moods) == {
        "happy": 10,
        "sad": 2,
        "neutral": 55,
    }
