import flask
import json,os,argparse

import ComputeDash.utils.general_utils as gu
import ComputeDash.utils.globalParams as gp
import ComputeDash.flaskTools.flask_utils as fu
from types import FunctionType


def mainParser():
	parser = argparse.ArgumentParser(add_help=False)
	# add arguments that we may want to change from one simulation to another
	parser.add_argument("--configLoc",default='../../configs/localConfig.json',help="Config.json location")
	parser.add_argument("--logLoc",default='../../logs/',help="Config.json location")
	return parser



def createApp(args):

	app = flask.Flask(__name__)

	with open(args.configLoc) as f:
		config = json.load(f)


	pages=[]
	for node in config['NODES'].keys():
		print(f"checking for : {node}")
		if os.path.isfile(args.logLoc+f'/{node}.npy'):
			page_code = compile(f'def {node.replace("-","_")}(): return fu.node_page("{node}","{args.logLoc}")', "<string>", "exec")
			page_func = FunctionType(page_code.co_consts[0], globals(), f"{node}")
			pages.append(page_func.__name__)
			print(page_func.__name__)
			app.route(f'/{node}')(page_func)
		else:
			print(f'Node not found')

	@app.route('/')
	def main():
		return flask.render_template('main.html',NODES=pages)

	return app










if __name__=="__main__":
	parser = mainParser()
	args = parser.parse_args()
	app=createApp(args)
	app.run(host="0.0.0.0",port=5000)