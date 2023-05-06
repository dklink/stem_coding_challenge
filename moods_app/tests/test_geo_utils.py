from moods_app.geo_utils import nearest_neighbor

def test_nearest_neigbor_no_locations():
    result = nearest_neighbor((0, 0), [])
    assert result is None


def test_nearest_neighbor():
    target = (10, 10)
    locations = [(45, 37), (-90, 0), (11, 11)]

    result = nearest_neighbor(target, locations)

    assert result == (11, 11)
