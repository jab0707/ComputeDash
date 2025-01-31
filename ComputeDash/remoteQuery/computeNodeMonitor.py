
import ComputeDash.utils.globalParams as gp
import ComputeDash.utils.general_utils as gu
import ComputeDash.utils.ssh_utils as shu
import json,os

def check_for_config(func):
	def wrapper(self, *args, **kwargs):
		# Check the attribute value
		if not getattr(self, "_isConfiged"): 
			gu.infoDump(f'Cannot {func.__name__} without first configuring ssh info',gp.ERROR_VERBOCITY)
			return
		return func(self, *args, **kwargs)
	return wrapper

class node:
	def __init__(self,attributes,useJumphost=False):
		self.socket = None
		self.jump_client = None
		self.ssh_client = None

		#config info, set my self.setupConfig
		#ssh info
		self.jumphost = None
		self.username = None
		self.keypath = None
		self.jumpport = None
		#log path info
		self.localLogFile=None
		self.remoteLogFile=None

		for key in attributes.keys():
			setattr(self,key,attributes[key])

		self._isConfiged =False



	def setupConfig(self,sshConfig,localConfig,remoteTargetScript='remote_script.py'):
		#ssh info
		self.jumphost = sshConfig['JUMP_HOST']
		self.username = sshConfig['USERNAME']
		self.keypath = sshConfig['KEY_PATH']
		self.jumpport = sshConfig['JUMP_PORT']

		#log file locations
		self.localLogFile = localConfig['BASE_PATH'] + localConfig['LOG_PATH'] + self.LOG_FILE
		self.remoteLogFile = self.BASE_PATH + self.LOG_PATH + self.LOG_FILE
		
		#remote script location and arguments
		wrapping_script = self.BASE_PATH + self.SCRIP_PATH
		remoteScript = os.path.dirname(wrapping_script) + '/' + remoteTargetScript
		scrip_args = ['--interpreter', self.INTERP_PATH,'--remote_script', remoteScript,'--log_file',self.remoteLogFile]
		wrappingScript = [wrapping_script]
		wrappingScript.extend(scrip_args)
		self.wrappingScript = wrappingScript


		self._isConfiged = True
		gu.infoDump('Config set',1)

	@check_for_config
	def remove_remote_log_file(self):
		output = 0
		if shu.execute_remote_command(self.ssh_client,f'ls {self.remoteLogFile}') == 0:#check if it exists first
			output = shu.execute_remote_command(self.ssh_client,f'rm {self.remoteLogFile}')
		return output

	@check_for_config
	def update_log_file(self,cleanRemote=True):
		gu.infoDump('Fetching log file to local machine',1)
		fetchResult = shu.fetch_remote_file(self.ssh_client, self.remoteLogFile, self.localLogFile)
		if fetchResult == 1:
			return fetchResult
		output=0
		if cleanRemote:
			gu.infoDump('Cleaning remote log file',1)
			output = self.remove_remote_log_file()
		return output

	@check_for_config
	def run_remote_scirpt(self,additionalArgs=None,prefix=''):
		gu.infoDump(f'Sending the following command:\n{prefix}{self.wrappingScript}{additionalArgs}',2)
		args = self.wrappingScript[1:]
		if additionalArgs is not None:
			args.extend(additionalArgs)
		return shu.execute_remote_script(self.ssh_client,self.wrappingScript[0],args,prefix=prefix)
		

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
				destination_addr = (self.HOSTNAME, 22)
				local_addr = ('127.0.0.1', 0)
				self.socket = jump_transport.open_channel("direct-tcpip", destination_addr, local_addr)

			self.ssh_client = shu.establish_ssh(self.HOSTNAME,
												self.username,
												self.keypath,
												socket=self.socket)
		except:
			gu.infoDump('SSH connection failed',gp.ERROR_VERBOCITY)
			return 1
		if self.ssh_client:
			return 0
		return 1

	def print_log_info(self,logFile=None,stats=None):
		if logFile is None:
			logFile = self.localLogFile
		try:
			gu.infoDump(f'Attempting to read log:\n\t{logFile}')
			with open(logFile) as f:
				stats = json.load(f)
			priority=0
			gu.infoDump(f"Node : {self.LABEL}:",priority)
			gu.infoDump(f"\tCPU   : {stats['cpu']}% loaded",priority)
			gu.infoDump(f"\tMEMORY: {stats['memory']}% loaded",priority)
			gu.infoDump(f"\tDISK  : {stats['disk']}% loaded",priority)
			
			gpuIds = [g['id'] for g in stats['gpu'][0]]
			gpuLoads = [[] for _ in gpuIds]
			
			for log in stats['gpu']:

				for gpuIx in range(len(gpuIds)):
					gpuLoads[gpuIx].extend([log[gpuIx]['load']])
			
			gpuInfo = ''.join([f"GPU:{gpuIds[ix]} : {gpuLoads[ix]}% loaded\n\t        " for ix in range(len(gpuIds))])
			if len(gpuInfo)>1:
				gu.infoDump(f"\tGPU   : {gpuInfo}",priority)
		except Exception as e:
			gu.infoDump(e,gp.ERROR_VERBOCITY)
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



