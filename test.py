import paramiko
import logging

from modules.ssh_session import create_ssh_session

# Enable Paramiko logging for debugging
# logging.basicConfig(level=logging.DEBUG)

command_hostname = "cat /etc/hostname"

# def create_ssh_session(hostname, username, keyfile):
#     client = paramiko.SSHClient()
#     client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#
#     key = paramiko.RSAKey.from_private_key_file(keyfile)
#     client.connect(hostname, port=22, username='root', pkey=key)
#     return client


# Example usage
hostname = '192.168.4.60'
username = 'root'
keyfile = '/Users/gsingh/.ssh/id_rsa'
keyfile_4k = '/Users/gsingh/.ssh/id_rsa'
# create_ssh_session(hostname,keyfile,keyfile_4k)

ssh = create_ssh_session(hostname,keyfile=keyfile, keyfile_4k=keyfile_4k)

# Execute a command (optional)
stdin, stdout, stderr = ssh.exec_command(command_hostname)
print(stdout.read().decode())

# Close the connection
stdin.close()
stdout.close()
stderr.close()
ssh.close()