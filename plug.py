from flask import Flask, request, session, redirect, jsonify, render_template, url_for
from gpiozero import LED, Button
import yaml
from functools import partial
import multiprocessing as mp
import ctypes
import hashlib

class PlugFlaskApp(Flask):
	def run(self, host='0.0.0.0', port=80, debug=None, load_dotenv=True, **options):
		super(PlugFlaskApp, self).run(host=host, port=port, debug=debug, load_dotenv=load_dotenv, **options)

app = PlugFlaskApp(__name__)
app.secret_key = 'pr*WATsfFm9a"M_RJbsMm9j;\hH:=(,^EGftHX/_L</BrWXTbFY&wgQRh]dg2^\!R>djVbe7APC&d(='

sst = None
config = None

def toggle(si):
	global sst
	global config
	sst[si] = not sst[si]
	gpio = config['ports'][si]['gpio']
	if sst[si]:
		gpio.on()
	else:
		gpio.off()

def setup_app(app):
	global config
	global sst
        
	with open("config.yaml", 'r') as stream:
		try:
			config = yaml.safe_load(stream)
		except yaml.YAMLError as exc:
			print(exc)
			quit()
	si = 0
	for port in config['ports']:
		port['gpio'] = LED(port['gpio_actor'])

		port['button'] = Button(port['gpio_button'])
		port['button'].when_pressed = partial(toggle, si)

		si = si + 1

	sst = mp.Array(ctypes.c_bool, len(config['ports']))

setup_app(app)

@app.route('/api/v1/login', methods=['POST'])
def api_login():
	global config
	username = request.form.get('username', None)
	password = hashlib.md5(request.form.get('password', None).encode('utf-8')).hexdigest()

	print('login user:', username, ' password:', password)

	for user in config['users']:
		if user['name'] == username and user['password'] == password:
			print('user matched: ', user)
			session['username'] = user['name']
			return 'OK'
	return "Unauthorized", 400

@app.route('/api/v1/switch/<int:port>/<int:status>')
def api_switch(port, status):
	global sst
	global config
	if port >= 0 and port < len(config['ports']):
		un = session['username'] if 'username' in session else ''
		if 'ALL' in config['ports'][port]['permission'] or un in config['ports'][port]['permission']:
			sst[port] = (status != 0)
			gpio = config['ports'][port]['gpio']
			if sst[port]:
				gpio.on()
			else:
				gpio.off()
	return 'OK'

@app.route('/api/v1/status')
def api_status():
	global sst
	lsst = sst[:].copy()
	return jsonify(lsst)

@app.route('/login', methods=['GET'])
def login():
	return render_template('login.html')

@app.route('/logout', methods=['GET'])
def logout():
	session.pop('username', None)
	return redirect(url_for('switch'))

@app.route('/switch')
def switch():
	global sst
	return render_template('switch.html', sst=sst, ports=config['ports'])

@app.route('/')
def index():
	return '<a href="/switch">switch</a>'

if __name__ == '__main__':
	app.run()

