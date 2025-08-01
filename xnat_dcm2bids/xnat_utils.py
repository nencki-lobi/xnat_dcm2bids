import subprocess
from pathlib import Path
import click

def download_session(xnat_id, output_dir, skip_if_exists=True):
    if not Path("~/.netrc").expanduser().exists():
        click.echo("💡 XNAT not configured yet. Run 'xnat-get' to set it up.")
        return
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    cmd = ["xnat-get", "-t", output_dir, xnat_id]
    if skip_if_exists:
        cmd.insert(1, "-k")
    subprocess.run(cmd, check=True)
