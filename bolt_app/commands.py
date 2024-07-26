from flask import Blueprint
import click

from .utils import ingest_file

commands = Blueprint("commands", __name__)


@commands.cli.command("ingest")
@click.argument("filename")
def ingest(filename):
    print(f"Ingesting {filename}")
    ingest_file(filename)
