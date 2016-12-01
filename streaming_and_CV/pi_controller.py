import requests


class PiController:
    def __init__(address="http://192.168.1.11:9876/"):
        self.address = address
        self.last_direction = None
        self.direction = None

    def set_direction(new_directon):
        self.direction = new_directon
        self.last_direction = self.direction

    def check_speed():
        if self.last_direction == "stop" and self.direction != "stop":
            requests.post(bot_url + "/speed", data={"speed": "9"})

    def stop():
        requests.post(bot_url + "/speed", data={"speed": "0"})
        requests.post(bot_url + "/turn", data={"direction": "forward"})
        self.set_direction("stop")

    def right():
        self.check_speed()
        requests.post(bot_url + "/turn", data={"direction": "right"})
        self.set_direction("right")

    def left():
        self.check_speed()
        requests.post(bot_url + "/turn", data={"direction": "left"})
        self.set_direction("left")

    def forwards():
        self.check_speed()
        requests.post(bot_url + "/turn", data={"direction": "forward"})
        self.set_direction("forward")

    def forward_right():
        self.check_speed()
        requests.post(bot_url + "/turn", data={"direction": "forward right"})
        self.set_direction("forward right")

    def forward_left():
        self.check_speed()
        requests.post(bot_url + "/turn", data={"direction": "forward left"})
        self.set_direction("forward left")

    def reverse():
        self.check_speed()
        requests.post(bot_url + "/turn", data={"direction": "reverse"})
        self.set_direction("reverse")
