from flask import Flask, request, render_template
from flask.ext.cors import CORS
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


@app.route('/turn/', defaults={'path': ''}, methods=['GET'])
def set_speed():
	"""
	This is an endpoint to cause the raspberry pi to turn by some
	real number of degrees.
	"""
    angel = request.args.get('angle')
    print(angle)
    return angle


if __name__ == "__main__":
    # port = int(os.environ.get('PORT', 5000))
    # app.run(host='0.0.0.0', port=port, debug = True)
    app.run(debug = True)