import yaml, subprocess, sys, os




# Read the interpreter path from settings.yaml
def pullConfig():
    with open('remoteConfig.yaml', 'r') as f:
        config = yaml.safe_load(f)
    return config

if __name__=="__main__":
    config = pullConfig()
    interpreter = config['VENV_INTERPRETER']

    if not os.isdir(config['STATS_DIR']):
        os.mkdir(config['STATS_DIR'])
    args = [config['DEFAULT_STATS_FILE']]
    if len(sys.argv>1):
        args = sys.argv[1:]
    # Pass all arguments to the main script
    subprocess.run([interpreter, 'remote_script.py', *args])