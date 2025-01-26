ComputeDash
A tool for querying compute node usage statistics

Current working example:
first download this repo both locally and in a centralized location accessible to all compute nodes that you plan to run it on

next, confgure the localConfig.json (you can store this outside of the repo and point at it later)
Params are:
```json
{
"SSH_INFO":{ //Info about your ssh identity
	"USERNAME":"<ssh log in username>",
	"KEY_PATH":"<path/to/a/ssh/private/key>",
	"JUMP_HOST":"<jump host (if needed)>",
	"JUMP_PORT":"<jump port (if needed)>"
},
"NODES":{
	"<name of compute node>":{
	"HOSTNAME":"<host.name.of.node>",
	"INTERP_PATH":"<path/to/python/venv/interpreter>",
	"LABEL":"<a label>",
	"BASE_PATH":"<path/to/this/repo/locally/on/this/machine/>",
	"LOG_PATH":"<path/where/logs/should/be/written/referenced/to/BASE_PATH/>",
	"SCRIP_PATH":"remote_wrapper.py",//this is probably the script you want
	"LOG_FILE":"<name of log file for this node>"
	}
}
```
the INTERP_PATH is a path to a python interpreter which has the following packaged:
json, psutil, GPUtil, setuptools
(requirements.txt file to follow)
I usue a virtual environment for this, but it can also be the default if those packages are installed globally. But I doubt that is the case across all machines soo.....


locally the maching calling things will need a python env with the following packages:
paramiko

Then just run the baselineExample like so:
```bash
python3 baselineExample.py --jumphost --configLoc <path/to/config.json> --verbocity 1 --nodes "all"
```

### TODO:
- Add more metrics
- Set up periodic logging
- Set up updating visualization of logs (flask?)
- Other stuff
- Better error handling/exception detials
- Documentation I guess



