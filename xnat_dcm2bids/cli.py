import click
from pathlib import Path
from .xnat_utils import download_session
from .dcm2bids import run_dcm2bids
from .fmriprep import repair_all_fieldmaps

@click.command()
@click.argument("session_id")
@click.argument("subject_id")
@click.argument("session_number")
@click.option("--bids-dir", default="./bids-dir", show_default=True, help="Ścieżka do katalogu BIDS")
@click.option("--auto_extract_entities", default=True, show_default=True, help="dcm2bids option i.e. skips run label if not neccesairy")
@click.option("--config", default=None, help="Path to config.json (default: {bids_dir}/code/config.json)")
@click.option("--sourcedata", default=None, help="Path to DICOMs (default: {bids_dir}/sourcedata/{subject_id})")
def main(session_id, subject_id, session_number, bids_dir, config, sourcedata, auto_extract_entities):
    bids_dir = Path(bids_dir)

    if sourcedata is None:
        sourcedata = bids_dir / "sourcedata"
        dicom_dir = sourcedata / session_id
    else:
        sourcedata = Path(sourcedata)
        dicom_dir = sourcedata

    if config is None:
        config = bids_dir / "code" / "config.json"
    else:
        config = Path(config)

    click.echo(f"Pobieram dane do: {sourcedata}")
    download_session(session_id, output_dir=sourcedata)

    click.echo(f"Uruchamiam dcm2bids dla subject {subject_id}, session {session_number}")
    run_dcm2bids(subject_id, session_number, config, bids_dir, dicom_dir , auto_extract_entities)

    click.echo("Naprawiam fieldmapy...")
    repair_all_fieldmaps( bids_dir / f"sub-{subject_id}" )

if __name__ == "__main__":
    main()
