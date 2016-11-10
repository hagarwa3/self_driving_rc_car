from flask import Flask, request, render_template
from flask_cors import CORS, cross_origin
import ArduinoController
import os

app = Flask(__name__)
CORS(app)
cors = CORS(app, resources={"/*": {"origins": "*"}})

#This path migth vary. Make sure to update before use
serialPath = "/dev/serial/by-path/platform-bcm2708_usb-usb-0:1.4:1.0-port0"
conn = ArduinoController.ArduinoController(serialPath)


@app.route('/speed/', methods=['GET'])
def set_speed():
    """
    This is an endpoint to set the speed of the raspberry pi from 
    an HTTP post request.
    speed will be a tag in the request and will be a number in the range 0-9
    """
    try:
        speed = int(requestFormat(request.args.get('speed')))
        if speed<0 or speed>9:
            return "Not a valid speed"
        conn.set_speed(speed)
        return speed
    except:
        return "Expected number between 0-9"


@app.route('/turn', methods=['GET'])
def set_direction():
    """
    This is an endpoint to cause the raspberry pi to tell the arduino to turn the car in whatever direction
    """
    direction = requestFormat(request.args.get('direction'))
    if direction == "left":
        conn.turn_left()
    elif direction == "right":
        conn.turn_right()
    elif direction == "forward":
        conn.move_forward()
    elif direction == "reverse":
        conn.move_backward()
    print(direction)
    return direction

def requestFormat(strInput):
    """
    formats incoming requests to remove quotation marks
    """
    strInput = strInput.replace("%22", "")
    strInput = strInput.replace('"', "")
    return strInput

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 9876))
    app.run(host='0.0.0.0', port=port, debug = True)