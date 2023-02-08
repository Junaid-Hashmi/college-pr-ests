import os
import cv2
from numpy import *
import face_recognition


def Training_encode(name_for_training):
    try:
        # makin path
        parent_dir = "Trained/"
        path_train = os.path.join(parent_dir, name_for_training)
        os.mkdir(path_train)

        path = f"Images/{name_for_training}"
        images = []
        classNames = []
        myList = os.listdir(path)
        #print(myList)
        for cl in myList:
            curImg = cv2.imread(f'{path}/{cl}')
            images.append(curImg)
            classNames.append(os.path.splitext(cl)[0])
        #print(classNames)
        
        def findEncodings(images):
            encodeList = []
            for img in images:
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                encode = face_recognition.face_encodings(img)[0]
                encodeList.append(encode)
            print(encodeList)
            return encodeList
            # return numpy.tolist(encodeList)
        encodeListKnown = findEncodings(images)
        Numpy_path = f"Trained/{name_for_training}/{name_for_training}" + ".npy"
        save(Numpy_path, encodeListKnown)
        #print('Encoding Complete')
    except:
        pass

