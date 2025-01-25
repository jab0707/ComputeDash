
import globalParams as gp
import general_utils as gu
import ssh_utils as shu

def format_file_names(node):
	remoteFile = node['BASE_PATH'] + node['LOG_PATH'] + node['LOG_FILE']
	localFile = './'+node['LOG_PATH']+node['LOG_FILE']
	return remoteFile,localFile

class node:
	def __init__(self,loadCheckScript,localLogFile,remoteLogFile,useJumphost=False):
		self.socket = None
		self.jump_client = None
		self.ssh_client = None

		self.loadCheckScript=loadCheckScript
		self.localLogFile=localFile
		self.remoteLogFile=remoteFile
		self.useJumphost=useJumphost

	@classmethod()
	def fromNodeDict(cls,nodeDict):
		script = node['BASE_PATH'] + node['SCRIP_PATH']
		remoteFile,localFile = format_file_names(node)
		scrip_args = [node['INTERP_PATH'],node['BASE_PATH'],remoteFile]
		loadCheckScript = [script,scrip_args]
		return cls(loadCheckScript,localFile,remoteFile)

	

	def update_log_file(self):
		shu.fetch_remote_file(self.ssh_client, self.remoteLogFile, self.localLogFile)

	def run_load_check(self):
		output = shu.execute_remote_script(self.ssh_client,self.loadCheckScript[0],self.loadCheckScript[1:])
		gu.infoDump(f"Remote execution output: {output}",1)

	def establish_connection(self):
		self.socket = None
		self.jump_client = None
		self.ssh_client = None
		try:
			if self.useJumphost:
				gu.infoDump('Using jumphost',2)
				self.jump_client = shu.establish_ssh(config['SSH_INFO']['JUMP_HOST'],
											config['SSH_INFO']['USERNAME'],
											config['SSH_INFO']['KEY_PATH'],
											config['SSH_INFO']["JUMP_PORT"])
				if self.jump_client is None:
					gu.infoDump('Jump host failed gracefully',gp.ERROR_VERBOCITY)
					return 1

				jump_transport = self.jump_client.get_transport()
				destination_addr = (node['HOSTNAME'], 22)
				local_addr = ('127.0.0.1', 0)
				self.socket = jump_transport.open_channel("direct-tcpip", destination_addr, local_addr)

			self.ssh_client = shu.establish_ssh(node['HOSTNAME'],
									   config['SSH_INFO']['USERNAME'],
									   config['SSH_INFO']['KEY_PATH'],
									   socket=self.socket)
		except:
			gu.infoDump('SSH connection failed',gp.ERROR_VERBOCITY)
			return 1
		return 0

	def close_connection(self):
		pass



