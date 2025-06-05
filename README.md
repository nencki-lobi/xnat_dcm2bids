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
