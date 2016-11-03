import cv2
import urllib.request
import numpy as np


evan_url = 'http://192.168.1.22/live'                   # URL for Evan's video stream
url = 'http://192.168.1.5:8080/video'                   # video for Harhit's stream
url_illinois_net = 'http://10.194.9.154:8080/video'     # video for Harshit's Siebel stream
evan_url_illinois_net = 'http://10.192.224.222/live'    # video for Evan's Siebel stream

show_grayscale = True

# Open the URL
stream = urllib.request.urlopen(evan_url_illinois_net)
bytes = bytes()
while True:
    bytes += stream.read(1024)
    start_idx = bytes.find(b'\xff\xd8')
    end_idx = bytes.find(b'\xff\xd9')
    if start_idx != -1 and end_idx != -1:
        # If valid frame
        jpg = bytes[start_idx : end_idx + 2]
        bytes = bytes[end_idx + 2 :]

        print(bytes)    # Show that things are coming in

        if not show_grayscale:
            img = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.IMREAD_COLOR)
            cv2.imshow('i', img)
        else:
            gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            cv2.imshow('i', gray_image)

        if cv2.waitKey(1) == 27:
            exit(0)
