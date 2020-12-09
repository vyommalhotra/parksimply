from matplotlib import pyplot as plt
from gluoncv import model_zoo, data, utils
from yolov3.utils import draw_bbox, read_class_names
from yolov3.configs import *
from deep_sort import nn_matching
from deep_sort.detection import Detection
from deep_sort.tracker import Tracker
from deep_sort import generate_detections as gdet
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
        self.thresh = 0.5

        NUM_CLASS = read_class_names(YOLO_COCO_CLASSES)
        key_list = list(NUM_CLASS.keys()) 
        val_list = list(NUM_CLASS.values())

        #Creating deep sort object, these parameters can be massaged
        max_cosine_distance = 0.7
        nn_budget = None
        model_filename = 'model_data/mars-small128.pb'
        self.encoder = gdet.create_box_encoder(model_filename, batch_size=1)
        metric = nn_matching.NearestNeighborDistanceMetric("cosine", max_cosine_distance, nn_budget)
        self.tracker = Tracker(metric)

        #Creating our model, we can change this to other models if needed. Check model zoo online for more.
        self.cvModel = model_zoo.get_model('yolo3_darknet53_coco', pretrained=True)

    def get_cars(inputFrame):
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
        netScores = netScores.asnumpy()
        netClass_IDs = netClass_IDs.asnumpy()


        for i, bbox in enumerate(netBounding_boxs[0]):
            if(netScores[0][i]< self.thresh):
                break
            currentBox = [((bbox[2]+bbox[0])/2).astype(int), ((bbox[3]+bbox[1])/2).astype(int), (bbox[2]-bbox[0]).astype(int), (bbox[3]-bbox[1]).astype(int)]
            boxes.append(currentBox)
            scores.append(netScores[0][i])
            class_IDs.append(NUM_CLASS[int(netClass_IDs[0][i])])

        #Match objects between frames
        finalBoxes = np.array(boxes) 
        finalNames = np.array(class_IDs)
        finalScores = np.array(scores)
        features = np.array(encoder(original_frame, finalBoxes))
        detections = [Detection(bbox, score, class_name, feature) for bbox, score, class_name, feature in zip(finalBoxes, finalScores, finalNames, features)]

        tracker.predict()
        tracker.update(detections)

        #Set new bounding boxes with IDs
        tracked_bboxes = []
        for track in tracker.tracks:
            if not track.is_confirmed() or track.time_since_update > 5:
                continue 
            bbox = track.to_tlbr() 
            class_name = track.get_class() 
            tracking_id = track.track_id 
            index = key_list[val_list.index(class_name)]
            if(index ==2):
                tracked_bboxes.append([tracking_id] + bbox.tolist()) 

        self.prevFrame = self.currFrame

        #Return bounding boxes with carIDs to broker
        return tracked_bboxes

    def get_car_image(inputID, inputImg):
        print("hi")
        #Cross reference inputID with stored IDs

        #Highlight location of ID car on the inputImg

        #Return highlighted image to broker