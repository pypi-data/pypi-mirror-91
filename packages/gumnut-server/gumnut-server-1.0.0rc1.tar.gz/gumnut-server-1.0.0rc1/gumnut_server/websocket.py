import os
import signal
import tempfile
from flask import Flask, session
from flask_socketio import SocketIO, emit
from flask_session import Session
from gumnut_simulator.simulator import GumnutSimulator

import logging

logger = logging.getLogger(__name__)


app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(24).hex()
socketio = SocketIO(app, async_mode=None, logger=False, engineio_logger=False, cors_allowed_origins="*")
logging.getLogger("socketio").setLevel(logging.WARNING)
logging.getLogger("engineio").setLevel(logging.WARNING)
logging.getLogger("geventwebsocket").setLevel(logging.WARNING)

app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_FILE_DIR"] = tempfile.gettempdir()
app.config["SESSION_FILE_THRESHOLD"] = 32
Session(app)


def get_simulator():
    """Returns simulator object from session. If no simulator object exists in session it creates a new one"""
    if "simulator" not in session:
        session["simulator"] = GumnutSimulator()
        emit("server", "Created new GumnutSimulator")
    return session["simulator"]


def update():
    simulator = get_simulator()
    emit(
        "update",
        {
            "flags": simulator.get_flags(),
            "register": simulator.get_register(),
            "instr_memory": simulator.get_instruction_memory(),
            "data_memory": simulator.get_data_memory(),
            "io_controller": simulator.get_IO_controller_register(),
            "simulator": simulator.get_simulator_data(),
        },
    )


@socketio.on("reset", namespace="/simulator")
def reset():
    """Resets the simulator state"""
    simulator = get_simulator()
    simulator.reset()
    update()


@socketio.on("setup", namespace="/simulator")
def setup(message):
    """Resets the simulator state and sets up the simulator with the passed assembler source code.

    :param message: JSON string containing data with the field `source` which contains assembler source code, e.g.:

    .. code-block:: json

            {
                    "source":"text\\njmp middle\\norg 0x10\\nfirst:  add r1, r1, 1\\njmp last"
            }

    :type message: str
    """
    simulator = get_simulator()
    simulator.reset()
    simulator.setup(message["source"])
    update()


@socketio.on("step", namespace="/simulator")
def step():
    """Trigger on step of the simulator and return simulator state"""
    simulator = get_simulator()
    simulator.step()
    update()


@socketio.on("IO_input", namespace="/simulator")
def IO_input(message):
    """Sets IO input controller registers of the simulator.

    :param message: JSON string containing data with the field `io_addr_inp` and `io_reg_value`, e.g.:

    .. code-block:: json

            {
                    "io_addr_inp":0,
                    "io_reg_value": 127
            }

    :type message: str
    """
    simulator = get_simulator()
    simulator.set_IO_controller_register(message["io_addr_inp"], message["io_reg_value"])


@socketio.on("ping", namespace="/server")
def ping_pong():
    """Ping/Pong event handler"""
    emit("pong")


def stop(signum, _frame):
    """Stop websocket interface"""
    logger.info("Stopping websocket")
    logger.debug("Reason for stopping: %s (%s)", signal.Signals(signum).name, signum)  # pylint: disable=no-member
    socketio.stop()


def run(host="127.0.0.1", port=5000):
    """Start websocket interface
    \f
    :param port: The port number for the server to listen on. Defaults to `5000`
    :type port: int, optional
    :param host: The hostname or IP address for the server to listen on. Defaults to `127.0.0.1`
    :type host: str, optional
    """
    logger.info("Starting websocket on %s:%s", host, port)

    signal.signal(signal.SIGTERM, stop)
    signal.signal(signal.SIGINT, stop)  # CTRL C
    socketio.run(app, host=host, port=port)
