import json,os,sys,argparse
import ComputeDash.utils.general_utils as gu
import ComputeDash.utils.globalParams as gp
import ComputeDash.remoteQuery.computeNodeMonitor as computeNodeMonitor

gp.ERROR_VERBOCITY=-1#give errors high priority during testing
#This would effectivly suppress errors: globalParams.ERROR_VERBOCITY=100000

def mainParser():
	parser = argparse.ArgumentParser(add_help=False)
	# add arguments that we may want to change from one simulation to another
	parser.add_argument("--jumphost", action='store_true', help="")
	parser.add_argument("--configLoc",default='../../configs/localConfig.json',help="Config.json location")
	parser.add_argument("--nodes",default='all',help='Which nodes to run on')
	parser.add_argument("--verbocity",type=int,default=1,help='Level of verbocity. Higher the level, the more detailed messages. Scale from 0 (no message) to like 4 or something.')

	return parser



if __name__ == "__main__":

	parser = mainParser()
	args = parser.parse_args()
	gp.VERBOCITY = args.verbocity

	gu.infoDump(f'arguments: {args}',3)

	with open(args.configLoc) as f:
		config = json.load(f)
	nodesToRun = []

	if args.nodes == 'all':
		nodesToRun = config['NODES'].keys()
	else:
		if args.nodes not in config['NODES'].keys():
			possibleNodes = '\n\t'.join(config["NODES"].keys())
			gu.infoDump(f'Unknown node name {args.node}. I only know about these: {possibleNodes}\n',-1)
			sys.exit(1)
		nodesToRun.extend([args.nodes])
	gu.infoDump(f"Running on all of these: {' '.join(nodesToRun)}",3)

	for nodeName in nodesToRun:
		gu.infoDump(f'\n=====Cancling jobs on {node.LABEL}=====',0)
		
		if node.establish_connection() != 0:
			gu.infoDump('Failed during connection',gp.ERROR_VERBOCITY)
			continue
		if node.execute_command('pkill -u jbergquist') != 0:
			gu.infoDump('Failed during command execution',gp.ERROR_VERBOCITY)
			continue
		try:
			node.close_connection()


		gu.infoDump(f'Done with {node.LABEL}\n',0)


	
