import subprocess
from pathlib import Path
import click
import netrc
import csv
import re
from pyxnat import Interface
from . import errors

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

    for exp in experiments:
        xnat_id = exp.label()
        subject = exp.parent()
        subject_id = subject.label()
        guess_code = re.sub(r'\D', '', subject_id)
        
        experiment_data.append((xnat_id, subject_id, guess_code))

    # Sort the experiment data based on subject_id
    experiment_data.sort(key=lambda x: x[1])

    # Save the sorted list to csv file
    with open(output_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, lineterminator='\n')
        writer.writerow(['MR ID', 'Subject_ID', 'subject', 'session'])
        
        for data in experiment_data:
            writer.writerow(data)
