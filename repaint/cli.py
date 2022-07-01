import click

from .core import Repaint


@click.group()
def cli():
    pass


@cli.command()
@click.option("--port", default=8765, help="Port to listen on")
def serve(port):
    """
    Start the websocket server
    """
    Repaint(port=port).server.serve()


@cli.command()
@click.option("--port", default=8765, help="Port to connect to")
def reload(port):
    Repaint(port=port).reload()
