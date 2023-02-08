import os 
import cv2


def capture_image(name):
    
    # making folder
    #name = "Ayyan7"
    parent_dir = "Images/"
    path = os.path.join(parent_dir, name)
    os.mkdir(path)

    import cv2

    cam = cv2.VideoCapture(0)

    count = 0

    while True:
        ret, img = cam.read()

        cv2.imshow("Test", img)

        if not ret:
            break

        k = cv2.waitKey(1)

        if k % 256 == 27:
            # For Esc key
            print("Close")
            break
        elif k % 256 == 32:
            # For Space key

            print("Image " + str(count) + "saved")
            file = f"Images/{name}/{name}" + str(count) + '.jpg'
            cv2.imwrite(file, img)
            count += 1

    cam.release()
    cv2.destroyAllWindows()

    return " "
#capture_image()