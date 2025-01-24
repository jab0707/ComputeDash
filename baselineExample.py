import paramiko,json,os


def establish_ssh(host, username, key_path):
	print(f'attemtping to connect to {host} as {username}')
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	try:
		# Connect to the remote server
		ssh.connect(hostname=host, username=username, key_filename=key_path)
		print('Success')
		return ssh
	except:
		print('Failed to connect')
		return None

def fetch_remote_file(ssh_client, remote_file_path, local_file_path):
	"""
	Fetches a file from the remote server via SFTP.

	:param remote_file_path: Path to the file on the remote machine.
	:param local_file_path: Path to save the file locally.
	"""

   
	# Open an SFTP session and fetch the file
	sftp = ssh_client.open_sftp()
	sftp.get(remote_file_path, local_file_path)
	sftp.close()

def format_file_names(node):
	remoteFile = node['BASE_PATH'] + node['LOG_PATH'] + node['LOG_FILE']

	localFile = './'+node['LOG_PATH']+node['LOG_FILE']
	return remoteFile,localFile



def print_results(node,localFile):
	with open(localFile) as f:
		stats = json.load(f)
	print(f"Node : {node['LABEL']}:")
	print(f"\tCPU   : {stats['cpu']}% loaded")
	print(f"\tMEMORY: {stats['memory']}% loaded")
	print(f"\tDISK  : {stats['disk']}% loaded")
	gpuInfo = ''.join([f"GPU:{g['id']} : {g['load']}% loaded\n\t        " for g in stats['gpu']])
	print(f"\tGPU   : {gpuInfo}")
	print('\n')
def execute_remote_script(ssh_client, remote_script_path,args=None):
	"""
	Executes a remote script via SSH.

	:param remote_script_path: Path to the script on the remote machine.
	:return: Output from the script execution.
	"""
	

	try:
		# Command to execute the remote script
		command = f"python3 {remote_script_path} {' '.join(args)}"
		stdin, stdout, stderr = ssh_client.exec_command(command)

		# Read the output
		output = stdout.read().decode()
		error = stderr.read().decode()
		print(f'output from command execution\n{output}')
		if error:
			print(f"Error occurred: {error}")
		return output
	except:
		return None
if __name__ == "__main__":

	with open('localConfig.json') as f:
		config = json.load(f)

	for node in config['NODES']:
		print(f'Running usage diagnostics on {node["LABEL"]}')
		ssh_client = establish_ssh(node['HOSTNAME'],config['SSH_INFO']['USERNAME'],config['SSH_INFO']['KEY_PATH'])
		if ssh_client is None:
			continue
		script = node['BASE_PATH'] + node['SCRIP_PATH']
		remoteFile,localFile = format_file_names(node)
		args = [node['INTERP_PATH'],node['BASE_PATH'],remoteFile]
		output = execute_remote_script(ssh_client,script,args)
		if output is None:
			ssh_client.close()
			continue

		

		fetch_remote_file(ssh_client, remoteFile, localFile)

		print_results(node,localFile)
		print(f'Done with {node["LABEL"]}')


	
