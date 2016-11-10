import serial
import time


conn = None
timeseries = []


def initialize():
    global conn
    conn = serial.Serial("/dev/serial/by-path/platform-bcm2708_usb-usb-0:1.4:1.0-port0", 9600)
    time.sleep(2)
    stop()


def send_command(cmd, delay=0):
    global conn, timeseries
    conn.write(cmd)
    timeseries.append(conn.read())
    time.sleep(delay)


def stop(delay=0):
    send_command(b'S', delay=delay)


def fwd(delay=0):
    send_command(b'F', delay=delay)


def back(delay=0):
    send_command(b'B', delay=delay)


def right(delay=0):
    send_command(b'R', delay=delay)


def left(delay=0):
    send_command(b'L', delay=delay)


if __name__ == "__main__":
    global timeseries
    initialize()
    fwd(1)
    stop(1)
    back(1)
    stop(1)

    print(timeseries)
