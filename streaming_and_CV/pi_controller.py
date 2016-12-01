import requests


class PiController:
    def __init__(self, address="http://192.168.1.11:9876/"):
        self.address = address
        self.last_direction = None
        self.direction = None

    def set_direction(self, new_directon):
        self.direction = new_directon
        self.last_direction = self.direction

    def check_speed(self):
        if self.last_direction == "stop" and self.direction != "stop":
            requests.post(self.address + "/speed", data={"speed": "9"})

    def stop(self):
        requests.post(self.address + "/speed", data={"speed": "0"})
        requests.post(self.address + "/turn", data={"direction": "forward"})
        self.set_direction("stop")

    def right(self):
        self.check_speed()
        requests.post(self.address + "/turn", data={"direction": "right"})
        self.set_direction("right")

    def left(self):
        self.check_speed()
        requests.post(self.address + "/turn", data={"direction": "left"})
        self.set_direction("left")

    def forwards(self):
        self.check_speed()
        requests.post(self.address + "/turn", data={"direction": "forward"})
        self.set_direction("forward")

    def forward_right(self):
        self.check_speed()
        requests.post(self.address + "/turn", data={"direction": "forward right"})
        self.set_direction("forward right")

    def forward_left(self):
        self.check_speed()
        requests.post(self.address + "/turn", data={"direction": "forward left"})
        self.set_direction("forward left")

    def reverse(self):
        self.check_speed()
        requests.post(self.address + "/turn", data={"direction": "reverse"})
        self.set_direction("reverse")

    def __del__(self):
        self.stop()


if __name__ == "__main__":
    conn = PiController()
    print(conn.address)
    conn.forwards()
