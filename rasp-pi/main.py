from flask import Flask, request, render_template
from flask_cors import CORS, cross_origin
app = Flask(__name__)
CORS(app)
cors = CORS(app, resources={"/*": {"origins": "*"}})


@app.route('/speed/', defaults={'path': ''}, methods=['POST'])
def set_speed():
    """
    This is an endpoint to set the speed of the raspberry pi from 
    an HTTP post request.
    """
    speed = request.args.get('speed')
    print(speed)
    return speed


@app.route('/turn/', defaults={'path': ''}, methods=['POST'])
def set_direction():
    """
    This is an endpoint to cause the raspberry pi to turn in some direction. 
    Exact implementation to be figured out with an actual arduino.
    """
    direction = request.args.get('direction')
    """
    if direction == "left":
        arduino execute left turn
    elif direction == "right":
        arduino execute right turn
    elif direction == "forward":
        arduino move forward
    elif direction == "reverse":
        arduino move backwards
    """
    print(direction)
    return direction


if __name__ == "__main__":
    # port = int(os.environ.get('PORT', 5000))
    # app.run(host='0.0.0.0', port=port, debug = True)
    app.run(debug = True)