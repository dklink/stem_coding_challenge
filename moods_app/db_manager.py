from pathlib import Path
from typing import List

import pandas as pd

from moods_app.resources.mood import Mood


class DBManager:
    """Lightweight class to write/read to a 'database' (csv file, in this implementation)"""

    def __init__(self, moods_table_path: str):
        """Create the manager.  All it needs is a path to a csv file.  Creates the table if it doesn't exist."""
        self.moods_table_path = moods_table_path

        if not Path(self.moods_table_path).exists():
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

    def write_new_mood(self, mood: Mood):
        """writes a new mood into the moods table."""
        table = pd.read_csv(self.moods_table_path, index_col="id")
        new_row = pd.DataFrame(vars(mood), index=[len(table)])
        new_row.index.name = "id"
        table = table.append(new_row)
        table.to_csv(self.moods_table_path)

    def get_all_moods_for_user(self, user_id: int) -> List[Mood]:
        pass
