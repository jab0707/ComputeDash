import flask
import json,os

import ComputeDash.utils.general_utils as gu
import ComputeDash.utils.globalParams as gp
app = flask.Flask(__name__)



@app.route('/')
def main():
	
	logHistory = gu.readLogHistory('../'+gp.LOG_LOC+'zagreus.npy')
	time=[str(ix) for ix in range(logHistory.shape[1])]
	cpu = logHistory[0,:].tolist()
	memory = logHistory[1,:].tolist()
	disk = logHistory[2,:].tolist()
	num_gpu = int(logHistory[3,1])
	gpu_ids = logHistory[4:4+num_gpu,0].tolist()
	gpu = logHistory[4+num_gpu:4+num_gpu+num_gpu,:].tolist()
	print(f'sending:\n{cpu}\n{memory}\n{disk}\n{gpu_ids}\n{gpu}\n{time}')
	return flask.render_template('testSite.html',LABEL='zagreus',CPU=cpu,MEMORY=memory,DISK=disk,GPU=gpu,TIME=time)

if __name__=="__main__":
	app.run(host="0.0.0.0",port=5000)