from tempfile import TemporaryDirectory, NamedTemporaryFile
from pathlib import Path

from moods_app.db_manager import DBManager
from moods_app.resources.mood import MoodCapture, Mood

import pandas as pd


def test_create_new_table_no_file():
    with TemporaryDirectory() as tmpdir:
        # create a temporary path to a nonexistent file
        table = Path(tmpdir) / "empty.csv"
        assert not table.exists()

        # create a db manager for this path
        manager = DBManager(mood_captures_table_path=table)

        # check the manager created the file
        assert table.exists()

        # check the table is empty and has correct columns
        df = pd.read_csv(table)
        assert len(df) == 0
        assert set(df.columns) == {"id", "user_id", "latitude", "longitude", "mood"}


def test_create_new_table_empty_file():
    with TemporaryDirectory() as tmpdir:
        # create a temporary path to an empty file
        table = Path(tmpdir) / "empty.csv"
        table.touch()

        # create a db manager for this path
        manager = DBManager(mood_captures_table_path=table)

        # check the manager created the file
        assert table.exists()

        # check the table is empty and has correct columns
        df = pd.read_csv(table)
        assert len(df) == 0
        assert set(df.columns) == {"id", "user_id", "latitude", "longitude", "mood"}


def test_write_new_mood_capture():
    mood1 = MoodCapture(
        user_id=123,
        latitude=71.5,
        longitude=-123.2,
        mood=Mood.HAPPY,
    )

    with TemporaryDirectory() as tmpdir:
        table = Path(tmpdir) / "moods.csv"
        manager = DBManager(mood_captures_table_path=table)
        manager.write_new_mood_capture(mood1)

        contents = pd.read_csv(table)
        assert len(contents) == 1
        assert contents["id"].item() == 0
        assert contents["user_id"].item() == mood1.user_id
        assert contents["latitude"].item() == mood1.latitude
        assert contents["longitude"].item() == mood1.longitude
        assert contents["mood"].item() == mood1.mood.value


def test_write_new_mood_captures_multiple():
    mood1 = MoodCapture(
        user_id=123,
        latitude=71.5,
        longitude=-123.2,
        mood=Mood.HAPPY,
    )
    mood2 = MoodCapture(
        user_id=456,
        latitude=0,
        longitude=-10,
        mood=Mood.SAD,
    )

    with TemporaryDirectory() as tmpdir:
        table = Path(tmpdir) / "moods.csv"
        manager = DBManager(mood_captures_table_path=table)
        manager.write_new_mood_capture(mood1)
        manager.write_new_mood_capture(mood2)

        contents = pd.read_csv(table)
        assert len(contents) == 2
        assert contents.iloc[0]["id"] == 0
        assert contents.iloc[0]["user_id"] == mood1.user_id
        assert contents.iloc[1]["id"] == 1
        assert contents.iloc[1]["user_id"] == mood2.user_id


def test_retrieve_mood_captures_empty_table():
    with NamedTemporaryFile() as tmp:
        manager = DBManager(mood_captures_table_path=tmp.name)
        result = manager.retreive_mood_captures(user_id=0)

        assert len(result) == 0


def test_retreive_mood_captures_by_user():
    with NamedTemporaryFile() as tmp:
        # populate db with some data
        columns = ["id", "user_id", "latitude", "longitude", "mood"]
        records = [
            [0, 123, 71.5, 123.2, "happy"],
            [1, 456, 23.2, -100, "sad"],
            [2, 456, 22.8, -99, "neutral"],
            [3, 456, 23.3, -101, "happy"],
        ]   
        pd.DataFrame(records, columns=columns).set_index("id").to_csv(tmp)

        # set up manager
        manager = DBManager(mood_captures_table_path=tmp.name)
        results = manager.retreive_mood_captures(user_id=456)

        # make sure we got all the records, and no extraneous records
        assert len(results) == 3
        assert all(mood.user_id == 456 for mood in results)
        assert set(mood.mood.value for mood in results) == {"happy", "neutral", "sad"}



def test_retrieve_mood_captures_by_user_and_mood():
    with NamedTemporaryFile() as tmp:
        # populate db with some data
        columns = ["id", "user_id", "latitude", "longitude", "mood"]
        records = [
            [0, 123, 71.5, 123.2, "happy"],
            [1, 456, 23.2, -100, "sad"],
            [2, 456, 22.8, -99, "neutral"],
            [3, 456, 23.3, -101, "happy"],
        ]   
        pd.DataFrame(records, columns=columns).set_index("id").to_csv(tmp)

        # set up manager
        manager = DBManager(mood_captures_table_path=tmp.name)
        results = manager.retreive_mood_captures(user_id=456, mood=Mood.NEUTRAL)

        # make sure we got all the records, and no extraneous records
        assert len(results) == 1
        assert results[0].user_id == 456
        assert results[0].mood.value == "neutral"
