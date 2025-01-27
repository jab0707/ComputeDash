import json, psutil, GPUtil, time, pathlib,sys,time,argparse
import ComputeDash.utils.globalParams as gp

def mainParser():
	parser = argparse.ArgumentParser(add_help=False)
	# add arguments that we may want to change from one simulation to another
	parser.add_argument("--wait_delay", default=gp.WAIT_INTERVAL, help="")
	parser.add_argument("--repeate_times", default=gp.REPEATE_LIMIT, help="")


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
		if len(sys.argv) != 2:
			print("Usage: remote_script.py <statsFile>")
			sys.exit(1)
		statsFile = sys.argv[1]
		pathlib.Path(statsFile).touch()
		current_stats = scrape_data()
		logStats(current_stats,statsFile)
		time.sleep(args.wait_delay)


