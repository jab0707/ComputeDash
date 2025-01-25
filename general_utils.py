import globalParams

def infoDump(message,priority=-1):
	if priority < globalParams.VERBOCITY:
		print(message)