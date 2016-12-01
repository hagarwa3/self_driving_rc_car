import requests
import os
import threading
import multiprocessing
import time

class stoppable(threading.Thread):
    def __init__(self, target, args):
        super(stoppable, self).__init__()
        self._stop = threading.Event()
        self.target = target
        self.args = args

    def run(self):    
        while True:
            # print ("thread running")
            # self.func()
            self.target(*self.args)
            if self.stopped():
                break
            time.sleep(1)
        print ("thread on the way to its exit")


def make_stoppable(target, args):
    threading.Thread(target=stoppable, args=[target, args]).start()


class PiController:
    def __init__(self, address="http://192.168.1.11:9876"):
        if address[-1] == "/":
            address = address[:-1]
        self.address = address
        self.last_direction = None
        self.direction = None
        self.n_threads_max = 10
        # self.parallelizer = mutliprocessing.Process
        # self.parallelizer = threading.Thread
        # self.parallelizer = stoppable
        self.parallelizer = self.threader
        self.last_command = (None, None)
        # self.threads = []

    def set_direction(self, new_directon):
        self.direction = new_directon
        self.last_direction = self.direction

    def check_speed(self):
        if self.last_direction == "stop" and self.direction != "stop":
            t = self.parallelizer(target=_speed_worker, args=["9"])
            # self.threads.append(t)
            t.start()

    def trim_threads(self):
        print(len(threading.enumerate()))
        for t in threading.enumerate()[self.n_threads_max:]:
            t._stop()

    def threader(target, args):
        if len(threading.enumerate()) < self.n_threads_max or (target == self.stop and last_command[0] != self.stop):
            self.last_command = (target, args)
            threading.Thread(target=stoppable, args=[target, args]).start()

    def _speed_worker(self, speed):
        requests.post(self.address + "/speed", data={"speed": str(speed)})

    def _direction_worker(self, direction):
        requests.post(self.address + "/turn", data={"direction": str(direction)})

    def stop(self):
        t = self.parallelizer(target=self._speed_worker, args=["0"])
        # self.threads.append(t)
        t.start()

        t = self.parallelizer(target=self._direction_worker, args=["forward"])
        # self.threads.append(t)
        t.start()
        
        self.trim_threads()
        self.set_direction("stop")

    def right(self):
        self.check_speed()

        t = self.parallelizer(target=self._direction_worker, args=["right"])
        # self.threads.append(t)
        t.start()

        self.trim_threads()
        self.set_direction("right")

    def left(self):
        self.check_speed()

        t = self.parallelizer(target=self._direction_worker, args=["left"])
        # self.threads.append(t)
        t.start()

        self.trim_threads()
        self.set_direction("left")

    def forwards(self):
        self.check_speed()

        t = self.parallelizer(target=self._direction_worker, args=["forward"])
        # self.threads.append(t)
        t.start()

        self.trim_threads()
        self.set_direction("forward")

    def forward_right(self):
        self.check_speed()

        t = self.parallelizer(target=self._direction_worker, args=["right"])
        # self.threads.append(t)
        t.start()

        self.trim_threads()
        self.set_direction("forward right")

    def forward_left(self):
        self.check_speed()

        t = self.parallelizer(target=self._direction_worker, args=["forward left"])
        # self.threads.append(t)
        t.start()

        self.trim_threads()
        self.set_direction("forward left")

    def reverse(self):
        self.check_speed()

        t = self.parallelizer(target=self._direction_worker, args=["reverse"])
        # self.threads.append(t)
        t.start()

        self.trim_threads()
        self.set_direction("reverse")

    def __del__(self):
        for t in threading.enumerate():
            t.exit()
        os.system("python stop_car.py " + self.address)


if __name__ == "__main__":
    conn = PiController()
    print(conn.address)
    # conn.forwards()
    conn.forward_left()
    # time.sleep(1)
    # conn.stop()
    # time.sleep(1)
    # conn.forwards()
    # time.sleep(1)
    # conn.stop()
    time.sleep(5)
