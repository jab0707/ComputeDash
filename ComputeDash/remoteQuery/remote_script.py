import json, psutil, GPUtil, time, pathlib,sys,argparse,datetime
import ComputeDash.utils.general_utils as gu

def mainParser():
	parser = argparse.ArgumentParser(add_help=False)
	# add arguments that we may want to change from one simulation to another
	parser.add_argument("--log_file", default='log.stats', help="")

	

	return parser
def scrape_data():
	stats = {
		"cpu":[psutil.cpu_percent(interval=1)],
		"memory": [psutil.virtual_memory().percent],
        "disk": [psutil.disk_usage('/').percent],
        "gpu": [[{"id": gpu.id, "load": gpu.load * 100} for gpu in GPUtil.getGPUs()]],
        "time":[datetime.datetime.now()]
	}
	return stats

if __name__ == "__main__":
	parser = mainParser()
	args, otherArgs = parser.parse_known_args()
	pathlib.Path(args.log_file).touch()
	current_stats = scrape_data()
	gu.updateLogFile(current_stats,args.log_file)