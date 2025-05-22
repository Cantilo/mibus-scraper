from datetime import datetime
from pathlib import Path
import shutil

OLD_DATA_DIR = "data"
DATA_FILE_NAMES = [
    "paradas.json",
    "unique_paradas.json",
    "info_rutas.json",
    "recorridos.json",
]
if __name__ == "__main__":
    # change the name of the files to include todays date
    for filename in DATA_FILE_NAMES:
        current_file = Path(filename)
        new_filename = Path(
            "old", f"{current_file.stem}-{datetime.now():%Y-%m-%d}.json"
        )
        shutil.copy2(filename, new_filename)
