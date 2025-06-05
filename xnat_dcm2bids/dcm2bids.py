import subprocess

def run_dcm2bids(subject, session, config, output_dir, dicom_dir, auto_extract=True):
    cmd = [
        "dcm2bids",
        "-p", subject,
        "-s", session,
        "-c", config,
        "-o", output_dir,
        "-d", dicom_dir
    ]
    if auto_extract:
        cmd.insert(1, "--auto_extract_entities")
    subprocess.run(cmd, check=True)
