from flask import Flask, render_template, Response, send_file
import streaming
import urllib.request
import numpy as np
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


def gen():
    """
    generates frames to send to front end
    calls our streaming code for streaming in the frames and processing them
    """
    global im_bytes
    #list of urls that could exist for the stream
    evanURL = 'http://192.168.1.10/live'
    URL = 'http://192.168.1.3:8080/video'
    urlIllinoisNet = 'http://10.194.9.154:8080/video'
    evanUrlIllinoisNet = 'http://10.192.224.222/live'

    stream = urllib.request.urlopen(evanURL)
    im_bytes = bytes()

    #while loop helps it keep streaming
    while True:
        frame, im_bytes = streaming.processIncoming(im_bytes, stream)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed')
def video_feed():
    """
    Endpoint for the video stream of the processed image
    """
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route("/loadFile/<path:path>", methods=['GET'])
def loadFile(path):
    return send_file('templates/'+path)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True)
