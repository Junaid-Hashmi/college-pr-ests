import os 
import cv2
global capture
capture = 0

def gen_frames(name):  # generate frame by frame from camera

    camera = cv2.VideoCapture(0)

    global out, capture,rec_frame

    try:
        parent_dir = "Images/"
        path = os.path.join(parent_dir, name)
        os.mkdir(path)
    except:
        pass

    while True:
        success, frame = camera.read() 
        if success:  
            if(capture):
                capture=0
                file = f"Images/{name}/{name}" + '.jpg'
                cv2.imwrite(file, frame)
                # now = datetime.datetime.now()
                # p = os.path.sep.join(['shots', "shot_{}.png".format(str(now).replace(":",''))])
                # cv2.imwrite(p, frame)
              
            try:
                ret, buffer = cv2.imencode('.jpg', cv2.flip(frame,1))
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            except Exception as e:
                pass
                
        else:
            pass