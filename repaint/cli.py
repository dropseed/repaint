import click

from .core import Repaint


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
    Repaint(port=port, quiet=quiet).server.serve()


@cli.command()
@click.option("--port", help="Port to connect to")
def reload(port):
    Repaint(port=port).reload()
