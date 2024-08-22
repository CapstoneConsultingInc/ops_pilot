import threading
import paramiko
import os

from channels.generic.websocket import WebsocketConsumer
from .env_config import workspace_root

def command_executor(host, command, commandToken, cmdConsumer:WebsocketConsumer):
    """ Execute the given command in another thread. """
    threading.Thread(target=execute_command, args=(host, command, commandToken, cmdConsumer)).start()

def execute_command(host, command, commandToken, cmdConsumer:WebsocketConsumer):
    """ Execute the given command on a remote machine via SSH. """

    # Add the setup required for any command.
    commandSetup = f"export FLUXOPS_WORKSPACE_ROOT={workspace_root}; \"$FLUXOPS_WORKSPACE_ROOT\"/capzu/src/util/update-workspace.sh"
    commandSetup = f"{commandSetup};mkdir -p {workspace_root}/pids; echo $$ > {workspace_root}/pids/{commandToken}-pid.txt"
    # Create the final command, with common setup prepended.
    command = f"{commandSetup}; {command}"
    cmdConsumer.command_output_message('COMMAND: ' + command + '\n')
    ssh = get_ssh_client(host)
    
    # Execute the command
    stdin, stdout, stderr = ssh.exec_command(command)
    stdin.close()

    # While there's standard output, forward it to the browser.
    for line in iter(lambda: stdout.readline(2048), ""):
        # Send the output to the WebSocket
        cmdConsumer.command_output_message(line)
    
    # Send the standard error to the browser    
    cmdConsumer.command_output_message("\n===== STDERR =======\n")
    for line in iter(lambda: stderr.readline(2048), ""):
        # Send the output to the WebSocket
        cmdConsumer.command_output_message(line)

    exit_status = stdout.channel.recv_exit_status()
    cmdConsumer.command_output_message(f"COMMAND EXIT STATUS : {exit_status}\n")
    # Close the SSH connection
    ssh.close()

def get_ssh_client(host):
    ssh = paramiko.SSHClient()
    
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, username=os.environ['DESKTOP_USER'], password=os.environ['DESKTOP_PASS'])
    return ssh