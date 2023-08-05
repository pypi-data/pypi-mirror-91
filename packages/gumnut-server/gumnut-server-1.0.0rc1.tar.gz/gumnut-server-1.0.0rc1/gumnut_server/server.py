from gumnut_server import __version__
import sys
import click
import logging
from logging.handlers import RotatingFileHandler
import tempfile
from pathlib import Path

logger = logging.getLogger(__name__)


@click.version_option(prog_name="gumnut-server", version=__version__)
@click.group()
def server():
    """Provide an interface for gumnut-simulator
    \f
    Provides the entry point for CLI usage"""

    logger = logging.getLogger()  # pylint:disable=redefined-outer-name
    logger.setLevel(logging.DEBUG)

    # Create rotating file handler with DEBUG level
    temp_dir = Path(tempfile.gettempdir())
    fh = RotatingFileHandler(filename=temp_dir / "gumnut_server.log", maxBytes=1024 * 1024, backupCount=3)
    fh.setLevel(logging.DEBUG)

    # Create console handler with a INFO level
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    # Create formatters and add them to the handlers
    formatter_simple = logging.Formatter("%(asctime)s | %(levelname)-8s | %(name)s | %(message)s")
    formatter_detail = logging.Formatter("%(asctime)s | %(levelname)-8s | %(name)s %(module)s:%(lineno)d | %(message)s")
    fh.setFormatter(formatter_detail)
    ch.setFormatter(formatter_simple)

    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)

    logger.debug("gumnut-server %s", __version__)
    logger.info("gumnut-server %s", __version__)
    logger.warning("gumnut-server %s", __version__)
    logger.error("gumnut-server %s", __version__)
    logger.critical("gumnut-server %s", __version__)


@server.command()
@click.option("-h", "--host", default="127.0.0.1", type=str, help="Host for communication", show_default=True)
@click.option("-p", "--port", default=5000, type=int, help="Port for communication", show_default=True)
def websocket(host, port):
    """Run server in websocket mode
    \f
    :param port: The port number for the server to listen on. Defaults to `5000`
    :type port: int, optional
    :param host: The hostname or IP address for the server to listen on. Defaults to `127.0.0.1`
    :type host: str, optional
    """
    from gumnut_server import websocket as ws

    try:
        ws.run(host, port)
    except Exception as e:  # pylint: disable=broad-except
        logging.error("Unhandled exception:")
        logging.error(e, exc_info=True)
        logger.critical("There was an unhandled exception. Stopping now!")
        sys.exit(1)
