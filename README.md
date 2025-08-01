# xnat_dcm2bids

## install
```
python -m venv ./venv
source venv/bin/activate
pip install https://github.com/nencki-lobi/xnat_dcm2bids/archive/refs/heads/master.zip
```

## use

```bash
xnat-dcm2bids [OPTIONS] SESSION_ID SUBJECT_ID SESSION_NUMBER
```

### Arguments:

* `SESSION_ID` – XNAT session ID
* `SUBJECT_ID` – BIDS subject ID (e.g., `01`)
* `SESSION_NUMBER` – BIDS session number (e.g., `01`)

### Options:

| Option                            | Description                                       | Default                              |
| --------------------------------- | ------------------------------------------------- | ------------------------------------ |
| `--bids-dir TEXT`                 | Ścieżka do katalogu BIDS                          | `./bids-dir`                         |
| `--auto_extract_entities BOOLEAN` | dcm2bids option; skips run label if not necessary | `True`                               |
| `--config TEXT`                   | Path to `config.json`                             | `{bids_dir}/code/config.json`        |
| `--sourcedata TEXT`               | Path to DICOMs                                    | `{bids_dir}/sourcedata/{subject_id}` |


### Example: run single subject
```
dcm2bids_scaffold -o ./bids-dir
xnat-dcm2bids --bids-dir bids-dir --config ./config.json 55b4c571-cc33-4d pilot2 01
```

### Example: run multiple subjects
[prepare csv as follows](https://bkossows.notion.site/Export-XNAT-sessions-to-CSV-249fe8b66b5d42b98feb06897a92fea9):
```
23fa0001-b839-40,2025-06-04,MW25a,pilot3,01
55b4c571-cc33-4d,2025-06-04,MW25a,pilot2,01
fd4197f4-72a3-48,2025-06-04,MW25a,pilot1,01
```

and run
```
MacOS/Linux:
while IFS=',' read -r id _ sub ses _; do xnat-dcm2bids --config ./config.json "$id" "$sub" "$ses"; done < subjects.csv
Windows:
for /f "usebackq skip=1 tokens=1,3,4 delims=," %A in ("subjects.csv") do xnat-dcm2bids --config config.json %A %B %C
```

## more 
- [dcm2niix customization](dcm2niix.md)

- [troubleshooting](troubleshooting.md)



