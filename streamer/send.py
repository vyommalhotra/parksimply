import socket
import time
from imutils.video import VideoStream
import imagezmq
import cv2

sender = imagezmq.ImageSender(connect_to='tcp://LAPTOP-EA7DT8JN:5555')

rpi_name = socket.gethostname()
time.sleep(2.0)

while True:
    footage = cv2.VideoCapture('vid.mp4')
    escape = 0

    while True:
        ret, frame = footage.read()
        if ret == True:
            sender.send_image(rpi_name, frame)

            if cv2.waitKey(1) == 27:
                escape = 1
                break
        
        else:
            break
    
    if escape:
        break
