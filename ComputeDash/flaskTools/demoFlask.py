import flask
import json,os

app = flask.Flask(__name__)

CONFIG_LOC='../remoteQuery/localConfig.json'
BASE_PATH='../'

@app.route('/')
def main():
	with open(CONFIG_LOC) as f:
		config = json.load(f)
		
	return flask.render_template('testSite.html')

if __name__=="__main__":
	app.run(host="0.0.0.0",port=5000)