import subprocess, sys, os




# Read the interpreter path from settings.yaml


if __name__=="__main__":

	if len(sys.argv!=3):
		print("That didn't work")
		sys.exit(1)
	interpreter=sys.argv[1]
	args = sys.argv[2:]
	# Pass all arguments to the main script
	command = [interpreter, 'remote_script.py', *args]
	print(f'Attmepting to run like so:\n{' '.join(command)} ')
	subprocess.run(command)