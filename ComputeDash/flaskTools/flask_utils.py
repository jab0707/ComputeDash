import flask
import json,os

import ComputeDash.utils.general_utils as gu
import ComputeDash.utils.globalParams as gp




def node_page(nodeId):
	print('Loading data')
	logHistory = gu.readLogHistory('../'+gp.LOG_LOC+f'{nodeId}.npy')
	time=[str(t) for t in logHistory[-1,:]]
	cpu = logHistory[0,:].tolist()
	memory = logHistory[1,:].tolist()
	disk = logHistory[2,:].tolist()
	num_gpu = int(logHistory[3,1])
	gpu_ids = logHistory[4:4+num_gpu,0].tolist()
	gpu = logHistory[4+num_gpu:4+num_gpu+num_gpu,:].tolist()
	print(f'sending lots of data. {logHistory.shape}')
	return flask.render_template('testSite.html',LABEL=nodeId,CPU=cpu,MEMORY=memory,DISK=disk,GPU=gpu,TIME=time)