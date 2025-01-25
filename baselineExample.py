import paramiko,json,os,sys,argparse

def infoDump(message,priority=0,args=None):
	if args is None:
		parser = mainParser()
		args = parser.parse_args()
	if priority < args.verbocity:
		print(message)

def mainParser():
	parser = argparse.ArgumentParser(add_help=False)
	# add arguments that we may want to change from one simulation to another
	parser.add_argument("--jumphost", action='store_true', help="")
	parser.add_argument("--configLoc",default='./localConfig.json',help="Config.json location")
	parser.add_argument("--nodes",default='all',help='Which nodes to run on')
	parser.add_argument("--verbocity",type=int,default=1,help='Level of verbocity. Higher the level, the more detailed messages. Scale from 0 (no message) to like 4 or something.')

	return parser

def establish_ssh(host, username, key_path,port=22,socket=None):
	infoDump(f'attemtping to connect to {host} as {username}',1)
	infoDump(f'Config:\n\tKey: {key_path}\n\tPort: {port}',2)
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	try:
		# Connect to the remote server
		ssh.connect(hostname=host, username=username, key_filename=key_path,port=port,sock=socket)
		infoDump('Successful connection',2)
		return ssh
	except:
		infoDump('Failed to connect',-1)
		return None

def fetch_remote_file(ssh_client, remote_file_path, local_file_path):
	"""
	Fetches a file from the remote server via SFTP.

	:param remote_file_path: Path to the file on the remote machine.
	:param local_file_path: Path to save the file locally.
	"""
	# Open an SFTP session and fetch the file
	infoDump(f'Fetching {remote_file_path} to {local_file_path}',2)
	sftp = ssh_client.open_sftp()
	sftp.get(remote_file_path, local_file_path)
	sftp.close()

def format_file_names(node):
	remoteFile = node['BASE_PATH'] + node['LOG_PATH'] + node['LOG_FILE']

	localFile = './'+node['LOG_PATH']+node['LOG_FILE']
	return remoteFile,localFile



def print_results(node,localFile,args):
	with open(localFile) as f:
		stats = json.load(f)
	priority=0
	infoDump(f"Node : {node['LABEL']}:",priority,args)
	infoDump(f"\tCPU   : {stats['cpu']}% loaded",priority,args)
	infoDump(f"\tMEMORY: {stats['memory']}% loaded",priority,args)
	infoDump(f"\tDISK  : {stats['disk']}% loaded",priority,args)
	gpuInfo = ''.join([f"GPU:{g['id']} : {g['load']}% loaded\n\t        " for g in stats['gpu']])
	infoDump(f"\tGPU   : {gpuInfo}",priority,args)
	infoDump('\n',priority,args)

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
		infoDump(f'output from command execution\n{output}',1)
		if error:
			infoDump(f"Error occurred: {error}",-1)
		return output
	except:
		return None
if __name__ == "__main__":
	parser = mainParser()
	args = parser.parse_args()
	infoDump(f'arguments: {args}',3,args)
	with open(args.configLoc) as f:
		config = json.load(f)
	nodesToRun = []

	if args.nodes == 'all':
		nodesToRun = config['NODES'].keys()
	else:
		if args.nodes not in config['NODES'].keys():
			possibleNodes = '\n\t'.join(config["NODES"].keys())
			infoDump(f'Unknown node name {args.node}. I only know about these: {possibleNodes}\n',-1,args)
			sys.exit(1)
		nodesToRun.extend([args.nodes])
	infoDump(f"Running on all of these: {' '.join(nodesToRun)}",3,args)
	for nodeName in nodesToRun:
		node = config['NODES'][nodeName]
		infoDump(f'\n=====Running usage diagnostics on {node["LABEL"]}=====',0,args)
		socket = None
		jump_client=None
		if args.jumphost:
			infoDump('Using jumphost option',2,args)
			jump_client = establish_ssh(config['SSH_INFO']['JUMP_HOST'],
										config['SSH_INFO']['USERNAME'],
										config['SSH_INFO']['KEY_PATH'],
										config['SSH_INFO']["JUMP_PORT"])
			if jump_client is None:
				continue
			jump_transport = jump_client.get_transport()
			destination_addr = (node['HOSTNAME'], 22)
			local_addr = ('127.0.0.1', 0)
			socket = jump_transport.open_channel("direct-tcpip", destination_addr, local_addr)

		ssh_client = establish_ssh(node['HOSTNAME'],
								   config['SSH_INFO']['USERNAME'],
								   config['SSH_INFO']['KEY_PATH'],
								   socket=socket)
		if ssh_client is None:
			if jump_client is not None:
				jump_client.close()
			continue

		script = node['BASE_PATH'] + node['SCRIP_PATH']
		remoteFile,localFile = format_file_names(node)
		subscript_args = [node['INTERP_PATH'],node['BASE_PATH'],remoteFile]
		output = execute_remote_script(ssh_client,script,subscript_args)

		if output is None:
			if jump_client is not None:
				jump_client.close()
			ssh_client.close()
			continue

		

		fetch_remote_file(ssh_client, remoteFile, localFile)

		print_results(node,localFile,args)
		infoDump(f'Done with {node["LABEL"]}\n',0,args)


	
