from haversine import haversine
from typing import Tuple, List, Optional


def nearest_neighbor(target: Tuple[float, float], locations: List[Tuple[float, float]]) -> Optional[Tuple[float, float]]:
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
    
    return nearest
