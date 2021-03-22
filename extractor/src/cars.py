from yolov3.utils import Load_Yolo_model, image_preprocess, postprocess_boxes, nms, draw_bbox, read_class_names
from yolov3.configs import *
from deep_sort import nn_matching
from deep_sort.detection import Detection
from deep_sort.tracker import Tracker
from deep_sort import generate_detections as gdet
import cv2
import numpy as np
import tensorflow as tf
from shapely.geometry import Polygon , box

#Check out demo_yolo.py for explanation on how to set the model up

#Object Tracking links
# https://www.pyimagesearch.com/2018/07/23/simple-object-tracking-with-opencv/
# https://www.learnopencv.com/object-tracking-using-opencv-cpp-python/
# http://davheld.github.io/GOTURN/GOTURN.html

class spotObject:
    def __init__(self, index, polygon):  
        self.index = index  
        self.polygon = polygon
        self.isOccupied = False

class carDetector:

    def __init__(self):
        self.prevFrame = None #Store previous frame, don't know if we'll need this
        self.boundingBoxes = [] #Store bounding boxes of previous frame, will likely need this for object tracking
        self.currFrame = None
        self.openParkingSpots = []
        self.assignedParkingSpots=[]
        self.occupiedParkingSpots=[]
        self.matched = []
        self.matchedCars = []

        #Threshold of what is a car
        self.thresh = 0.7
        self.input_size = YOLO_INPUT_SIZE
        self.iou_threshold=0.45

        self.NUM_CLASS = read_class_names(YOLO_COCO_CLASSES)
        self.key_list = list(self.NUM_CLASS.keys()) 
        self.val_list = list(self.NUM_CLASS.values())
        self.Track_only = ["car", "truck"]

        #Creating deep sort object, these parameters can be massaged
        max_cosine_distance = 0.7
        nn_budget = None
        model_filename = 'model_data/mars-small128.pb'
        self.encoder = gdet.create_box_encoder(model_filename, batch_size=1)
        metric = nn_matching.NearestNeighborDistanceMetric("cosine", max_cosine_distance, nn_budget)
        self.tracker = Tracker(metric)

        #Creating our model, we can change this to other models if needed. Check model zoo online for more.
        self.cvModel = Load_Yolo_model()
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.out = cv2.VideoWriter('../footage/TrimmedVidDemo.mp4', fourcc, 1, (1280, 720)) # output_path must be .mp4
        print("init carDetector")


    def get_bounding_box_iou(self, box1, box2):

        left=max(box1[0], box2[0])
        top=max(box1[1], box2[1])
        right=min(box1[2], box2[2])
        bottom=min(box1[3], box2[3])

        if(right<left or bottom < top):
            return 0.0
        
        intersect_area = (right - left + 1) * (bottom - top + 1)
        area1 = (box1[2] - box1[0] + 1 ) * (box1[3] - box1[1] +1)
        area2 = (box2[2] - box2[0] + 1 ) * (box2[3] - box2[1] +1)

        iou = intersect_area / (float(area1 + area2 -intersect_area))
        return iou

    def getPolygonIntersection(self, poly1, poly2):
        overlap = poly1.intersection(poly2).area
        total = poly1.area + poly2.area - overlap
        return overlap/total
    
    def markSpots(self):
        polyImage = self.currFrame.copy()
        for poly in self.openParkingSpots:
            originalPoly = poly
            poly = poly.polygon
            int_coords = lambda x: np.array(x).round().astype(np.int32)
            exterior = [int_coords(poly.exterior.coords)]
            
            if(self.checkIfOccupied(poly)):
                cv2.fillPoly(polyImage, exterior, [0, 0, 255 ])
                self.occupiedParkingSpots.append(originalPoly)
            else:
                cv2.fillPoly(polyImage, exterior, [0, 225, 0])
        for poly in self.assignedParkingSpots:
            originalPoly = poly
            poly = poly.polygon
            int_coords = lambda x: np.array(x).round().astype(np.int32)
            exterior = [int_coords(poly.exterior.coords)]
            if(self.checkIfOccupied(poly)):
                cv2.fillPoly(polyImage, exterior, [0, 0, 255 ])
                self.assignedParkingSpots.remove(originalPoly)
                self.occupiedParkingSpots.append(originalPoly)
            else: 
                cv2.fillPoly(polyImage, exterior, [0, 255, 255 ])
        for poly in self.occupiedParkingSpots:
            originalPoly = poly
            poly = poly.polygon
            int_coords = lambda x: np.array(x).round().astype(np.int32)
            exterior = [int_coords(poly.exterior.coords)]
            if(self.checkIfOccupied(poly)):
                cv2.fillPoly(polyImage, exterior, [0, 0, 255 ])
            else: 
                cv2.fillPoly(polyImage, exterior, [0, 255, 0 ])
                self.occupiedParkingSpots.remove(originalPoly)
                self.openParkingSpots.append(originalPoly)
        image = cv2.addWeighted(polyImage, 0.3, self.currFrame, 0.7, 0.0)
        cv2.imwrite("../footage/poly.jpg", image)
        self.out.write(image)
        return
    
    def checkIfOccupied(self, poly):
        for car in self.boundingBoxes:
            carPoly = self.convertBbToPolygon(car)
            if(self.getPolygonIntersection(poly, carPoly) > 0.3):
                return True
        return False

    def get_spots(self, spotsArray):
        i = 0
        print(self.openParkingSpots)
        for spot in spotsArray:
            self.openParkingSpots.append(spotObject(i, spot))
            i = i+1
        

    def matchCar(self, carID):
        if(len(self.openParkingSpots ) < 1):
            print("No Open Spots")
            return
        if(carID in self.matchedCars):
            print("Car already matched")
            return
        else:
            selectedSpot = self.openParkingSpots.pop()
            newMatch = (selectedSpot.index, carID)
            self.matched.append(newMatch)
            self.matchedCars.append(carID)
            self.assignedParkingSpots.append(selectedSpot)
            print(self.matched)


    def convertBbToPolygon(self, bbox):
        poly = box(bbox[0], bbox[1], bbox[2], bbox[3], True)
        return poly
        print("Poly")

    def convertPolygonToBb(self, poly):
        print("Bb")

    def get_cars(self, inputFrame):
        self.currFrame = inputFrame

        original_frame = cv2.cvtColor(self.currFrame, cv2.COLOR_BGR2RGB)
        original_frame = cv2.cvtColor(original_frame, cv2.COLOR_BGR2RGB)

        image_data = image_preprocess(np.copy(original_frame), [self.input_size, self.input_size])
        #image_data = tf.expand_dims(image_data, 0)
        image_data = image_data[np.newaxis, ...].astype(np.float32)

        #Detect cars here
        pred_bbox = self.cvModel(image_data)

        pred_bbox = [tf.reshape(x, (-1, tf.shape(x)[-1])) for x in pred_bbox]
        pred_bbox = tf.concat(pred_bbox, axis=0)

        bboxes = postprocess_boxes(pred_bbox, original_frame, self.input_size, self.thresh)
        bboxes = nms(bboxes, self.iou_threshold, method='nms')

        # extract bboxes to boxes (x, y, width, height), scores and names
        boxes, scores, names = [], [], []
        for bbox in bboxes:
            if len(self.Track_only) !=0 and self.NUM_CLASS[int(bbox[5])] in self.Track_only or len(self.Track_only) == 0:
                boxes.append([bbox[0].astype(int), bbox[1].astype(int), bbox[2].astype(int)-bbox[0].astype(int), bbox[3].astype(int)-bbox[1].astype(int)])
                scores.append(bbox[4])
                names.append(self.NUM_CLASS[int(bbox[5])])

        #Match objects between frames
        finalBoxes = np.array(boxes) 
        finalNames = np.array(names)
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
        self.markSpots()
        self.boundingBoxes = tracked_bboxes
        #Return bounding boxes with carIDs to broker
        return tracked_bboxes

    def get_car_image(self, inputID):
        for box in self.boundingBoxes:
            if(box[4] == inputID):
                verticies = np.array( [[[box[0],box[1]],[box[2],box[1]],[box[2],box[3]],[box[0],box[3]]]], dtype=np.int32 )
                polyImage = self.currFrame.copy()
                cv2.fillPoly(polyImage, verticies, 255)
                image = cv2.addWeighted(polyImage, 0.3, self.currFrame, 0.7, 0.0)
                cv2.imwrite("../footage/blueSelection.jpg", image)
                return image
        return []
        #Cross reference inputID with stored IDs

        #Highlight location of ID car on the inputImg

        #Return highlighted image to broker
