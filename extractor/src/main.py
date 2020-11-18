from broker import Broker
import cv2

if __name__ == "__main__":

    footage = cv2.VideoCapture('')
    broker = Broker(footage, skip=30)

    # while there is still footage left
    while (broker.is_footage_open()):

        # process current frame of footage
        done = broker.process_frame()

        # end of footage
        if done:
            break
    
    footage.release()

# TODO: VYOM
# get frame from image
# calibrate fram skipping

# TODO: SARTHAK
# initialize spot class with image
# run spot detection on spot class
# returns unique IDs of detected spots

# TODO: SUNITH
# initialize car class with image
# run car detection on car class
# get car Ids from car class

# TODO: VYOM
# initilize matcher class with IDs of spots and cars
# For the IDs that don't yet have a match, perform a match
# for each previous and new match, get Image from car and spot classes
# save each image -> rest call to front end (later).
        


