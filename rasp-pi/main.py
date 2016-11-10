from flask import Flask, request, render_template
from flask_cors import CORS, cross_origin
import message_arduino
import os

app = Flask(__name__)
CORS(app)
cors = CORS(app, resources={"/*": {"origins": "*"}})


@app.route('/speed/', methods=['POST'])
def set_speed():
    """
    This is an endpoint to set the speed of the raspberry pi from 
    an HTTP post request.
    """
    speed = request.args.get('speed')
    print(speed)
    return speed


@app.route('/turn', methods=['GET'])
def set_direction():
    """
    This is an endpoint to cause the raspberry pi to tell the arduino to turn the car in whatever direction
    """
    direction = requestFormat(request.args.get('direction'))
    if direction == "left":
        message_arduino.left()
    elif direction == "right":
        message_arduino.right()
    elif direction == "forward":
        message_arduino.fwd()
    elif direction == "reverse":
        message_arduino.back()
    print(direction)
    return direction

def requestFormat(strInput):
    strInput = strInput.replace("%22", "")
    strInput = strInput.replace('"', "")
    return strInput

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 9876))
    app.run(host='0.0.0.0', port=port, debug = True)