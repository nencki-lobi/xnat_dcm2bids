import click
from pathlib import Path
from .xnat_utils import download_session
from .dcm2bids import run_dcm2bids
from .fmriprep import repair_all_fieldmaps

@click.command(help="This tool downloads XNAT sessions and converts them to BIDS format i.e. {bids-dir}/sub-{subject_id}/ses-{session_number}/..\n"
                    "You can specify multiple XNAT session IDs if a subject's data is split across several sessions.\n"
                    "Data will be automatically downloaded if not already present.\n"
                    "For troubleshooting, visit: https://github.com/nencki-lobi/xnat_dcm2bids/blob/main/troubleshooting.md\n")
@click.argument("xnat_session_ids", nargs=-1)
@click.argument("subject_id")
@click.argument("session_number")
@click.option("--bids-dir", default="./bids-dir", show_default=True, help="BIDS root directory")
@click.option("--config", default=None, help="Path to config.json (default: {bids_dir}/code/config.json)")
@click.option("--sourcedata", default=None, help="Folder where DICOMs will be downloaded (default: {bids_dir}/sourcedata/)")
@click.option("--auto_extract_entities", default=True, show_default=True, help="dcm2bids option i.e. skips run label if not neccesairy")
def main(xnat_session_ids, subject_id, session_number, bids_dir, config, sourcedata, auto_extract_entities):
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
        click.echo(f"Pobieram dane dla sesji xnat: {session_id} do: {sourcedata}")
        download_session(session_id, output_dir=sourcedata)

    click.echo(f"Uruchamiam dcm2bids dla subject {subject_id}, session {session_number}")
    run_dcm2bids(xnat_session_ids, subject_id, session_number, config, bids_dir, sourcedata, auto_extract_entities)

    click.echo("Naprawiam fieldmapy...")
    repair_all_fieldmaps( bids_dir / f"sub-{subject_id}" )

if __name__ == "__main__":
    main()
