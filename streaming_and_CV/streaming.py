import cv2
import urllib.request
import numpy as np

def processIncoming(url, bytes, stream):
    show_grayscale = True
    #we need a while true loop so that images of size larger than 024 bytes can be read in
    while True:
        bytes += stream.read(1024)
        
        #start and end index are determined by how jpeg files are when converted to bytes. Which is why the specific thing in the find
        start_idx = bytes.find(b'\xff\xd8')
        end_idx = bytes.find(b'\xff\xd9')

        if start_idx != -1 and end_idx != -1:
            jpg = bytes[start_idx : end_idx + 2]
            #update bytes from end of image bytes to the new index so that next image can be read
            bytes = bytes[end_idx + 2 :]
            img = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.IMREAD_COLOR)
            if not show_grayscale:
                ret, jpeg = cv2.imencode('.jpg', img)
                return jpeg.tobytes(), bytes
            else:
                gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                ret, jpeg = cv2.imencode('.jpg', gray_image)
                return jpeg.tobytes(), bytes
            if cv2.waitKey(1) == 27:
                exit(0)
            break
