import ComputeDash.utils.globalParams as gp
import json

def readLogFile(logFile):
	with open(logFile) as f:
		stats = json.load(f)
	return stats

def infoDump(message,priority=-1):
	if priority < gp.VERBOCITY:
		print(message)