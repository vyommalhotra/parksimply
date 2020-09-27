import cv2
from cars import car_extractor
from spots import spot_extractor

if __name__ == '__main__':
    print('begin extracting')
    process_frames()

def process_frames():
    # to be replaced by a stream from a camera later
    capture = cv2.VideoCapture('footage/footage.avi')

    # initialize extractors
    car_ex = car_extractor()
    spot_ex = spot_extractor()

    # to be replaced by while (True) later
    while(capture.isOpened()):

        # get next frame
        ret, frame = capture.read()

        # pass frame to extractors
        car_ex.process_frame(frame)
        spot_ex.process_frame(frame)

        # processing
        cars = car_ex.get_car_vectors()
        spots = spot_ex.get_open_spots()

        # output to file for now
        # later to be replaced by a buffer consumable by a rest api
        with open('buffer.txt', 'w') as output:
            output.write(str(cars) + '\n' + str(spots))





    

