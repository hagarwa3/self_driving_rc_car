import cv2
import numpy as np
import pi_controller
from sklearn.externals import joblib
from datetime import datetime as dt

bot_url = "http://192.168.1.11:9876/"
frame_idx = 0
direction = 0
n_reverses = 0
controller = pi_controller.PiController(bot_url)
log_model = joblib.load('logistic_regression.pkl')
convert_to_grayscale = True
last_img = None


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

def draw_edges_bw(img, n_components=-1):
    contours = draw_edges(img, n_components)
    img_bw = np.zeros(img.shape)
    cv2.drawContours(img_bw, contours, -1, 255, 1)
    return img_bw

def draw_direction_arrow(img, direction):
    # Draw arrow centered at (180, 75)
    if direction == 0:          # left turn
        cv2.arrowedLine(img, (230, 75), (130, 75), (255, 0, 0), 5, 5)
        # cv2.arrowedLine(gray_image, (230, 125), (130, 25), (0, 255, 0), 5, 5)
    elif direction == 1:        # right turn
        cv2.arrowedLine(img, (130, 75), (230, 75), (255, 0, 0), 5, 5)
        # cv2.arrowedLine(gray_image, (130, 125), (230, 25), (0, 255, 0), 5, 5)
    elif direction == 2:        # forwards
        cv2.arrowedLine(img, (180, 125), (180, 25), (255, 0, 0), 5, 5)
    elif direction == 3:        # backwards
        cv2.arrowedLine(img, (180, 25), (180, 125), (255, 0, 0), 5, 5)


def navigate(img):
    global direction
    global n_reverses
    direction, img = get_direction_from_image(img)

    if direction == 2:
        controller.forwards()
    elif direction == 0:
        controller.forward_left()
    elif direction == 1:
        controller.forward_right()
    elif direction == 3:
        controller.stop()
        n_reverses += 1

    if direction != 3:
        n_reverses = 0

    return img

    # if n_reverses == 5:
    #     raise Exception("time to stop")

def get_direction_from_image(img):
    global log_model
    img_bw = img
    #img_bw = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #print(img_bw.shape)
    height, width = img_bw.shape
    img_bw = img_bw[int(height/2):height, :]
    img_bw = cv2.resize(img_bw, (0,0), fx=0.25, fy=0.25)
    img_bw = draw_edges_bw(img_bw, 0.05)
    img_bw_copy = img_bw.flatten().astype(np.float32)
    prediction = log_model.predict([img_bw_copy])
    return prediction[0], img_bw

def processIncoming(im_bytes, stream):
    """
    Processes incoming frames from the streaming url
    :param stream: incoming bytes from URL for the video
    :param bytes: The data that is being received and sent through
    :return: processed image to bytes, updated bytes param
    """
    global direction
    global frame_idx
    global convert_to_grayscale
    global last_img

    #we need a while true loop so that images of size larger than 1024 bytes can be read in
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
            if not convert_to_grayscale:
                ret, jpeg = cv2.imencode('.jpg', img)
                return jpeg.tobytes(), im_bytes
            else:
                # this is where the processing would actually take place.
                # current processing is to convert incoming stream to black and white only
                gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                # Navigate once per second (once every 30 frames) to avoid too many open TCP connections
                img = navigate(gray_image) if frame_idx % 30 == 0 else last_img
                last_img = img

                gray_image = cv2.cvtColor(gray_image, cv2.COLOR_GRAY2BGR)
                # draw_edges(gray_image, 0.05)
                
                contours = draw_edges(gray_image, 0.1)
                # cv2.putText(gray_image, "↖️⬆️↗️",
                #             (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 3)
                draw_direction_arrow(gray_image, direction)

                ret, jpeg = cv2.imencode('.jpg', gray_image)
                # ret, jpeg = cv2.imencode('.jpg', img)
                # ret, jpeg = cv2.imencode('.jpg', contour)

                frame_idx += 1
                return jpeg.tobytes(), im_bytes
            if cv2.waitKey(1) == 27:
                exit(0)

            break
