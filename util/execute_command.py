import threading
import paramiko
import os
import subprocess

from channels.generic.websocket import WebsocketConsumer
from .env_config import workspace_root


def command_executor(host, command, commandToken, cmdConsumer: WebsocketConsumer):
    """ Execute the given command in another thread. """
    threading.Thread(target=execute_command, args=(
        host, command, commandToken, cmdConsumer)).start()


def execute_command(host, command, commandToken, cmdConsumer: WebsocketConsumer):
    """ Execute the given command on a remote machine via SSH. """

    # Add the setup required for any command.
    commandSetup = f"export OPS_WORKSPACE_ROOT={workspace_root}; \"$OPS_WORKSPACE_ROOT\"/ops-core/src/util/update-workspace.sh"
    # Create the final command, with common setup prepended.
    command = f"{commandSetup}; {command}"
    cmdConsumer.command_output_message('COMMAND: ' + command + '\n')

    # Execute the command on the bastion server.
    execute_command_on_bastion(host, command, cmdConsumer)


def execute_command_on_bastion(host, command, cmdConsumer):
    if host == 'localhost':
        execute_locally(command, cmdConsumer)
    else:
        execute_via_ssh(host, command, cmdConsumer)


def execute_locally(command, cmdConsumer):
    # Open the process and run the script in the background
    scriptContents = f"""#!/usr/bin/env bash   
    {command}
    """

    runScript = '/tmp/ops-pilot-exe-command.sh'

    # Write the commands to the script file
    with open(runScript, "w") as script_file:
        script_file.write(scriptContents)

    # Make the script executable
    os.chmod(runScript, 0o755)

    process = subprocess.Popen(
        [runScript],
        stdout=subprocess.PIPE,  # Redirect stdout
        stderr=subprocess.PIPE,  # Redirect stderr
        text=True  # Ensure the output is treated as text (not bytes)
    )

    # Continuously read and print the output as it is produced
    try:
        while True:
            output = process.stdout.readline()
            if output == "" and process.poll() is not None:
                break
            if output:
                cmdConsumer.command_output_message(output)

        # Print any errors that occurred
        cmdConsumer.command_output_message("\n===== STDERR =======\n")
        stderr = process.stderr.read()
        if stderr:
            cmdConsumer.command_output_message(stderr)

    except Exception as e:
        cmdConsumer.command_output_message("\n\nERROR: {e}")
        print(f"ERROR: {e}")


def execute_via_ssh(host, command, cmdConsumer):
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
    cmdConsumer.command_output_message(
        f"COMMAND EXIT STATUS : {exit_status}\n")
    # Close the SSH connection
    ssh.close()


def get_ssh_client(host):
    ssh = paramiko.SSHClient()

    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(
        host, username=os.environ['DESKTOP_USER'], password=os.environ['DESKTOP_PASS'])
    return ssh
