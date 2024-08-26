# flux_manager/consumers.py
import json
import re

from channels.generic.websocket import WebsocketConsumer
from util import execute_command
from util.env_config import workspace_root

fluxInstallConsumer = None
fluxDeleteConsumer = None
fluxCleanConsumer = None

# Function to remove ANSI escape codes from a string
def remove_ansi_escape_codes(input_string):
    # Define regular expression to match ANSI escape codes
    ansi_escape_regex = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')

    # Remove ANSI escape codes using regular expression
    output_string = ansi_escape_regex.sub('', input_string)

    return output_string

def send_clean_message(consumer, message):
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
            
            cmd = f"{workspace_root}/capzu/src/flux-mgmt/flux-install-std-offering.sh {tenant} {cluster} {branch}"             
                
            execute_command.command_executor('desktop.msp.capstonec.net', 
                                             cmd, 
                                             commandToken,
                                             self)

    
    def command_output_message(self, stdout):
        """The stdout of a command that is echoed back to the web browser."""
        send_clean_message(self, stdout)
        
class DeleteFluxConsumer(WebsocketConsumer):
    def connect(self):
        global fluxInstallConsumer
        fluxInstallConsumer = self
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        """Receives the command to execute."""
        commandToken = 'flux-delete'
        text_data_json = json.loads(text_data)
        if 'kill' in text_data_json:
            execute_command.command_executor('desktop.msp.capstonec.net', 
                                             create_kill_cmd(commandToken), 
                                             commandToken + '-kill',
                                             self)       
        else: 
            tenant = text_data_json['tenant']
            cluster = text_data_json['cluster']
            stage = text_data_json['stage']
            
            if stage == 'plan':
                cmd = f"{workspace_root}/capzu/src/flux-mgmt/flux-delete-plan.sh {tenant} {cluster}"
            elif stage == 'apply':
                cmd = f"{workspace_root}/capzu/src/flux-mgmt/flux-delete-apply.sh {tenant} {cluster}"               
                
            execute_command.command_executor('desktop.msp.capstonec.net', 
                                             cmd, 
                                             commandToken,
                                             self)

    
    def command_output_message(self, stdout):
        """The stdout of a command that is echoed back to the web browser."""
        send_clean_message(self, stdout)
        
class CleanFluxConsumer(WebsocketConsumer):
    def connect(self):
        global fluxInstallConsumer
        fluxInstallConsumer = self
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        """Receives the command to execute."""
        commandToken = 'flux-clean'
        text_data_json = json.loads(text_data)
        if 'kill' in text_data_json:
            execute_command.command_executor('desktop.msp.capstonec.net', 
                                             create_kill_cmd(commandToken), 
                                             commandToken + '-kill',
                                             self)       
        else: 
            tenant = text_data_json['tenant']
            cluster = text_data_json['cluster']
            
            cmd = f"{workspace_root}/capzu/src/flux-mgmt/flux-clean.sh {tenant} {cluster}"
                
            execute_command.command_executor('desktop.msp.capstonec.net', 
                                             cmd, 
                                             commandToken,
                                             self)

    
    def command_output_message(self, stdout):
        """The stdout of a command that is echoed back to the web browser."""
        send_clean_message(self, stdout)