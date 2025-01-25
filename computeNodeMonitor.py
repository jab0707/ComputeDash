
import globalParams as gp
import general_utils as gu
import ssh_utils as shu
import json

def format_file_names(nodeDict):
	remoteFile = nodeDict['BASE_PATH'] + nodeDict['LOG_PATH'] + nodeDict['LOG_FILE']
	localFile = './'+nodeDict['LOG_PATH']+nodeDict['LOG_FILE']
	return remoteFile,localFile

def check_for_config(func):
	def wrapper(self, *args, **kwargs):
		# Check the attribute value
		if not getattr(self, "_isConfiged"): 
			gu.infoDump(f'Cannot {func.__name__} without first configuring ssh info',gp.ERROR_VERBOCITY)
			return
		return func(self, *args, **kwargs)
	return wrapper

class node:
	def __init__(self,label='',hostname='',loadCheckScript='',localLogFile='',remoteLogFile='',useJumphost=False):
		self.socket = None
		self.jump_client = None
		self.ssh_client = None

		self.jumphost = None
		self.username = None
		self.keypath = None
		self.jumpport = None

		self.loadCheckScript=loadCheckScript
		self.localLogFile=localLogFile
		self.remoteLogFile=remoteLogFile
		self.useJumphost=useJumphost
		self.label = label
		self.hostname=hostname

		self._isConfiged =False

	@classmethod
	def fromNodeDict(cls,nodeDict):
		script = nodeDict['BASE_PATH'] + nodeDict['SCRIP_PATH']
		remoteFile,localFile = format_file_names(nodeDict)
		scrip_args = [nodeDict['INTERP_PATH'],nodeDict['BASE_PATH'],remoteFile]
		loadCheckScript = [script]
		loadCheckScript.extend(scrip_args)
		label = nodeDict['LABEL']
		hostname = nodeDict['HOSTNAME']
		return cls(label,hostname,loadCheckScript,localFile,remoteFile)

	def setupConfig(self,config):
		self.jumphost = config['JUMP_HOST']
		self.username = config['USERNAME']
		self.keypath = config['KEY_PATH']
		self.jumpport = config['JUMP_PORT']
		self._isConfiged = True
		gu.infoDump('Config set',1)

	@check_for_config
	def update_log_file(self):
		return shu.fetch_remote_file(self.ssh_client, self.remoteLogFile, self.localLogFile)

	@check_for_config
	def run_load_check(self):
		gu.infoDump(f'Sending the following command:\n{self.loadCheckScript}',2)
		return shu.execute_remote_script(self.ssh_client,self.loadCheckScript[0],self.loadCheckScript[1:])
		

	@check_for_config
	def establish_connection(self):
		self.socket = None
		self.jump_client = None
		self.ssh_client = None
		try:
			if self.useJumphost:
				gu.infoDump('Using jumphost',2)
				self.jump_client = shu.establish_ssh(self.jumphost,
											self.username,
											self.keypath,
											self.jumpport)
				gu.infoDump('Jump host returned. Moving to main host',2)
				if self.jump_client is None:
					gu.infoDump('Jump host failed gracefully',gp.ERROR_VERBOCITY)
					return 1

				jump_transport = self.jump_client.get_transport()
				destination_addr = (self.hostname, 22)
				local_addr = ('127.0.0.1', 0)
				self.socket = jump_transport.open_channel("direct-tcpip", destination_addr, local_addr)

			self.ssh_client = shu.establish_ssh(self.hostname,
												self.username,
												self.keypath,
												socket=self.socket)
		except:
			gu.infoDump('SSH connection failed',gp.ERROR_VERBOCITY)
			return 1
		return 0

	def print_log_info(self):
		try:
			gu.infoDump(f'Attempting to read local log:\n\t{self.localLogFile}')
			with open(self.localLogFile) as f:
				stats = json.load(f)
			priority=0
			gu.infoDump(f"Node : {self.label}:",priority)
			gu.infoDump(f"\tCPU   : {stats['cpu']}% loaded",priority)
			gu.infoDump(f"\tMEMORY: {stats['memory']}% loaded",priority)
			gu.infoDump(f"\tDISK  : {stats['disk']}% loaded",priority)
			gpuInfo = ''.join([f"GPU:{g['id']} : {g['load']}% loaded\n\t        " for g in stats['gpu']])
			gu.infoDump(f"\tGPU   : {gpuInfo}",priority)
			gu.infoDump('\n',priority)
		except:
			return 1
		return 0
	@check_for_config
	def close_connection(self):
		if self.jump_client is not None:
			self.jump_client.close()
		if self.ssh_client is not None:
			self.ssh_client.close()
		self.ssh_client = None
		self.jump_client = None



