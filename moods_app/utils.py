from haversine import haversine
from typing import Tuple, List, Dict, Optional

from moods_app.resources.mood_capture import Mood


def nearest_neighbor_latlon(
    target: Tuple[float, float], locations: List[Tuple[float, float]]
) -> Optional[Tuple[float, float]]:
    """Performs a nearest neighbor search over a set of latitude/longitude locations, using haversine distance
    :param target: (latitude, longitude) tuple
    :param locations: list of (latitude, longitude) tuples
    :returns: (latitude, longitude) tuple, or None
    """
    nearest = None
    nearest_distance = float("inf")
    for location in locations:
        distance = haversine(target, location)
        if distance < nearest_distance:
            nearest = location
            nearest_distance = distance

    return nearest


def calculate_mood_distribution(moods: List[Mood]) -> Dict[str, int]:
    """For a list of moods, returns a dict with a counter of how many moods are in the list.
    Keys are strings from enum .name property"""
    distribution = {key.name: 0 for key in Mood}
    for mood in moods:
        distribution[mood.name] += 1
    return distribution
