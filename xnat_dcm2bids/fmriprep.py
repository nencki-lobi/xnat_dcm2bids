import json
from pathlib import Path
import re
import sys

def clean_path(path):
    # Usuwa "bids::sub-XX/ses-YY/" z początku ścieżki
    return re.sub(r"^bids::sub-[0-9a-zA-Z]+/", "", path)

def repair_fieldmap_json(file_path: Path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Zamień klucz "intendedFor" na "IntendedFor"
        if "intendedFor" in data:
            data["IntendedFor"] = data.pop("intendedFor")

        # Obsługa pojedynczego stringa lub listy ścieżek
        if "IntendedFor" in data:
            val = data["IntendedFor"]
            if isinstance(val, str):
                data["IntendedFor"] = clean_path(val)
            elif isinstance(val, list):
                data["IntendedFor"] = [clean_path(p) for p in val]

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        print(f"✔ {file_path}")

    except Exception as e:
        print(f"❌ {file_path}: {e}")

def repair_all_fieldmaps(subjects_dir: Path):
    for json_file in subjects_dir.glob("**/fmap/*.json"):
        repair_fieldmap_json(json_file)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Użycie: python repair_fieldmaps.py /ścieżka/do/bids")
        sys.exit(1)

    repair_all_fieldmaps(Path(sys.argv[1]))
