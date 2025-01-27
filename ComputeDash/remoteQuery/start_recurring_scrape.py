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
	parser.add_argument("--wait_delay", default=gp.WAIT_INTERVAL, help="")
	parser.add_argument("--repeate_times", default=gp.REPEATE_LIMIT, help="")

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
		nodeDict = config['NODES'][nodeName]
		node = computeNodeMonitor.node(nodeDict)
		node.setupConfig(config['SSH_INFO'],config['LOCAL_INFO'],'recurring_remote_query.py')

		node.useJumphost = args.jumphost
		gu.infoDump(f'\n=====Running usage diagnostics on {node.LABEL}=====',0)
		
		if node.establish_connection() != 0:
			gu.infoDump('Failed during connection',gp.ERROR_VERBOCITY)
			continue
		if node.run_remote_scirpt(['--wait_delay',f'{args.wait_delay}','--verbocity',{args.verbocity},'--repeate_times',args.repeate_times, f"> ~/{node.LABEL}.log 2>&1", '&'],prefix='nohup ') != 0:
			gu.infoDump('Failed during load check',gp.ERROR_VERBOCITY)
			continue
		node.close_connection()


		gu.infoDump(f'Done with {node.LABEL}\n',0)


	
