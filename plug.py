from flask import Flask, request, session, redirect, jsonify, render_template
from gpiozero import LED, Button
import yaml
from functools import partial

app = Flask(__name__)

sst = [False] * 8

led = LED(17)
button = Button(2)

lock = False

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
	return render_template('switch.html', sst=sst)

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

if __name__ == '__main__':
	sst[2] = True

	if not lock:
		lock = True
		button.when_pressed = partial(toggle, 0)
#		button.when_released = togg2

	app.run(debug=True, host='0.0.0.0', port=80)

