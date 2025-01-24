import json, psutil, GPUtil, time, pathlib


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
	if len(sys.argv) != 2:
		print("Usage: remote_script.py <statsFile>")
		sys.exit(1)
	statsFile = sys.argv[1]
	pathlib.Path(statsFile).touch()
	current_stats = scrape_data()
	logStats(current_stats,statsFile)