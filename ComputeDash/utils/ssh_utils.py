import ComputeDash.utils.general_utils as gu
import ComputeDash.utils.globalParams as gp

import paramiko


def establish_ssh(host, username, key_path,port=22,socket=None):
	gu.infoDump(f'Attemtping to connect to {host} as {username}.',1)
	gu.infoDump(f'Config:\n\tHostname: {host}\n\tUser: {username}\n\tKey: {key_path}\n\tPort: {port}',2)
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	try:
		# Connect to the remote server
		ssh.connect(hostname=host, username=username, key_filename=key_path,port=port,sock=socket)
		gu.infoDump('Successful connection',2)
		return ssh
	except:
		gu.infoDump('Failed to connect',gp.ERROR_VERBOCITY)
		return None

def fetch_remote_file(ssh_client, remote_file_path, local_file_path):
	"""
	Fetches a file from the remote server via SFTP.

	:param remote_file_path: Path to the file on the remote machine.
	:param local_file_path: Path to save the file locally.
	"""
	# Open an SFTP session and fetch the file
	try:
		gu.infoDump(f'Fetching remote file.\nRemote: {remote_file_path}\nLocal: {local_file_path}',2)
		sftp = ssh_client.open_sftp()
		sftp.get(remote_file_path, local_file_path)
		sftp.close()
		return 0
	except:
		gu.infoDump('Could not fetch file.',2)
		return 1


def execute_remote_command(ssh_client,command,capture=False):
	output = None
	error = None
	try:
		gu.infoDump(f'Attempting to run:\n{command}',2)
		stdin, stdout, stderr = ssh_client.exec_command(command)

		# Read the output
		output = stdout.read().decode()
		error = stderr.read().decode()
		gu.infoDump(f'output from command execution\n{output}',1)
		if error:
			gu.infoDump(f"Error occurred: {error}",gp.ERROR_VERBOCITY)
			return 1
		return 0
	except Exception as e:
		gu.infoDump(e,gp.ERROR_VERBOCITY)
		return 1

def execute_remote_script(ssh_client, remote_script_path,args=None,prefix=''):
	"""
	Executes a remote script via SSH.

	:param remote_script_path: Path to the script on the remote machine.
	:param args: Arguments to pass to remote script
	:return: Output from the script execution. None if script fails.
	"""
	

	try:
		# Command to execute the remote script
		command = f"{prefix}python3 {remote_script_path} "
		if args is not None:
			command +=  ' '.join(args)
		gu.infoDump(f'Attempting to run:\n{command}',2)
		stdin, stdout, stderr = ssh_client.exec_command(command)

		# Read the output
		output = stdout.read().decode()
		error = stderr.read().decode()
		gu.infoDump(f'output from command execution\n{output}',1)
		if error:
			gu.infoDump(f"Error occurred: {error}",gp.ERROR_VERBOCITY)
			return 1
		return 0
	except:
		return 1