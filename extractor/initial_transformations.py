import cv2
import numpy as np
import matplotlib.pyplot as plt

class transformer:
    def birds_eye(frame):
        # temporary test
        img = cv2.imread('footage/screenshot.png')
        src = np.float32([[1265, 512], [117, 1424], [2538, 1504], [1914, 517]])
        dst = np.float32([[0,0],[0,800],[1200, 800],[1200,0]])
        M = cv2.getPerspectiveTransform(src, dst)
        warped_img = cv2.warpPerspective(img, M, (2880, 1626))
        plt.imshow(warped_img) # Show results
        plt.show()

    def get_car_vectors(self):
        return 0

if __name__ == '__main__':
    transformer.birds_eye('')