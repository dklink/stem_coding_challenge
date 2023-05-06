from moods_app.utils import nearest_neighbor_latlon

def test_nearest_neigbor_no_locations():
    result = nearest_neighbor_latlon((0, 0), [])
    assert result is None


def test_nearest_neighbor():
    target = (10, 10)
    locations = [(45, 37), (-90, 0), (11, 11)]

    result = nearest_neighbor_latlon(target, locations)

    assert result == (11, 11)
