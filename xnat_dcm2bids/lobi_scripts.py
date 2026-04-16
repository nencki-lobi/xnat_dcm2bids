import shutil
import subprocess
from pathlib import Path

import click

GITHUB_REPO_URL = "https://github.com/nencki-lobi/lobi-mri-scripts.git"
SCRIPTS_DIR = Path.home() / "lobi-mri-scripts"


def _print_intro():
    click.echo("lobi_scripts")
    click.echo("")
    click.echo("Scripts from the lobi-mri-scripts GitHub repository used in our MRI data analysis workflow.")
    click.echo(GITHUB_REPO_URL)
    click.echo("")
    click.echo("Available commands:")
    click.echo("  lobi_scripts install - clone the scripts repository to ~/lobi-mri-scripts")
    click.echo("  lobi_scripts ls - list available scripts from the repository")
    click.echo("  lobi_scripts add <script_name> [destination] - copy a selected script to the current or chosen directory")
    click.echo("  lobi_scripts update - update the lobi_mri_scripts repository with git stash and git pull")
    click.echo("  lobi_scripts diff <local_copy> [repository_script_name] - compare a local file with its repository version")


def _require_scripts_dir():
    if not SCRIPTS_DIR.exists():
        click.echo(f"🛑 Directory {SCRIPTS_DIR} does not exist. Run 'lobi_scripts install' first.")
        raise SystemExit(1)


def _iter_available_scripts():
    for script in sorted(SCRIPTS_DIR.glob("*.sh")):
        yield script.name
    for script in sorted(SCRIPTS_DIR.glob("*/*.sh")):
        yield f"{script.parent.name}/{script.name}"


def _find_remote_script_path(script_name):
    direct_path = SCRIPTS_DIR / script_name
    if direct_path.exists():
        return direct_path

    script_basename = Path(script_name).name

    top_level_match = SCRIPTS_DIR / script_basename
    if top_level_match.exists():
        return top_level_match

    for script_path in sorted(SCRIPTS_DIR.glob("*/*.sh")):
        if script_path.name == script_basename:
            return script_path

    return None


def _install_scripts_repo():
    if SCRIPTS_DIR.exists():
        click.echo(f"🟡 Directory {SCRIPTS_DIR} already exists")
        return

    click.echo(f"🟢 Cloning {GITHUB_REPO_URL} to {SCRIPTS_DIR}")
    subprocess.run(
        ["git", "clone", GITHUB_REPO_URL, str(SCRIPTS_DIR)],
        check=True,
    )
    click.echo("✅ Scripts cloned.")


@click.group(invoke_without_command=True)
@click.pass_context
def lobi_scripts(ctx):
    if ctx.invoked_subcommand is None:
        _print_intro()


@lobi_scripts.command("install")
def lobi_scripts_install():
    try:
        _install_scripts_repo()
    except subprocess.CalledProcessError as e:
        click.echo(f"🛑 Error installing scripts repository: {e.returncode}")
        raise SystemExit(e.returncode)


@lobi_scripts.command("ls")
def lobi_scripts_ls():
    _require_scripts_dir()
    click.echo(f"Scripts in {SCRIPTS_DIR}:")
    for script_name in _iter_available_scripts():
        click.echo(script_name)


@lobi_scripts.command("add")
@click.argument("script_name")
@click.argument("destination", required=False, default="./")
def lobi_scripts_add(script_name, destination):
    _require_scripts_dir()

    source_path = SCRIPTS_DIR / script_name
    if not source_path.exists():
        click.echo(f"🛑 Script {script_name} does not exist in {SCRIPTS_DIR}")
        raise SystemExit(1)

    destination_dir = Path(destination).expanduser()
    destination_dir.mkdir(parents=True, exist_ok=True)
    destination_path = destination_dir / Path(script_name).name

    shutil.copy2(source_path, destination_path)
    click.echo(f"✅ Copied {script_name} to {destination_path}")


@lobi_scripts.command("update")
def lobi_scripts_update():
    _require_scripts_dir()

    try:
        click.echo(f"🟢 Updating {SCRIPTS_DIR}")
        subprocess.run(["git", "-C", str(SCRIPTS_DIR), "stash"], check=True)
        subprocess.run(["git", "-C", str(SCRIPTS_DIR), "pull"], check=True)
        click.echo("✅ Repository updated.")
    except subprocess.CalledProcessError as e:
        click.echo(f"🛑 Error updating scripts repository: {e.returncode}")
        raise SystemExit(e.returncode)


@lobi_scripts.command("diff")
@click.argument("script_name")
@click.argument("remote_script_name", required=False)
def lobi_scripts_diff(script_name, remote_script_name):
    _require_scripts_dir()

    local_path = Path(script_name).expanduser()
    remote_name = remote_script_name or local_path.name
    remote_path = _find_remote_script_path(remote_name)

    if not local_path.exists():
        click.echo(f"🛑 Local file {local_path} does not exist")
        raise SystemExit(1)

    if remote_path is None:
        click.echo(f"🛑 Remote script {remote_name} does not exist in {SCRIPTS_DIR}")
        raise SystemExit(1)

    result = subprocess.run(
        ["diff", "-u", str(local_path), str(remote_path)],
        check=False,
        capture_output=True,
        text=True,
    )

    if result.returncode == 0:
        click.echo("✅ Files are the same.")
        return

    if result.returncode == 1:
        click.echo(result.stdout, nl=False)
        return

    click.echo(result.stderr.strip() or "🛑 Error running diff")
    raise SystemExit(result.returncode)
