import subprocess, sys, os




# Read the interpreter path from settings.yaml


if __name__=="__main__":

	if len(sys.argv)!=4:
		print("That didn't work")
		sys.exit(1)
	interpreter=sys.argv[1]
	basePath = sys.argv[2]
	args = sys.argv[3:]
	# Pass all arguments to the main script
	command = [interpreter, basePath+'remote_script.py', *args]
	print(f'Attmepting to run like so:\n{' '.join(command)} ')
	subprocess.run(command)