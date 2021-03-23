from cars import carDetector #import from carsGluon if you wanna use gluon
from matcher import Matcher
from spots import spotDetector

class Broker:
    def __init__(self, footage, skip):
        self.footage = footage
        self.frame_num = 0
        self.skip = skip
        self.matcher = Matcher() # keeps track of previous ID matches
        self.car_detector = carDetector()
        self.spot_detector = spotDetector()
        self.spotsArray = []
        self.get_spots()
        self.give_spots()
    
    def get_spots(self):
        self.spotsArray = self.spot_detector.returnSpots()
        return self.spotsArray

    def give_spots(self):
        self.car_detector.get_spots(self.spotsArray)
    
    def get_cars(self, frame):
        return self.car_detector.get_cars(frame)

    def get_spot_image(self, spot_id):
        pass

    def get_car_image(self, car_id, spot_image):
        pass
    
    def is_footage_open(self):
        return self.footage.isOpened()

    def write_to_buffer(self, frame_num, car_ids):
        f = open("api/buffer.txt", "w")
        f.write("frame {} : IDS {}\n".format(frame_num, car_ids))
        f.close
    
    def process_frame(self):
        # get next frame from footage
        ret, frame = self.footage.read()
        
        # not end of footage
        if ret:

            # calibrate frame skipping 
            self.frame_num += self.skip
            self.footage.set(1, self.frame_num)

            # get spot Ids from spot class
            

            # get car Ids from car class
            car_ids = self.get_cars(frame)
            #print("frame {} : IDS {}".format(self.frame_num, car_ids)) #TODO: <- remove this
            self.write_to_buffer(self.frame_num, car_ids)
            # provide current spot and car IDS
            self.matcher.set_ids([],[])

            # perform new matches
            matches = self.matcher.match()

            # for each pre-existing and new match
            #for match in matches:
                # get image from spot class then car class 
            #    self.get_spot_image()
                #self.get_car_image()
            #print(self.car_detector.get_car_image(2))
            if(self.frame_num == 15):
                self.car_detector.matchCar(2)

                # TODO: send image to front end
            #    pass

            # not done
            return False
        
        else:
            # done
            self.car_detector.out.release()
            self.write_to_buffer(0,0)
            return True
        


    


    



