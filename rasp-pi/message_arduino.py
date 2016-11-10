import serial
import time


conn = None
timeseries = []


class ArduinoController():

    def __init__(self, path, port=9600):
        self.path = path
        self.port = port
        self.conn = serial.Serial(path, port)
        self.timeseries = []
        self.stop()
        time.sleep(2)


    def send_command(self, cmd, delay = 0):
        self.conn.write(cmd)
        self.timeseries.append(conn.read())
        time.sleep(delay)


    def stop(self, delay=0):
        self.send_command(b'S', delay=delay)


    def fwd(self, delay=0):
        self.send_command(b'F', delay=delay)


    def right(self, delay=0):
        self.send_command(b'r', delay=delay)


    def hard_right(self, delay=0):
        self.send_command(b'R', delay=delay)


    def left(self, delay=0):
        self.send_command(b'l', delay=delay)


    def hard_left(self, delay=0):
        self.send_command(b'L', delay=delay)


if __name__ == "__main__":
    global timeseries
    initialize()
    fwd(1)
    stop(1)
    back(1)
    stop(1)

    print(timeseries)
