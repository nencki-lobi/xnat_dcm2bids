import subprocess
import os

def download_session(xnat_id, output_dir, skip_if_exists=True):
    os.makedirs(output_dir, exist_ok=True)
    cmd = ["xnat-get", "-t", output_dir, xnat_id]
    if skip_if_exists:
        cmd.insert(1, "-k")
    subprocess.run(cmd, check=True)
