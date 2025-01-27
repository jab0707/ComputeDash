import json, psutil, GPUtil, time, pathlib,sys,argparse,datetime
import ComputeDash.utils.general_utils as gu

def mainParser():
	parser = argparse.ArgumentParser(add_help=False)
	# add arguments that we may want to change from one simulation to another
	parser.add_argument("--log_file", default='log.stats', help="")

	

	return parser


if __name__ == "__main__":
	parser = mainParser()
	args, otherArgs = parser.parse_known_args()
	current_stats = gu.scrape_data()
	gu.updateLogFile(args.log_file,current_stats)