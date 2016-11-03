import cv2
import urllib.request
import numpy as np


evanURL = 'http://192.168.1.22/live'
URL = 'http://192.168.1.5:8080/video'

show_grayscale = True

stream = urllib.request.urlopen(evanURL)
bytes = bytes()
while True:
    bytes += stream.read(1024)
    start_idx = bytes.find(b'\xff\xd8')
    end_idx = bytes.find(b'\xff\xd9')
    if start_idx != -1 and end_idx != -1:
        jpg = bytes[start_idx : end_idx + 2]
        bytes = bytes[end_idx + 2 :]

        if not show_grayscale:
            img = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8))
            cv2.imshow('i', img)
        else:
            gray_image = cv2.cvtColor(i, cv2.COLOR_BGR2GRAY)
            cv2.imshow('i', gray_image)

        if cv2.waitKey(1) == 27:
            exit(0)