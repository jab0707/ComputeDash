import flask
import json,os

import ComputeDash.utils.general_utils as gu
import ComputeDash.utils.globalParams as gp
import ComputeDash.flaskTools.flask_utils as fu
from types import FunctionType


app = flask.Flask(__name__)

with open('../'+gp.CONFIG_LOC+'localConfig.json') as f:
	config = json.load(f)


pages=[]
for node in config['NODES'].keys():
	print(f"checking for : {node}")
	if os.path.isfile('../'+gp.LOG_LOC+f'{node}.npy'):
		page_code = compile(f'def {node.replace("-","_")}(): return fu.node_page("{node}")', "<string>", "exec")
		page_func = FunctionType(page_code.co_consts[0], globals(), f"{node}")
		pages.append(page_func.__name__)
		print(page_func.__name__)
		app.route(f'/{node}')(page_func)
	else:
		print(f'Node not found')

@app.route('/')
def main():
	return flask.render_template('main.html',NODES=pages)










if __name__=="__main__":
	app.run(host="0.0.0.0",port=5000)