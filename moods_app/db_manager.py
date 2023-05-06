from pathlib import Path
from typing import List

import pandas as pd
import os

from moods_app.resources.mood import Mood


class DBManager:
    """Lightweight class to write/read to a 'database' (csv file, in this implementation)"""

    def __init__(self, moods_table_path: str):
        """Create the manager.  All it needs is a path to a csv file.
        Creates the file if the path doesn't exist.
        Initializes the column headers if the file is empty.
        Otherwise, checks to make sure table is correctly formatted."""
        self.moods_table_path = moods_table_path

        if (not Path(self.moods_table_path).exists()
            or os.stat(self.moods_table_path).st_size == 0):
            table = pd.DataFrame(
                columns=[
                    "user_id",
                    "latitude",
                    "longitude",
                    "emotional_state"
                ]
            )
            table.index.name = "id"
            table.to_csv(self.moods_table_path)
        
        # check table is not malformed (TODO)

    def write_new_mood(self, mood: Mood):
        """writes a new mood into the moods table."""
        table = self._read_table()
        new_row = pd.DataFrame(vars(mood), index=[len(table)])
        new_row.index.name = "id"
        table = pd.concat([table, new_row])
        table.to_csv(self.moods_table_path)

    def get_all_moods_for_user(self, user_id: int) -> List[Mood]:
        """retrieves all moods and filters by provided user_id"""
        table = self._read_table()
        filtered = table[table["user_id"] == user_id]
        return [
            Mood(
                user_id=row["user_id"],
                latitude=row["latitude"],
                longitude=row["longitude"],
                emotional_state=row["emotional_state"],
            )
            for _, row in filtered.iterrows()
        ]

    def _read_table(self):
        return pd.read_csv(self.moods_table_path, index_col="id")
