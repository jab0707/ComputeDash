import json, psutil, GPUtil, time, pathlib,sys,time,argparse
import ComputeDash.utils.globalParams as gp
import ComputeDash.utils.general_utils as gu
def mainParser():
	parser = argparse.ArgumentParser(add_help=False)
	# add arguments that we may want to change from one simulation to another
	parser.add_argument("--wait_delay", default=gp.WAIT_INTERVAL, type=int,help="")
	parser.add_argument("--repeate_times", default=gp.REPEATE_LIMIT,type=int, help="")
	parser.add_argument("--log_file", default='log.stats', help="")
	parser.add_argument("--verbocity",type=int,default=1,help='Level of verbocity. Higher the level, the more detailed messages. Scale from 0 (no message) to like 4 or something.')
	
	return parser




if __name__ == "__main__":
	parser = mainParser()
	args = parser.parse_args()
	gp.VERBOCITY = args.verbocity
	repeate_num = 0
	while repeate_num < args.repeate_times:
		gu.infoDump(f'Running {repeate_num} of {args.repeate_times}')
		try:
			current_stats = gu.scrape_data()
			gu.updateLogFile(args.log_file,current_stats)
		except:
			gu.infoDump(f'Failed this iter, probably could not find the file',0)
		gu.infoDump(f'Waiting for {args.wait_delay} sec',0)
		
		time.sleep(args.wait_delay)
		repeate_num= repeate_num + 1


