import flask
import json,os

import ComputeDash.utils.general_utils as gu
import ComputeDash.utils.globalParams as gp
app = flask.Flask(__name__)



@app.route('/')
def main():
	
	stats = gu.readLogFile('../'+gp.LOG_LOC+'wall-e.stats')
	return flask.render_template('testSite.html',LABEL='wall-e',CPU=stats['cpu'],GPU=stats['gpu'])

if __name__=="__main__":
	app.run(host="0.0.0.0",port=5000)