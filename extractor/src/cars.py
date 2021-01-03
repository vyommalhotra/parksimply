from matplotlib import pyplot as plt
from gluoncv import model_zoo, data, utils
from yolov3.utils import draw_bbox, read_class_names
from yolov3.configs import *
from deep_sort import nn_matching
from deep_sort.detection import Detection
from deep_sort.tracker import Tracker
from deep_sort import generate_detections as gdet
import cv2
import numpy as np

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

        #Threshold of what is a car
        self.thresh = 0.7

        self.NUM_CLASS = read_class_names(YOLO_COCO_CLASSES)
        self.key_list = list(self.NUM_CLASS.keys()) 
        self.val_list = list(self.NUM_CLASS.values())

        #Creating deep sort object, these parameters can be massaged
        max_cosine_distance = 0.7
        nn_budget = None
        model_filename = 'model_data/mars-small128.pb'
        self.encoder = gdet.create_box_encoder(model_filename, batch_size=1)
        metric = nn_matching.NearestNeighborDistanceMetric("cosine", max_cosine_distance, nn_budget)
        self.tracker = Tracker(metric)

        #Creating our model, we can change this to other models if needed. Check model zoo online for more.
        self.cvModel = model_zoo.get_model('yolo3_darknet53_coco', pretrained=True)
        print("init carDetector")

    def get_cars(self, inputFrame):
        self.currFrame = inputFrame

        original_frame = cv2.cvtColor(self.currFrame, cv2.COLOR_BGR2RGB)
        original_frame = cv2.cvtColor(original_frame, cv2.COLOR_BGR2RGB)

        cv2.imwrite("../footage/currentImage.jpg", original_frame)
        imlink = "../footage/currentImage.jpg"
        
        x, img = data.transforms.presets.yolo.load_test(imlink, short=512)

        #Detect cars here
        netClass_IDs, netScores, netBounding_boxs = self.cvModel(x)

        boxes = []
        scores = []
        class_IDs = []

        netBounding_boxs = netBounding_boxs.asnumpy()
        netBounding_boxs =netBounding_boxs  * 1.4066 #Converting back from 512 to 720 height 
        netScores = netScores.asnumpy()
        netClass_IDs = netClass_IDs.asnumpy()


        for i, bbox in enumerate(netBounding_boxs[0]):
            if(netScores[0][i]< self.thresh):
                break
            currentBox = [bbox[0].astype(int), bbox[1].astype(int), (bbox[2]-bbox[0]).astype(int), (bbox[3]-bbox[1]).astype(int)]
            boxes.append(currentBox)
            scores.append(netScores[0][i])
            class_IDs.append(self.NUM_CLASS[int(netClass_IDs[0][i])])

        #Match objects between frames
        finalBoxes = np.array(boxes) 
        finalNames = np.array(class_IDs)
        finalScores = np.array(scores)
        features = np.array(self.encoder(original_frame, finalBoxes))
        detections = [Detection(bbox, score, class_name, feature) for bbox, score, class_name, feature in zip(finalBoxes, finalScores, finalNames, features)]

        self.tracker.predict()
        self.tracker.update(detections)

        #Set new bounding boxes with IDs
        tracked_bboxes = []
        for track in self.tracker.tracks:
            if not track.is_confirmed() or track.time_since_update > 5:
                continue 
            bbox = track.to_tlbr() # Get the corrected/predicted bounding box
            class_name = track.get_class() #Get the class name of particular object
            tracking_id = track.track_id # Get the ID for the particular track
            index = self.key_list[self.val_list.index(class_name)] # Get predicted object index by object name
            tracked_bboxes.append( bbox.tolist() + [tracking_id, index] ) # Structure data, that we could use it with our draw_bbox function

        self.prevFrame = self.currFrame
        image = draw_bbox(original_frame, tracked_bboxes, CLASSES=YOLO_COCO_CLASSES, tracking=True)
        cv2.imwrite("../footage/newimage.jpg", image)
        self.boundingBoxes = tracked_bboxes
        #Return bounding boxes with carIDs to broker
        return tracked_bboxes

    def get_car_image(self, inputID):
        print("hi")
        for box in self.boundingBoxes:
            if(box[4] == inputID):
                return box

        return []
        #Cross reference inputID with stored IDs

        #Highlight location of ID car on the inputImg

        #Return highlighted image to broker