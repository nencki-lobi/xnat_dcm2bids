import click
from pathlib import Path
from .xnat_utils import download_session
from .dcm2bids import run_dcm2bids
from .fmriprep import repair_all_fieldmaps
from .savecsv import savecsv


@click.command(help="This tool downloads XNAT sessions and converts them to BIDS format i.e. {bids-dir}/sub-{subject_id}/ses-{session_number}/..\n"
                    "You can specify multiple XNAT session IDs if a subject's data is split across several sessions.\n"
                    "Data will be automatically downloaded if not already present.\n"
                    "For troubleshooting, visit: https://github.com/nencki-lobi/xnat_dcm2bids/blob/main/troubleshooting.md\n")
@click.argument("xnat_session_ids", nargs=-1)
@click.argument("subject_id")
@click.argument("session_number")
@click.option("--bids-dir", default="./bids-dir", show_default=True, help="BIDS root directory")
@click.option("--config", default=None, help="Path to config.json (default: {bids_dir}/code/config.json)")
@click.option("--sourcedata", default=None, help="Each XNAT session is downloaded to a separate folder in this directory (default: {bids_dir}/sourcedata/)")
@click.option("--auto_extract_entities", default=True, show_default=True, help="dcm2bids option i.e. skips run label if not neccesairy")
def xnat_dcm2bids(xnat_session_ids, subject_id, session_number, bids_dir, config, sourcedata, auto_extract_entities):
    bids_dir = Path(bids_dir)

    if sourcedata is None:
        sourcedata = bids_dir / "sourcedata"
    else:
        sourcedata = Path(sourcedata)

    if config is None:
        config = bids_dir / "code" / "config.json"
    else:
        config = Path(config)

    for session_id in xnat_session_ids:
        click.echo(f"🟢 Downloading {session_id} to {sourcedata}")
        download_session(session_id, output_dir=sourcedata)

    for session_id in xnat_session_ids:
        if not (sourcedata / session_id ).exists():
            click.echo(f"🛑 {session_id} not available for conversion. Skipping session...")
            return
        
    click.echo(f"🟢 Running dcm2bids for subject {subject_id}, session {session_number}")
    run_dcm2bids(xnat_session_ids, subject_id, session_number, config, bids_dir, sourcedata, auto_extract_entities)

    click.echo("🟢 Repairing fieldmaps...")
    repair_all_fieldmaps( bids_dir / f"sub-{subject_id}" )

@click.command(help="Download list of sessions from XNAT project and save to CSV")
@click.argument("output_csv", type=click.Path())
@click.argument("project_id", type=click.STRING)
def save_csv(output_csv, project_id):
    #download list of sessions from xnat
    savecsv(output_csv, project_id)
    click.echo(f"🟢 Data saved to {output_csv}")
    
