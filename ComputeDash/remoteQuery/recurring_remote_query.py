import json, psutil, GPUtil, time, pathlib,sys,time,argparse
import ComputeDash.utils.globalParams as gp
import ComputeDash.utils.general_utils as gu
def mainParser():
	parser = argparse.ArgumentParser(add_help=False)
	# add arguments that we may want to change from one simulation to another
	parser.add_argument("--wait_delay", default=gp.WAIT_INTERVAL, type=int,help="")
	parser.add_argument("--repeate_times", default=gp.REPEATE_LIMIT,type=int, help="")
	parser.add_argument("--log_file", default='log.stats', help="")
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

def logStats(stats,file):
	with open(file, "w") as f:
		json.dump(stats, f)

if __name__ == "__main__":
	parser = mainParser()
	args = parser.parse_args()
	repeate_num = 0
	while repeate_num < args.repeate_times:
		pathlib.Path(args.log_file).touch()
		current_stats = scrape_data()
		logStats(current_stats,args.log_file)
		gu.infoDump('Waiting for {args.wait_delay} sec',1)
		time.sleep(args.wait_delay)
		repeate_num= repeate_num + 1


