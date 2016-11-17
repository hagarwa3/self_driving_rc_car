import cv2
import numpy as np


def draw_line(img, pt0, pt1, color=(255, 0, 0), weight=5):
    cv2.line(img, pt0, pt1, color, 5)


def auto_canny(img, sigma=0.01):
    """
    Applies the Canny detection algorithm with automatic parameter estimation. Modified from:
    http://www.pyimagesearch.com/2015/04/06/zero-parameter-automatic-canny-edge-detection-with-python-and-opencv/
    :param img: Image in
    :param sigma: A hyperparameter to tune how tight (small) the thresholds are
    :return: An image of edges
    """
    #
    # compute the median of the single channel pixel intensities
    v = np.median(img)

    # apply automatic Canny edge detection using the computed median
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edged = cv2.Canny(img, lower, upper)

    # return the edged image
    return edged


def draw_edges(img, n_components=-1):
    """
    Accepts an image, draws edges on the image, and returns the edged image.
    :param img: Image to be drawn on
    :return: Image of edges only
    """
    edges = auto_canny(img)
    contours = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[1]
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    if n_components != -1 and type(n_components) == int:
        contours = contours[:n_components]
    elif n_components != -1 and type(n_components) == float:
        contours = contours[:int(len(contours) * n_components)]
    cv2.drawContours(img, contours, -1, (0, 255, 0), 1)
    return contours


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
        prevImBytes = im_bytes
        im_bytes += stream.read(1024)
        if im_bytes == prevImBytes:
            print("Stream ended")
            break
        
        # start and end index are determined by how jpeg files are when converted to bytes.
        # Which is why the specific thing in the find
        start_idx = im_bytes.find(b'\xff\xd8')
        end_idx = im_bytes.find(b'\xff\xd9')

        if start_idx != -1 and end_idx != -1:
            jpg = im_bytes[start_idx : end_idx + 2]
            #update bytes from end of image bytes to the new index so that next image can be read
            im_bytes = im_bytes[end_idx + 2 :]
            img = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
            if not show_grayscale:
                ret, jpeg = cv2.imencode('.jpg', img)
                return jpeg.tobytes(), im_bytes
            else:
                # this is where the processing would actually take place.
                # current processing is to convert incoming stream to black and white only
                gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                gray_image = cv2.cvtColor(gray_image, cv2.COLOR_GRAY2RGB)
                draw_edges(gray_image, 0.05)
                ret, jpeg = cv2.imencode('.jpg', gray_image)
                # draw_line(jpeg, (0, 0), (100, 100))
                return jpeg.tobytes(), im_bytes
            if cv2.waitKey(1) == 27:
                exit(0)
            break
