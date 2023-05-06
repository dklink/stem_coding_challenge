from pathlib import Path
from typing import List, Optional

import pandas as pd
import os

from moods_app.resources.mood_capture import MoodCapture, Mood


class DBManager:
    """Class to read/write to a lightweight 'database' (csv file, in this implementation)"""

    def __init__(self, mood_captures_table_path: str):
        """Create the manager.  All it needs is a path to a csv file.
        Notes: if the path doesn't exist, a new file is created.
            If the path points to an empty file, column headers are initialized.
            If the path points to a non-empty file, check to make sure it has the correct headers.
        """
        self.table_path = mood_captures_table_path

        if (not Path(self.table_path).exists()
            or os.stat(self.table_path).st_size == 0):
            table = pd.DataFrame(
                columns=[
                    "user_id",
                    "latitude",
                    "longitude",
                    "mood"
                ]
            )
            table.index.name = "id"
            table.to_csv(self.table_path)
        else:
            table = pd.read_csv(self.table_path)
            if set(table.columns) != {"id", "user_id", "latitude", "longitude", "mood"}:
                raise RuntimeError("Database is corrupt - incorrect and/or unexpected column names.")

    def write_new_mood_capture(self, mood_capture: MoodCapture):
        """writes a new mood into the moods table."""
        table = self._read_table()
        new_row = pd.DataFrame(
            {
                "user_id": mood_capture.user_id,
                "latitude": mood_capture.latitude,
                "longitude": mood_capture.longitude,
                "mood": mood_capture.mood.value,
            },
            index=[len(table)],
        )
        new_row.index.name = "id"
        table = pd.concat([table, new_row])
        table.to_csv(self.table_path)

    def retreive_mood_captures(self, user_id: int, mood: Optional[Mood]=None) -> List[MoodCapture]:
        """Filters moods by user_id, and mood (optionally).  Returns a list of mood objects."""
        table = self._read_table()
        filtered = table[table["user_id"] == user_id]
        if mood is not None:
            filtered = filtered[filtered["mood"] == mood.value]
        return [
            MoodCapture(
                user_id=row["user_id"],
                latitude=row["latitude"],
                longitude=row["longitude"],
                mood=Mood(row["mood"]),
            )
            for _, row in filtered.iterrows()
        ]

    def _read_table(self):
        return pd.read_csv(self.table_path, index_col="id")
