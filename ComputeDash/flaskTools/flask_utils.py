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
	num_gpu = int((logHistory.shape[0] - 4) /2)
	gpu_ids = logHistory[3:3+num_gpu,0].tolist()
	gpu = logHistory[3+num_gpu:3+num_gpu+num_gpu,:].tolist()
	print('sending lots of data:')
	print(f'\tcpu    : {len(cpu)}')
	print(f'\tmemory : {len(memory)}')
	print(f'\tdisk   : {len(disk)}')
	print(f'\tnum_gpu: {num_gpu}')
	print(f'\tgpu_ids: {len(gpu_ids)}')
	print(f'\tgpu    : {len(gpu)}')
	print(f'\ttime   : {len(time)}')
	return flask.render_template('testSite.html',LABEL=nodeId,CPU=cpu,MEMORY=memory,DISK=disk,GPU=gpu,TIME=time)