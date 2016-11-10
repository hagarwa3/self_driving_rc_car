import serial
import time


conn = None


def initialize():
    global conn
    conn = serial.Serial("/dev/serial/by-path/platform-bcm2708_usb-usb-0:1.4:1.0-port0", 9600)
    time.sleep(2)
    stop()


def stop():
    global conn
    conn.write(b'S')


def fwd():
    global conn
    conn.write(b'F')


def back():
    global conn
    conn.write(b'B')


def right():
    global conn
    conn.write(b'R')


def left():
    global conn
    conn.write(b'L')


if __name__ == "__main__":
    initialize()
    fwd()
    time.sleep(1)
    stop()
    time.sleep(1)
    back()
    time.sleep(1)
    stop()

