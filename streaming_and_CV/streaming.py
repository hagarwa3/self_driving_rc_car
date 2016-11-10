import cv2
import urllib.request
import numpy as np

def processIncoming(im_bytes, stream):
    """
    Processes incoming frames from the streaming url
    :param stream: incoming bytes from URL for the video
    :param bytes: The data that is being received and sent through
    :return: processed image to bytes, updated bytes param
    """
    show_grayscale = True
    #we need a while true loop so that images of size larger than 024 bytes can be read in
    while True:
        im_bytes += stream.read(1024)
        
        #start and end index are determined by how jpeg files are when converted to bytes. Which is why the specific thing in the find
        start_idx = im_bytes.find(b'\xff\xd8')
        end_idx = im_bytes.find(b'\xff\xd9')

        if start_idx != -1 and end_idx != -1:
            jpg = im_bytes[start_idx : end_idx + 2]
            #update bytes from end of image bytes to the new index so that next image can be read
            im_bytes = im_bytes[end_idx + 2 :]
            img = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.IMREAD_COLOR)
            if not show_grayscale:
                ret, jpeg = cv2.imencode('.jpg', img)
                return jpeg.tobytes(), im_bytes
            else:
                # this is where the processing would actually take place.
                # current processing is to convert incoming stream to black and white only
                gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                ret, jpeg = cv2.imencode('.jpg', gray_image)
                return jpeg.tobytes(), im_bytes
            if cv2.waitKey(1) == 27:
                exit(0)
            break
