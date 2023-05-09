from moods_app.utils import nearest_neighbor_latlon, calculate_mood_distribution
from moods_app.resources.mood_capture import Mood
import random


def test_nearest_neigbor_no_locations():
    result = nearest_neighbor_latlon((0, 0), [])
    assert result is None


def test_nearest_neighbor():
    locations = [(45, 37), (-90, 0), (11, 11)]
    target1 = (10, 10)
    target2 = (46, 38)
    target3 = (-85, 5)

    result1 = nearest_neighbor_latlon(target1, locations)
    result2 = nearest_neighbor_latlon(target2, locations)
    result3 = nearest_neighbor_latlon(target3, locations)

    assert result1 == (11, 11)
    assert result2 == (45, 37)
    assert result3 == (-90, 0)


def test_nearest_neighbor_equidistant():
    """make sure in an equidistant case, it returns one of them arbitrarily, and doesn't explode"""
    locations = [(-10, -10), (10, 10), (90, 120)]
    target = (0, 0)

    result = nearest_neighbor_latlon(target, locations)

    assert result in [(-10, -10), (10, 10)]


def test_mood_distribution_empty():
    assert calculate_mood_distribution([]) == {
        "happy": 0,
        "sad": 0,
        "neutral": 0,
    }


def test_mood_distribution():
    moods = [Mood.happy] * 10 + [Mood.sad] * 2 + [Mood.neutral] * 55
    random.seed(42)
    random.shuffle(moods)

    assert calculate_mood_distribution(moods) == {
        "happy": 10,
        "sad": 2,
        "neutral": 55,
    }
