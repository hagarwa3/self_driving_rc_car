import cv2
import urllib.request
import numpy as np

stream = urllib.request.urlopen('http://192.168.1.10/live')
bytes = bytes()
while True:
    bytes += stream.read(1024)
    a = bytes.find(b'\xff\xd8')
    b = bytes.find(b'\xff\xd9')
    if a != -1 and b != -1:
        jpg = bytes[a:b+2]
        bytes = bytes[b+2:]
        i = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
        cv2.imshow('i', i)
        if cv2.waitKey(1) == 27:
            exit(0)
        break


# import cv2
# cap = cv2.VideoCapture('http://10.194.9.154:8080/video')

# while True:
#   ret, frame = cap.read()
#   cv2.imshow('Video', frame)

#   if cv2.waitKey(1) == 27:
#     exit(0)