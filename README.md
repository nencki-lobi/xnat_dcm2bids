# xnat_dcm2bids

## install
```
python -m venv ./venv
source venv/bin/activate
pip install https://github.com/bkossows/xnat_dcm2bids/archive/refs/heads/master.zip
```

## run
```
dcm2bids_scaffold -o ./bids-dir
xnat-dcm2bids --bids-dir bids-dir --config ./config.json 55b4c571-cc33-4d 02 01
```

## run multiple subjects
prepare csv as follows:
```
23fa0001-b839-40,2025-06-04,MW25a,pilot3,01
55b4c571-cc33-4d,2025-06-04,MW25a,pilot2,01
fd4197f4-72a3-48,2025-06-04,MW25a,pilot1,01
```

and run
```
awk -F',' '{print $1, $4, $5}' subjects.csv | while read id sub ses; do xnat-dcm2bids --bids-dir bids-dir --config ./config.json "$id" "$sub" "$ses"; done
```
