# flux_manager/consumers.py
import json
import re

from channels.generic.websocket import WebsocketConsumer
from util import execute_command
from util.env_config import workspace_root, bastion_host

fluxInstallConsumer = None
fluxDeleteConsumer = None
fluxCleanConsumer = None


def remove_ansi_escape_codes(input_string):
    """
    Remove ANSI escape codes from a string. There was an issue where
    the command was executed by a user that had fancy features enabled, which added
    ansi escape codes to the output. When echoed back in the browser, it looked horrible.

    Parameters:
    input_string (str): The string that requires cleaning.

    Returns:
    str: The cleaned version of the input_string
    """

    # Define regular expression to match ANSI escape codes
    ansi_escape_regex = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')

    # Remove ANSI escape codes using regular expression
    output_string = ansi_escape_regex.sub('', input_string)

    return output_string


def send_clean_message(consumer, message):
    """
    A clean message is one that can be displyed pleasantly in the browser.

    Parameters:
    consumer (WebsocketConsumer): websocket connection with the browser.
    message (str) : message sent to the browser.

    """

    sanitizedMsg = remove_ansi_escape_codes(message)
    # Send the message to WebSocket
    consumer.send(text_data=json.dumps({
        'stdout': sanitizedMsg,
    }))


def create_kill_cmd(commandToken) -> str:
    return f"kill $(pgrep -P $(cat {workspace_root}/pids/{commandToken}-pid.txt))"


class InstallFluxConsumer(WebsocketConsumer):
    def connect(self):
        global fluxInstallConsumer
        fluxInstallConsumer = self
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        """Receives the command to execute."""
        commandToken = 'flux-install'
        text_data_json = json.loads(text_data)

        version = text_data_json['version']
        cluster = text_data_json['cluster']

        cmd = f"{workspace_root}/ops-core/src/flux-mgmt/flux-install.sh {cluster} {version}"

        execute_command.command_executor(bastion_host,
                                         cmd,
                                         commandToken,
                                         self)

    def command_output_message(self, stdout):
        """The stdout of a command that is echoed back to the web browser."""
        send_clean_message(self, stdout)


class DeleteFluxConsumer(WebsocketConsumer):
    def connect(self):
        global fluxDeleteConsumer
        fluxDeleteConsumer = self
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        """Receives the command to execute."""
        commandToken = 'flux-delete'
        text_data_json = json.loads(text_data)
        cluster = text_data_json['cluster']

        cmd = f"{workspace_root}/ops-core/src/flux-mgmt/flux-delete.sh {cluster}"

        execute_command.command_executor(bastion_host,
                                         cmd,
                                         commandToken,
                                         self)

    def command_output_message(self, stdout):
        """The stdout of a command that is echoed back to the web browser."""
        send_clean_message(self, stdout)
