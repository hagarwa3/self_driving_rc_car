import requests
import sys



"""
This is an independent Python file that just issues the command
to stop the RC car. This is used during the deletion operation
from the PiController object because some library functions are
garbage collected before the stop command can be issued using 
the requests library.
"""


address = sys.argv[1]
requests.post(address + "/speed", data={"speed": "0"})
requests.post(address + "/turn", data={"direction": "forward"})
