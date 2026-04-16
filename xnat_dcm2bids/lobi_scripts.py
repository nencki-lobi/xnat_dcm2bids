import subprocess
from pathlib import Path

import click

GITHUB_REPO_URL = "https://github.com/nencki-lobi/lobi-mri-scripts.git"
SCRIPTS_DIR = Path.home() / "lobi-mri-scripts"


def _placeholder_message(command_name):
    click.echo(f"Command 'lobi_scripts {command_name}' is not implemented yet.")


@click.group(help="Manage scripts from ~/lobi-mri-scripts/")
def lobi_scripts():
    pass


@lobi_scripts.command("install")
def lobi_scripts_install():
    _placeholder_message("install")


@lobi_scripts.command("ls")
def lobi_scripts_ls():
    _placeholder_message("ls")


@lobi_scripts.command("add")
@click.argument("script_name")
@click.argument("destination", required=False, default="./")
def lobi_scripts_add(script_name, destination):
    _ = (script_name, destination)
    _placeholder_message("add")


@lobi_scripts.command("update")
def lobi_scripts_update():
    _placeholder_message("update")


@lobi_scripts.command("diff")
@click.argument("script_name")
@click.argument("remote_script_name", required=False)
def lobi_scripts_diff(script_name, remote_script_name):
    _ = (script_name, remote_script_name)
    _placeholder_message("diff")


@click.command(help="Run script from ~/lobi-mri-scripts/")
@click.argument("script_name")
@click.argument("args", nargs=-1)
def lobi_script(script_name, args):
    script_path = SCRIPTS_DIR / script_name

    if not SCRIPTS_DIR.exists():
        click.echo(f"🛑 Directory {SCRIPTS_DIR} does not exist")
        subprocess.run(
            ["git", "clone", GITHUB_REPO_URL, str(SCRIPTS_DIR)],
            check=True,
        )
        click.echo("✅ Scripts cloned.")

    if script_name == "ls":
        click.echo(f"Scripts in {SCRIPTS_DIR}:")
        for script in sorted(SCRIPTS_DIR.glob("*.sh")):
            click.echo(f"{script.name}")
        for script in sorted(SCRIPTS_DIR.glob("*/*.sh")):
            click.echo(f"{script.parent.name}/{script.name}")
        return

    if not script_path.exists():
        click.echo(f"🛑 Script {script_name} does not exist in {SCRIPTS_DIR}")
        raise SystemExit(1)

    script_path.chmod(script_path.stat().st_mode | 0o111)

    cmd = f"{script_path} {' '.join(args)}"
    click.echo(f"▶️  Running: bash -l -c \"{cmd}\"")

    try:
        subprocess.run(["bash", "-l", "-c", cmd], check=True)
    except subprocess.CalledProcessError as e:
        click.echo(f"🛑 Error running script: {e.returncode}")
        raise SystemExit(e.returncode)
