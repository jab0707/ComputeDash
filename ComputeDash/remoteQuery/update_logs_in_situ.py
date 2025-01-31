import ComputeDash.utils.general_utils as gu
import ComputeDash.utils.globalParams as gp

import json,os,sys,argparse,time
import ComputeDash.utils.general_utils as gu
import ComputeDash.utils.globalParams as gp
import ComputeDash.remoteQuery.computeNodeMonitor as computeNodeMonitor

gp.ERROR_VERBOCITY=-1#give errors high priority during testing
#This would effectivly suppress errors: globalParams.ERROR_VERBOCITY=100000

def mainParser():
	parser = argparse.ArgumentParser(add_help=False)
	# add arguments that we may want to change from one simulation to another
	parser.add_argument("--configLoc",default='../../configs/localConfig.json',help="Config.json location")
	parser.add_argument("--nodes",default='all',help='Which nodes to run on')
	parser.add_argument("--verbocity",type=int,default=1,help='Level of verbocity. Higher the level, the more detailed messages. Scale from 0 (no message) to like 4 or something.')
	parser.add_argument("--wait_delay", default=gp.WAIT_INTERVAL,type=int, help="")
	parser.add_argument("--repeate_times", default=gp.REPEATE_LIMIT,type=int, help="")

	return parser



if __name__ == "__main__":

	parser = mainParser()
	args = parser.parse_args()
	gp.VERBOCITY = args.verbocity

	gu.infoDump(f'arguments: {args}',3)

	with open(args.configLoc) as f:
		config = json.load(f)
	nodesToRun = []
	repeate_num = 0
	if args.nodes == 'all':
		nodesToRun = config['NODES'].keys()
	else:
		if args.nodes not in config['NODES'].keys():
			possibleNodes = '\n\t'.join(config["NODES"].keys())
			gu.infoDump(f'Unknown node name {args.node}. I only know about these: {possibleNodes}\n',-1)
			sys.exit(1)
		nodesToRun.extend([args.nodes])
	allNodes=[]
	for nodeName in nodesToRun:
		nodeDict = config['NODES'][nodeName]
		node = computeNodeMonitor.node(nodeDict)
		node.setupConfig(config['SSH_INFO'],config['LOCAL_INFO'],'')
		allNodes.append(node)
	while repeate_num < args.repeate_times:
		repeate_num +=1
		gu.infoDump(f"Running on all of these: {' '.join(nodesToRun)}",3)
		for node in allNodes:
			gu.infoDump(f'\n=====Running usage diagnostics on {node.LABEL}=====',0)
			try:
				gu.infoDump('reading log',0)
				log = gu.readLogFile(node.localLogFile,pop=True)#pop causes us to delete the local log
				node.print_log_info()
				gu.infoDump('Writting as binary',0)
				gu.writeLogHistory(node.localLogFile.replace('.stats','.npy'),log)
			except Exception as e:
				gu.infoDump(f'Error encountered in {node.LABEL}:\n{e}\n')
			gu.infoDump(f'Done with {node.LABEL}\n',0)

		gu.infoDump(f'Sleeping for {args.wait_delay} sec\n',0)
		time.sleep(args.wait_delay)

