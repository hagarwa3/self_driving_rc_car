import requests
import os
import threading
import multiprocessing
import time

class stoppable(threading.Thread):
    """
    Wrapper for a stoppable thread pulled from GitHub.
    """
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
    """
    Wrapper function to make a stoppable thread using the same inputs
    as threading.Thread.
    """
    stoppable(target=stoppable, args=[target, args]).run()


class PiController:
    """
    This class serves as a wrapper for the Pi's http server for controls.
    """
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
        """
        Set's the direction and updates the last direction of the Pi.
        """
        self.last_direction = self.direction
        self.direction = new_directon

    def check_speed(self):
        """
        Checks if the last command was a stop and the current command is not
        stop, in which case we need to give the car velocity again. This prevents
        sending extra messages which will be slow due to TCP handshake.
        """
        if self.last_direction == "stop" and self.direction != "stop":
            t = self.parallelizer(target=_speed_worker, args=["9"])
            # self.threads.append(t)
            t.start()

    def trim_threads(self):
        """
        This will see how many threads are running and attempt to stop 
        old threads over a threshold
        """
        if self.parallelizer != threading.Thread and self.parallelizer != :

        return
        print("number of threads running: ", len(threading.enumerate()))
        for t in threading.enumerate()[:self.n_threads_max]:
            t._stop()

    def threader(self, target=None, args=None):
        """
        This function creates a new thread if there are not too many threads open.
        Stop commands will always be issued regardless of anything else.
        """
        print("number of threads running: ", len(threading.enumerate()))
        if (len(threading.enumerate()) < self.n_threads_max or target == self.stop) and target != self.last_command[0]:
            self.last_command = (target, args)
            threading.Thread(target=stoppable, args=[target, args]).start()

    def _speed_worker(self, speed):
        """
        Worker function to set the car speed.
        """
        requests.post(self.address + "/speed", data={"speed": str(speed)})

    def _direction_worker(self, direction):
        """
        Worker funciton to set the car direction.
        """
        requests.post(self.address + "/turn", data={"direction": str(direction)})

    def stop(self):
        """
        Stops the car by setting speed to zero and direction to forwards.
        """
        t = self.parallelizer(target=self._speed_worker, args=["0"])
        # self.threads.append(t)
        if type(t) == threading.Thread:
            t.start()

        t = self.parallelizer(target=self._direction_worker, args=["forward"])
        # self.threads.append(t)
        if type(t) == threading.Thread:
            t.start()
        
        self.trim_threads()
        self.set_direction("stop")

    def right(self):
        """
        Turns the car right.
        """
        self.check_speed()

        t = self.parallelizer(target=self._direction_worker, args=["right"])
        # self.threads.append(t)
        if type(t) == threading.Thread:
            t.start()

        self.trim_threads()
        self.set_direction("right")

    def left(self):
        """
        Turns the car left.
        """
        self.check_speed()

        t = self.parallelizer(target=self._direction_worker, args=["left"])
        # self.threads.append(t)
        if type(t) == threading.Thread:
            t.start()

        self.trim_threads()
        self.set_direction("left")

    def forwards(self):
        """
        Moves the car forwards.
        """
        self.check_speed()

        t = self.parallelizer(target=self._direction_worker, args=["forward"])
        # self.threads.append(t)
        if type(t) == threading.Thread:
            t.start()

        self.trim_threads()
        self.set_direction("forward")

    def forward_right(self):
        """
        Moves the car right by powering both wheels but reducing power to the 
        right wheel slightly.
        """
        self.check_speed()

        print(self.parallelizer)
        t = self.parallelizer(target=self._direction_worker, args=["right"])
        # self.threads.append(t)
        if type(t) == threading.Thread:
            t.start()

        self.trim_threads()
        self.set_direction("forward right")

    def forward_left(self):
        """
        Moves the car left by powering both wheels but reducing power to the 
        left wheel slightly.
        """
        self.check_speed()

        t = self.parallelizer(target=self._direction_worker, args=["forward left"])
        # self.threads.append(t)
        if type(t) == threading.Thread:
            t.start()

        self.trim_threads()
        self.set_direction("forward left")

    def reverse(self):
        """
        Reverses the RC car.
        """
        self.check_speed()

        t = self.parallelizer(target=self._direction_worker, args=["reverse"])
        # self.threads.append(t)
        if type(t) == threading.Thread:
            t.start()

        self.trim_threads()
        self.set_direction("reverse")

    def __del__(self):
        """
        Overridden deletion operator that runs a script to issue a separate stop command
        then attempts to clean up its own threads.
        """
        os.system("python stop_car.py " + self.address)
        for t in threading.enumerate():
            t._stop()


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
