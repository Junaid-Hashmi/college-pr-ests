import cv2
import os 


count = 0

class Video(object):
    def __init__(self, name):
        self.video=cv2.VideoCapture(0)
        self.name = name
        global c 
        c=0
        parent_dir = "Images/"
        path = os.path.join(parent_dir, name)
        os.mkdir(path)
    def __del__(self):
        self.video.release()
    def get_frame(self):
        ret,frame=self.video.read()

        # # if not ret:
        # #     break
        # k = cv2.waitKey(1)

        # if k % 256 == 27:
        #     # For Esc key
        #     print("Close")
        #     #break
        # elif k % 256 == 32:
        #     # For Space key
        if c == 0:
            print("Image " + str(count) + "saved")
            file = f"Images/{name}/{name}" + str(count) + '.jpg'
            cv2.imwrite(file, img)
            count += 1
            c = 1

        

        ret,jpg=cv2.imencode('.jpg',frame)
        return jpg.tobytes()