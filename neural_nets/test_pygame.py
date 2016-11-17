import cv2
import numpy as np
import urllib.request

evanURL = 'http://192.168.1.10/live'
URL = 'http://192.168.1.3:8080/video'
urlIllinoisNet = 'http://10.194.9.154:8080/video'
evanUrlIllinoisNet = 'http://10.192.224.222/live'

stream = urllib.request.urlopen(evanURL)
im_bytes = bytes()

saved_frame = 0
total_frame = 0

# collect images for training
print('Start collecting images...')
e1 = cv2.getTickCount()
image_array = np.zeros((1, 86400))
label_array = np.zeros((1, 4), 'float')

# stream video frames one by one
show_grayscale = True
#we need a while true loop so that images of size larger than 024 bytes can be read in
keep_running = True
frame = 1
count = 0
while keep_running:
    prevImBytes = im_bytes
    im_bytes += stream.read(1024)
    if im_bytes == prevImBytes:
        print("stream ended")
        break
                
    
    # start and end index are determined by how jpeg files are when converted to bytes.
    # Which is why the specific thing in the find
    start_idx = im_bytes.find(b'\xff\xd8')
    end_idx = im_bytes.find(b'\xff\xd9')
    #print("lmao ")
    if start_idx != -1 and end_idx != -1:
        jpg = im_bytes[start_idx : end_idx + 2]
        #update bytes from end of image bytes to the new index so that next image can be read
        im_bytes = im_bytes[end_idx + 2 :]
        img = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        cv2.imshow('image', img)
        #print("lol")
        if cv2.waitKey(1) == 27:
            exit(0)