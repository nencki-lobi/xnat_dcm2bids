# xnat_dcm2bids

[installation](#installation)  
[examples](#examples)  
[hints and tips](#more)

## Modules

This package consists of the following modules:

* **`xnat_getcsv`** – downloads a list of all sessions for a given XNAT project and saves it to a CSV file:  
`xnat_getcsv mj_ris.csv mj_ris`

* **`xnat_dcm2bids`** – downloads data from a selected XNAT session (e.g., `f490f566-2124-46`) and converts it to BIDS format using `dcm2bids`:  
`xnat_dcm2bids --bids-dir ~/bids-dir --config ./code/config.json f490f566-2124-46 03 01`

* **`lobi_script`** – a shortcut for running scripts from the [lobi-mri-scripts](https://github.com/nencki-lobi/lobi-mri-scripts) repository:  
`lobi_script run_mriqc.sh 03 ~/bids-dir ~/bids-dir/derivatives/mriqc`

---

## Additional Tools (automatically installed)

The package also leverages existing tools, which are installed automatically. Some commands are very useful:

* **[dcm2bids](https://unfmontreal.github.io/Dcm2Bids/)**

   * **`dcm2bids_scaffold`** – prepares a new BIDS directory:  
   `dcm2bids_scaffold -o /home/jovyan/bids-dir`

   * **`dcm2bids`** – converts and sorts DICOMs without downloading them from XNAT:  
   `dcm2bids -c config.json -p 01 -s 01 -o ./ -d ./sourcedata/12345678 --auto_extract_entities`

* **[xnat-utils](https://github.com/Australian-Imaging-Service/xnatutils)**

   * **`xnat-get`** – downloads DICOM files from XNAT; by default, downloads all files from the specified project:  
   `xnat-get -p mj_ris -t ./sourcedata`



## installation
```
python -m venv ./venv
source venv/bin/activate
pip install https://github.com/nencki-lobi/xnat_dcm2bids/archive/refs/heads/master.zip
```

## use (xnat_dcm2bids)

```bash
xnat_dcm2bids [OPTIONS] SESSION_ID SUBJECT_ID SESSION_NUMBER
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

## examples

### Example: run single subject
```
dcm2bids_scaffold -o ./bids-dir
xnat_dcm2bids --bids-dir bids-dir --config ./config.json 55b4c571-cc33-4d pilot2 01
```

### Example: run multiple subjects
First, download CSV list of sessions using `xnat_getcsv`:
```
xnat_getcsv mj_ris.csv mj_ris
```
You will get a file like this:
```
MR ID,Subject_ID,subject,session
23fa0001-b839-40,MJ_RIS_003,003
23fa0001-b839-41,MJ_RIS_004_02,00402
23fa0001-b839-42,MJ_RIS_005_2,0052
```
You can make changes such as editing suggested subject ID or adding session number (not mandatory):
```
MR ID,Subject_ID,subject,session
23fa0001-b839-40,MJ_RIS_003,003,01
23fa0001-b839-41,MJ_RIS_004_02,004,02
23fa0001-b839-42,MJ_RIS_005_2,005,02
```
Finally You can run xnat_dcm2bids in a loop:
```
MacOS/Linux:
while IFS=',' read -r id _ sub ses _; do xnat_dcm2bids --config ./config.json "$id" "$sub" "$ses"; done < subjects.csv
Windows:
for /f "usebackq skip=1 tokens=1,3,4 delims=," %A in ("subjects.csv") do xnat_dcm2bids --config config.json %A %B %C
```

## more 
- [disable gz compression](dcm2niix.md)

- [troubleshooting](troubleshooting.md)



