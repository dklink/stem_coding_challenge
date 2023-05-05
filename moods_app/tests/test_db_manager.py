from tempfile import TemporaryDirectory, NamedTemporaryFile
from pathlib import Path

from moods_app.db_manager import DBManager
from moods_app.resources.mood import Mood

import pandas as pd


def test_create_new_table():
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


def test_write_mood():
    mood1 = Mood(
        user_id=123,
        latitude=71.5,
        longitude=-123.2,
        emotional_state="happy",
    )

    with TemporaryDirectory(suffix=".csv") as tmpdir:
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

    with TemporaryDirectory(suffix=".csv") as tmpdir:
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
