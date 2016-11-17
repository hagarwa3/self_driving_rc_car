import numpy as np
import cv2
import serial
import socket
import urllib.request
import getch
class CollectTrainingData(object):
    
    def __init__(self):


        # create labels
        self.k = np.zeros((4, 4), 'float')
        for i in range(4):
            self.k[i, i] = 1
        self.temp_label = np.zeros((1, 4), 'float')

        self.collect_image()

    def collect_image(self):

        global im_bytes

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
        try:
            frame = 1
            count = 0
            while keep_running:
                im_bytes += stream.read(1024)
                
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
                    height, width = img.shape
                    # select lower half of the image
                    roi = img[int(height/2):height, :]
                    # save streamed images
                    cv2.imwrite('training_images/frame{:>05}.jpg'.format(frame), img)
                    
                    
                    
                    # reshape the roi image into one row array
                    temp_array = roi.flatten().astype(np.float32)
                    #print(temp_array.shape)
                    frame += 1
                    total_frame += 1
                    count+=1
                    # get input from human driver
                    if count == 10:
                        count = 0
                        c = getch.getch()
                        if c == 'd':
                            print("Forward Right")
                            image_array = np.vstack((image_array, temp_array))
                            label_array = np.vstack((label_array, self.k[1]))
                            saved_frame += 1

                        elif c == 'a':
                            print("Forward Left")
                            image_array = np.vstack((image_array, temp_array))
                            label_array = np.vstack((label_array, self.k[0]))
                            saved_frame += 1

                        elif c == 'w':
                            print("Forward")
                            saved_frame += 1
                            image_array = np.vstack((image_array, temp_array))
                            label_array = np.vstack((label_array, self.k[2]))

                        elif c == 's':
                            print("Reverse")
                            saved_frame += 1
                            image_array = np.vstack((image_array, temp_array))
                            label_array = np.vstack((label_array, self.k[3]))

                        elif c== 'x':
                            print('exit')
                            keep_running = False
                                   

            # save training images and labels
            train = image_array[1:, :]
            train_labels = label_array[1:, :]

            # save training data as a numpy file
            np.savez('training_data_temp/test.npz', train=train, train_labels=train_labels)

            e2 = cv2.getTickCount()
            # calculate streaming duration
            time0 = (e2 - e1) / cv2.getTickFrequency()
            print('Streaming duration:', time0)

            print(train.shape)
            print(train_labels.shape)
            print('Total frame:', total_frame)
            print('Saved frame:', saved_frame)
            print('Dropped frame', total_frame - saved_frame)
        except:
            print("rip")

if __name__ == '__main__':
    CollectTrainingData()