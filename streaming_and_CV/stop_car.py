import requests
import sys


address = sys.argv[1]
requests.post(address + "/speed", data={"speed": "0"})
requests.post(address + "/turn", data={"direction": "forward"})
