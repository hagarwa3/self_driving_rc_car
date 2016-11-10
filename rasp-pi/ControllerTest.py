import unittest
import ArduinoController as controller
import sys
from io import StringIO


path = "/dev/serial/by-path/platform-bcm2708_usb-usb-0:1.4:1.0-port0"
port = 9600


# local_only = len(sys.argv) > 1 and sys.argv[1] == "local"
local_only = True


def format_expected_timeseries(series):
    """
    Function to map conversion to a bytechar of every element in an expected output array.
    :param series: list of chars/strings
    :return: list of bytechars
    """
    return [str(x).encode() for x in series]


class MyTestCase(unittest.TestCase):

    def test_timeseries(self):
        """
        Tests a series of commands to check the timeseries saved from the Arduino. The car should end in approximately
        the same position and direction it starts in.
        """
        if not local_only:
            conn = controller.ArduinoController(path, port)
            conn.move_forward()
            conn.move_backward()
            conn.turn_right()
            conn.turn_left()
            conn.stop()
            conn.turn_left()
            conn.turn_right()
            conn.move_backward()
            conn.move_forward()
            conn.stop()

            expected_out = ['F', 'B', 'r', 'l', 'S', 'l', 'r', 'B', 'F', 'S']
            expected_out = format_expected_timeseries(expected_out)
            self.assertListEqual(conn.timeseries, expected_out)

        else:
            self.assertTrue(True)


    def test_turns(self):
        """
        Tests the turn versus hard turn commands. It should be visably apparent when the car is making a hard.
        """
        if not local_only:
            conn = controller.ArduinoController(path, port)
            conn.turn_right()
            conn.stop()
            conn.turn_hard_left()
            conn.stop()
            conn.turn_left()
            conn.stop()
            conn.turn_hard_right()
            conn.stop()

            expected_out = ['r', 'S', 'L', 'S', 'l', 'S', 'R', 'S']
            expected_out = format_expected_timeseries(expected_out)
            self.assertListEqual(conn.timeseries, expected_out)

        else:
            self.assertTrue(True)


    def test_deletion_behavior(self):
        """
        The ArduinoController has an overridden __del__ operator, which stops the car. This tests that the overriden
        function is called on __del__.
        """
        stdout = sys.stdout
        sys.stdout = StringIO()

        def test_scope():
            """
            Local function to test behavior of ArduinoController on close.
            """
            conn = controller.ArduinoController(path, port, print_on_death=True, test_mode=True)

        test_scope()
        out = sys.stdout.getvalue()

        sys.stdout.close()
        sys.stdout = stdout  # restore original stdout

        expected_out = "Arduino at " + path + " "  + str(port) + " is going out of scope. Stopping car.\n"
        self.assertEqual(str(out), expected_out)

if __name__ == '__main__':
    unittest.main()
