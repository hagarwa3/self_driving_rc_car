import serial
import time


class ArduinoController:

    def __init__(self, path, port=9600, print_on_death=False, test_mode=False):
        """
        :param path: str path to file for usb serial connection to Arduino
        :param port: int port number
        :param print_on_death: boolean to print output when object is deleted
        :param test_mode: boolean to prevent connection for localizable tests (no Arduino required)
        """
        self.path = path
        self.port = port
        self.print_on_death = print_on_death
        self.test_mode = test_mode
        self.speed = 9
        if not test_mode:
            self.conn = serial.Serial(path, port)
            self.timeseries = []
            self.state = None
            self.stop(save_cmd=False)
            self.print_on_death = print_on_death
            time.sleep(2)


    def send_command(self, cmd, delay=1, save_cmd=True):
        """
        Sends a command to the Arduino.
        :param cmd: bytechar of command
        :param delay: int Number of seconds to wait after completion. Defaults to 1.
        :param save_cmd: Boolean for whether command should be saved to timeseries.
        :return: None
        """
        assert type(cmd) == bytes
        if not self.test_mode:
            self.conn.write(cmd)
            if save_cmd:
                self.timeseries.append(conn.read())
            time.sleep(delay)


    def stop(self, delay=1, save_cmd=True):
        """
        Command to stop the Arduino.
        :param delay: int Number of seconds to wait after completion. Defaults to 1.
        :param save_cmd: Boolean for whether command should be saved to timeseries.
        :return: None
        """
        self.send_command(b'S', delay=delay, save_cmd=save_cmd)
        self.state = "stop"


    def move_forward(self, delay=1, save_cmd=True):
        """
        Command to move the Arduino forwards.
        :param delay: int Number of seconds to wait after completion. Defaults to 1.
        :param save_cmd: Boolean for whether command should be saved to timeseries.
        :return: None
        """
        self.send_command(b'F', delay=delay, save_cmd=save_cmd)
        self.state = "forwards"


    def move_backward(self, delay=1, save_cmd=True):
        """
        Command to move the Arduino backwards.
        :param delay: int Number of seconds to wait after completion. Defaults to 1.
        :param save_cmd: Boolean for whether command should be saved to timeseries.
        :return: None
        """
        self.send_command(b'B', delay=delay, save_cmd=save_cmd)
        self.state = "backwards"


    def turn_right(self, delay=1, save_cmd=True):
        """
        Command to turn the Arduino right.
        :param delay: int Number of seconds to wait after completion. Defaults to 1.
        :param save_cmd: Boolean for whether command should be saved to timeseries.
        :return: None
        """
        self.send_command(b'r', delay=delay, save_cmd=save_cmd)
        self.state = "right"


    def turn_hard_right(self, delay=1, save_cmd=True):
        """
        Command to turn the Arduino on a hard right.
        :param delay: int Number of seconds to wait after completion. Defaults to 1.
        :param save_cmd: Boolean for whether command should be saved to timeseries.
        :return: None
        """
        self.send_command(b'R', delay=delay, save_cmd=save_cmd)
        self.state = "hard right"


    def turn_left(self, delay=1, save_cmd=True):
        """
        Command to turn the Arduino left.
        :param delay: int Number of seconds to wait after completion. Defaults to 1.
        :param save_cmd: Boolean for whether command should be saved to timeseries.
        :return: None
        """
        self.send_command(b'l', delay=delay, save_cmd=save_cmd)
        self.state = "left"


    def turn_hard_left(self, delay=1, save_cmd=True):
        """
        Command to turn the Arduino on a hard left.
        :param delay: int Number of seconds to wait after completion. Defaults to 1.
        :param save_cmd: Boolean for whether command should be saved to timeseries.
        :return: None
        """
        self.send_command(b'L', delay=delay, save_cmd=save_cmd)
        self.state = "hard left"


    def set_speed(self, speed, delay=1, save_cmd=True):
        """
        Updates the speed of the car normalized 0 to 9.
        :param speed:
        :param delay:
        :param save_cmd:
        :return:
        """
        self.speed = speed
        self.send_command(str(self.speed).encode(), delay=delay, save_cmd=save_cmd)


    def __del__(self):
        """
        Overridden deletion operator for the Arduino. Will issue a stop command when the controller object goes out of
        scope to prevent runaway cars. Will output if self.print_on_death is True for testing purposes. Also explicitly
        closes the PySerial connection ot the Arduino.
        :return:
        """
        if self.print_on_death:
            print("Arduino at", self.path, self.port, "is going out of scope. Stopping car.")

        self.stop()

        if not self.test_mode:
            self.conn.close()



if __name__ == "__main__":
    path = "/dev/serial/by-path/platform-bcm2708_usb-usb-0:1.4:1.0-port0"
    port = 9600
    local_only = True
    conn = ArduinoController(path, test_mode=True)
    conn.stop()
