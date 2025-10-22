import subprocess
from pathlib import Path
from . import errors

def prepare_paths(output_dir, sourcedata, config):
    bids_dir = Path(output_dir)

    sourcedata = Path(sourcedata) if sourcedata else bids_dir / "sourcedata"
    config = Path(config) if config else bids_dir / "code" / "config.json"

    if not config.exists():
        errors.handle_error(f"Config file not found at {config}")

    return bids_dir, sourcedata, config

def run_dcm2bids(session_ids, subject, session, config, output_dir, sourcedata, auto_extract=True):
    cmd = [
        "dcm2bids",
        "-p", subject,
        "-s", session,
        "-c", config,
        "-o", output_dir,
        "-d"
    ] + [str(sourcedata / s) for s in session_ids]

    if auto_extract:
        cmd.insert(1, "--auto_extract_entities")
    
    subprocess.run(cmd, check=True)
