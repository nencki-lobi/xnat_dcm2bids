import subprocess
from pathlib import Path
import click
import netrc
import csv
import re
from pyxnat import Interface
from . import errors

def meta_from_repr_impl(exp):
    """
    Ekstrakcja metadanych tak jak w __repr__, ale:
    - bez zliczania scans/resources (duży koszt),
    - w jednym zapytaniu dzięki 'columns'.
    Zwraca: dict z insert_date (timestamp), subject/system/labels itp.
    """
    intf = exp._intf
    eid = exp.id()            # jak w __repr__
    # Jeden strzał do XNAT Array z wybranymi kolumnami
    cols = ['xsiType', 'label', 'project', 'subject_id', 'subject_label', 'insert_date']
    row = intf.array.experiments(experiment_id=eid, columns=cols).data
    if not row:
        # fallback – bardzo rzadkie
        return {
            "exp_sys": eid,
            "exp_lbl": exp.label(),
            "project": None,
            "subject_id": None,
            "subject_lbl": None,
            "insert_date": None,
        }
    row = row[0]
    return {
        "exp_sys": eid,
        "exp_lbl": row.get('label'),
        "project": row.get('project'),
        "subject_id": row.get('subject_id'),
        "subject_lbl": row.get('subject_label'),
        "insert_date": row.get('insert_date'),  # to jest to, co __repr__ drukuje po "created on"
    }

def download_session(xnat_id, output_dir, skip_if_exists=True):
    if not Path("~/.netrc").expanduser().exists():
        errors.handle_xnat_not_configured()
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    cmd = ["xnat-get", "-t", output_dir, xnat_id]
    if skip_if_exists:
        cmd.insert(1, "-k")
    subprocess.run(cmd, check=True)

def savecsv(output_path, project_id):
    if not Path("~/.netrc").expanduser().exists():
        errors.handle_xnat_not_configured()
    
    auth_data = netrc.netrc()
    first_host = next(iter(auth_data.hosts))
    USERNAME, _, PASSWORD = auth_data.authenticators(first_host)

    XNAT_URL = f"https://{first_host}"
    PROJECT = project_id

    xnat = Interface(server=XNAT_URL, user=USERNAME, password=PASSWORD)
    experiments = xnat.select.project(PROJECT).experiments()

    # Prepare experiment data for sorting
    experiment_data = []

    # for exp in experiments:
    #     xnat_id = exp.label()
    #     subject = exp.parent()
    #     subject_id = subject.label()
    #     date = exp.attrs.get('xnat:experimentData/date')
    #     time = exp.attrs.get('xnat:experimentData/time')
    #     guess_code = re.sub(r'\D', '', subject_id)
        
    #     experiment_data.append((xnat_id, subject_id, date, time, guess_code))
    
    for exp in experiments:
        meta = meta_from_repr_impl(exp)
    
        xnat_id    = meta["exp_lbl"]          # etykieta sesji
        subject_id = meta["subject_lbl"]      # np. MJ_RIS_003 (to, co drukuje repr)
        insert_dt  = meta["insert_date"]      # pełny timestamp jak w "created on ..."
        
        #match sub and ses from subject_id
        parts = re.split(r'[_\-\s]+', subject_id or '')
        # skip first element eg ad25a; convert remaining parts to numeric
        numeric_parts = [re.sub(r'[A-Za-z]', '', part) for part in parts[1:]]
        # remove empty strings
        numeric_parts = [part for part in numeric_parts if part]

        if numeric_parts:
            guess_code = numeric_parts[0]
            guess_sess = numeric_parts[1] if len(numeric_parts) > 1 else "1"
        else:
            guess_code = "NA"
            guess_sess = "1"

        experiment_data.append((xnat_id, subject_id, insert_dt, guess_code, guess_sess))

    if len(experiment_data) == 0:
        click.echo(f"🛑 No experiments found for project {PROJECT}")
        raise SystemExit(1)

    # Sort the experiment data based on subject_id
    experiment_data.sort(key=lambda x: x[1])

    # Save the sorted list to csv file
    with open(output_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, lineterminator='\n')
        writer.writerow(['MR_ID', 'Patient_ID', 'DateTime', 'sub-XX', 'ses-YY'])
        
        for data in experiment_data:
            writer.writerow(data)
