from matplotlib import pyplot as plt
from gluoncv import model_zoo, data, utils
#Check out demo_yolo.py for explanation on how to set the model up

#Object Tracking links
# https://www.pyimagesearch.com/2018/07/23/simple-object-tracking-with-opencv/
# https://www.learnopencv.com/object-tracking-using-opencv-cpp-python/
# http://davheld.github.io/GOTURN/GOTURN.html


class carDetector:

    def __init__(self):
        self.prevFrame = None #Store previous frame, don't know if we'll need this
        self.boundingBoxes = [] #Store bounding boxes of previous frame, will likely need this for object tracking
        self.currFrame = None

        #Creating our model, we can change this to other models if needed. Check model zoo online for more.
        self.cvModel = model_zoo.get_model('yolo3_darknet53_coco', pretrained=True)

    def get_cars(inputFrame):
        self.currFrame = inputFrame

        #Detect cars here

        #Match objects between frames

        #Set new bounding boxes with IDs

        self.prevFrame = self.currFrame

        #Return bounding boxes with carIDs to broker
        return ['1', '2', '3', '4']

    def get_car_image(inputID, inputImg):
        #Cross reference inputID with stored IDs

        #Highlight location of ID car on the inputImg

        #Return highlighted image to broker



