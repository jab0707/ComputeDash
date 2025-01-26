import json,os,sys,argparse
import general_utils as gu
import ssh_utils as shu
import globalParams
import computeNodeMonitor

globalParams.ERROR_VERBOCITY=-1#give errors high priority during testing
#This would effectivly suppress errors: globalParams.ERROR_VERBOCITY=100000

def mainParser():
	parser = argparse.ArgumentParser(add_help=False)
	# add arguments that we may want to change from one simulation to another
	parser.add_argument("--jumphost", action='store_true', help="")
	parser.add_argument("--configLoc",default='./localConfig.json',help="Config.json location")
	parser.add_argument("--nodes",default='all',help='Which nodes to run on')
	parser.add_argument("--verbocity",type=int,default=1,help='Level of verbocity. Higher the level, the more detailed messages. Scale from 0 (no message) to like 4 or something.')

	return parser



if __name__ == "__main__":

	parser = mainParser()
	args = parser.parse_args()
	globalParams.VERBOCITY = args.verbocity

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
		nodeDict = config['NODES'][nodeName]
		node = computeNodeMonitor.node(nodeDict)
		node.setupConfig(config['SSH_INFO'],config['LOCAL_INFO'])
		node.useJumphost = args.jumphost
		gu.infoDump(f'\n=====Running usage diagnostics on {node.label}=====',0)
		
		if node.establish_connection() != 0:
			gu.infoDump('Failed during connection',globalParams.ERROR_VERBOCITY)
			continue
		if node.run_load_check() != 0:
			gu.infoDump('Failed during load check',globalParams.ERROR_VERBOCITY)
			continue
		if node.update_log_file() != 0:
			gu.infoDump('Failed during log update',globalParams.ERROR_VERBOCITY)
			continue
		if node.print_log_info() != 0:
			gu.infoDump('Failed during log report',globalParams.ERROR_VERBOCITY)
			continue
		node.close_connection()


		gu.infoDump(f'Done with {node.label}\n',0)


	
