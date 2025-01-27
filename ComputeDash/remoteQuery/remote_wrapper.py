import subprocess, sys, os, argparse

def mainParser():
	parser = argparse.ArgumentParser(add_help=False)
	# add arguments that we may want to change from one simulation to another
	parser.add_argument("--interpreter", default='python3', help="")
	parser.add_argument("--remote_script", default='remote_script.py', help="")
	

	return parser


if __name__=="__main__":
	parser = mainParser()
	args, otherArgs = parser.parse_known_args()
	
	# Pass all arguments to the main script
	command = [args.interpreter, args.remote_script]
	command.extend(otherArgs)
	print(f'Attmepting to run like so:\n{' '.join(command)} ')
	subprocess.run(command)
	print('Done')