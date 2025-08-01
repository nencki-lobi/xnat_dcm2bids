from pyxnat import Interface
import netrc
import csv
import re
from pathlib import Path


def savecsv(output_path, project_id):
    if not Path("~/.netrc").expanduser().exists():
        click.echo("💡 XNAT not configured yet. Run 'xnat-get' to set it up.")
        return
    
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
        writer = csv.writer(file)
        writer.writerow(['MR ID', 'Subject_ID', 'subject', 'session'])
        
        for data in experiment_data:
            writer.writerow(data)