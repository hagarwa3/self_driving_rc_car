from flask import Flask, render_template, Response
import streaming
import urllib.request
import numpy as np
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def gen():
	global bytes
	evanURL = 'http://192.168.1.10/live'
	URL = 'http://192.168.1.3:8080/video'
	urlIllinoisNet = 'http://10.194.9.154:8080/video'
	stream = urllib.request.urlopen(URL)
	bytes = bytes()
	while True:
		frame, bytes = streaming.processIncoming(URL, bytes, stream)
		yield (b'--frame\r\n'
		       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True)