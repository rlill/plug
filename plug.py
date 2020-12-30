from flask import Flask, request, session, redirect, jsonify, render_template
from gpiozero import LED, Button
import yaml
from functools import partial
import yaml

app = Flask(__name__)

sst = [False] * 8

led = LED(17)
button = Button(2)

config = None


@app.route('/api/v1/login', methods=['POST'])
def api_login():
	return {
		"session": session['_id']
	}

@app.route('/api/v1/switch/<int:port>/<int:status>')
def api_switch(port, status):
	global sst
	if port >= 0 and port <= 8:
		sst[port] = (status != 0)
	if sst[port]:
		led.on()
	else:
		led.off()
	return 'OK'

@app.route('/api/v1/status')
def api_status():
	global sst
	return jsonify(sst)

@app.route('/login', methods=['GET'])
def login():
	return render_template('login.html')

@app.route('/switch')
def switch():
	global sst
	global config
	return render_template('switch.html', sst=sst, ports=config['ports'])

@app.route('/')
def index():
	return '<a href="/switch">switch</a>'

def toggle(port):
	global led
	global sst
	print("toggle ", port)
	sst[port] = not sst[port]
	if sst[port]:
		led.on()
	else:
		led.off()


lock = False

if __name__ == '__main__':
	sst[2] = True

	if not lock:
		lock = True
		button.when_pressed = partial(toggle, 0)

		with open("config.yaml", 'r') as stream:
			try:
				config = yaml.safe_load(stream)
				print(config)
			except yaml.YAMLError as exc:
				print(exc)
				quit()

	app.run(debug=True, host='0.0.0.0', port=80)

