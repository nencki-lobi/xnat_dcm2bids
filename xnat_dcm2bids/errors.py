"""Error handling utilities for xnat-dcm2bids."""

import click
import sys

def handle_xnat_not_configured():
    """Handle case when XNAT is not configured."""
    click.echo("💡 XNAT not configured yet. Run 'xnat-get' to set it up.")
    sys.exit(1)

def handle_error(message, exit_code=1):
    """Handle general errors with a custom message and exit code."""
    click.echo(f"❌ {message}")
    sys.exit(exit_code)
