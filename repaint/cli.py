import click

from .core import Repaint
from .server import RepaintServer


@click.group()
def cli():
    pass


@cli.command()
@click.option("--port", help="Port to listen on")
@click.option("--quiet", is_flag=True, help="Don't print anything")
def serve(port, quiet):
    """
    Start the websocket server
    """
    RepaintServer(port=port, quiet=quiet).serve()


@cli.command()
@click.option("--port", help="Port to connect to")
def reload(port):
    Repaint(port=port).reload()
