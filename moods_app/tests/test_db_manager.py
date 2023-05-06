from tempfile import TemporaryDirectory, NamedTemporaryFile
from pathlib import Path

from moods_app.db_manager import DBManager
from moods_app.resources.mood import Mood

import pandas as pd


def test_create_new_table_no_file():
    with TemporaryDirectory() as tmpdir:
        # create a temporary path to a nonexistent file
        table = Path(tmpdir) / "empty.csv"
        assert not table.exists()

        # create a db manager for this path
        manager = DBManager(moods_table_path=table)

        # check the manager created the file
        assert table.exists()

        # check the table is empty and has correct columns
        df = pd.read_csv(table)
        assert len(df) == 0
        assert set(df.columns) == {"id", "user_id", "latitude", "longitude", "emotional_state"}


def test_create_new_table_empty_file():
    with TemporaryDirectory() as tmpdir:
        # create a temporary path to an empty file
        table = Path(tmpdir) / "empty.csv"
        table.touch()

        # create a db manager for this path
        manager = DBManager(moods_table_path=table)

        # check the manager created the file
        assert table.exists()

        # check the table is empty and has correct columns
        df = pd.read_csv(table)
        assert len(df) == 0
        assert set(df.columns) == {"id", "user_id", "latitude", "longitude", "emotional_state"}


def test_write_mood():
    mood1 = Mood(
        user_id=123,
        latitude=71.5,
        longitude=-123.2,
        emotional_state="happy",
    )

    with TemporaryDirectory() as tmpdir:
        table = Path(tmpdir) / "moods.csv"
        manager = DBManager(moods_table_path=table)
        manager.write_new_mood(mood1)

        contents = pd.read_csv(table)
        assert len(contents) == 1
        assert contents["id"].item() == 0
        assert contents["user_id"].item() == mood1.user_id
        assert contents["latitude"].item() == mood1.latitude
        assert contents["longitude"].item() == mood1.longitude
        assert contents["emotional_state"].item() == mood1.emotional_state


def test_write_multiple_moods():
    mood1 = Mood(
        user_id=123,
        latitude=71.5,
        longitude=-123.2,
        emotional_state="happy",
    )
    mood2 = Mood(
        user_id=456,
        latitude=0,
        longitude=-10,
        emotional_state="sad",
    )

    with TemporaryDirectory() as tmpdir:
        table = Path(tmpdir) / "moods.csv"
        manager = DBManager(moods_table_path=table)
        manager.write_new_mood(mood1)
        manager.write_new_mood(mood2)

        contents = pd.read_csv(table)
        assert len(contents) == 2
        assert contents.iloc[0]["id"] == 0
        assert contents.iloc[0]["user_id"] == mood1.user_id
        assert contents.iloc[1]["id"] == 1
        assert contents.iloc[1]["user_id"] == mood2.user_id


def test_get_all_moods_for_user_empty_table():
    with NamedTemporaryFile() as tmp:
        manager = DBManager(moods_table_path=tmp.name)
        result = manager.get_all_moods_for_user(user_id=0)

        assert len(result) == 0


def test_get_all_moods_for_user():
    with NamedTemporaryFile() as tmp:
        # populate db with some data
        columns = ["id", "user_id", "latitude", "longitude", "emotional_state"]
        records = [
            [0, 123, 71.5, 123.2, "happy"],
            [1, 456, 23.2, -100, "sad"],
            [2, 456, 22.8, -99, "neutral"],
            [3, 456, 23.3, -101, "happy"],
        ]   
        pd.DataFrame(records, columns=columns).set_index("id").to_csv(tmp)

        # set up manager
        manager = DBManager(moods_table_path=tmp.name)
        results = manager.get_all_moods_for_user(user_id=456)

        # make sure we got all the records, and no extraneous records
        assert len(results) == 3
        assert all(mood.user_id == 456 for mood in results)
        assert set(mood.emotional_state for mood in results) == {"happy", "neutral", "sad"}
