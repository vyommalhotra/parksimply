from cars import carDetector
from matcher import Matcher

class Broker:
    def __init__(self, footage, skip):
        self.footage = footage
        self.frame_num = 0
        self.skip = skip
        self.matcher = Matcher() # keeps track of previous ID matches
        self.car_detector = carDetector()
    
    def get_spots(self):
        return []
    
    def get_cars(self, frame):
        return self.car_detector.get_cars()

    def get_spot_image(self, spot_id):
        pass

    def get_car_image(self, car_id, spot_image):
        pass
    
    def is_footage_open(self):
        return self.footage.isOpened()
    
    def process_frame(self):
        # get next frame from footage
        ret, frame = self.footage.read()
        
        # not end of footage
        if ret:

            # calibrate frame skipping 
            self.frame_num += self.skip
            self.footage.set(1, self.frame_num)

            # get spot Ids from spot class
            spot_ids = self.get_spots(frame)

            # get car Ids from car class
            car_ids = self.get_cars(frame)
            print("frame {} : IDS {}".format(self.frame_num, car_ids)) #TODO: remove this

            # provide current spot and car IDS
            self.matcher.set_ids([],[])

            # perform new matches
            matches = self.matcher.match()

            # for each pre-existing and new match
            for match in matches:
                # get image from spot class then car class 
                self.get_spot_image()
                self.get_car_image()

                # TODO: send image to front end
                pass

            # not done
            return False
        
        else:
            # done
            return True
        


    


    



