import subprocess
from pathlib import Path

def run_dcm2bids(session_ids, subject, session, config, output_dir, sourcedata, auto_extract=True):
    cmd = [
        "dcm2bids",
        "-p", subject,
        "-s", session,
        "-c", config,
        "-o", output_dir
    ]

    for session_id in session_ids:
        cmd.extend(["-d", str(sourcedata / session_id)])

    if auto_extract:
        cmd.insert(1, "--auto_extract_entities")
    
    subprocess.run(cmd, check=True)
