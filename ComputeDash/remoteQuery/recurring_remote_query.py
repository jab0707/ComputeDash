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


def scrape_data():
	stats = {
		"cpu":psutil.cpu_percent(interval=1),
		"memory": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage('/').percent,
        "gpu": [{"id": gpu.id, "load": gpu.load * 100} for gpu in GPUtil.getGPUs()],
        "time":time.time()
	}
	return stats


if __name__ == "__main__":
	parser = mainParser()
	args = parser.parse_args()
	gp.VERBOCITY = args.verbocity
	repeate_num = 0
	while repeate_num < args.repeate_times:
		current_stats = scrape_data()
		gu.updateLogFile(args.log_file,current_stats)
		gu.infoDump(f'Waiting for {args.wait_delay} sec',1)
		time.sleep(args.wait_delay)
		repeate_num= repeate_num + 1


