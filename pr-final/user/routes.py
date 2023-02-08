from flask import Flask, render_template, redirect, url_for, session, Response, request
import pymongo
from app import app
from user.models import User, Admin
import cv2
import os
import os.path
from face_code.Training_code import Training_encode
import face_recognition
import numpy as np
from app import db
#import datetime 
import shutil
from datetime import datetime, timedelta
@app.route('/user/signup', methods=['POST'])
def signup():
    return User().signup()

@app.route('/user/signout')
def user_signout():
    return User().signout()

@app.route('/user/login', methods=['POST'])
def login():
    return User().login()

@app.route('/admin/login', methods=['POST'])
def admin_login():
    return Admin().login()

@app.route('/admin/signout')
def admin_signout():
    return Admin().signout()


#-----------------------------------dashboard -----------------------------------------

@app.route('/templates/capture/')
def dashboard_capture():
    path_folder = session['user']['email']
    path = f'Images/{path_folder}'
    if os.path.isdir(path):
        return render_template('capture_templates/already_face.html') 
    else:
        return render_template('capture.html') 

@app.route('/templates/checkin/')
def dashboard_checkin():
    name = session['user']['name']
    date_time = datetime.now()
    today_date = date_time.strftime("%d-%m-%Y")
    if db.employee_time.find_one({ "name": name, "status": "check-in", "date": today_date }):
        return render_template("capture_templates/face_recognition_checkin_already.html")
    else:
        return render_template('face_recognition_checkin.html')     

@app.route('/templates/checkout/')
def dashboard_checkout():
    name = session['user']['name']
    date_time = datetime.now()
    today_date = date_time.strftime("%d-%m-%Y")
    if db.employee_time.find_one({ "name": name, "status": "check-out", "date": today_date }):
        return render_template("capture_templates/face_recognition_checkout_already.html")
    else:
        return render_template('face_recognition_checkout.html')     

@app.route('/templates/attendance/')
def dashboard_attendance():
    return render_template('attendance.html')

@app.route('/templates/to-do/')
def dashboard_taskmanager():
    return render_template('to-do.html')

@app.route('/templates/my-profile/')
def dashboard_myprofile():
    return render_template('my-profile.html')

@app.route('/templates/home/')
def dashboard_home():
    return render_template('home.html')

@app.route('/templates/admin-login/')
def dashboard_admin_login():
    return render_template('admin-login.html')



#----------------------------- Face capture code -----------------------------------

global capture, switch
capture=0
switch=1



def gen_frames(name, folder_name):  


    global out, capture,rec_frame
    camera = cv2.VideoCapture(0)

    try:
        parent_dir = "Images/"
        path = os.path.join(parent_dir, folder_name)
        os.mkdir(path)
    except:
        pass

    while True:
        success, frame = camera.read() 
        if success:  
            if(capture):
                capture=0
                file = f"Images/{folder_name}/{name}" + '.jpg'
                cv2.imwrite(file, frame)
                try:
                    Training_encode(folder_name)
                except:
                    pass
              
            try:
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            except Exception as e:
                pass
                
        else:
            pass

@app.route('/video_feed')
def video_feed():
    folder_name = session['user']['email']
    name = session['user']['name']
    return Response(gen_frames(name, folder_name), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/requests',methods=['POST','GET'])
def tasks():
    global switch,camera
    camera = cv2.VideoCapture(0)
    if request.method == 'POST':
        if request.form.get('click') == 'Capture':
            global capture
            capture=1
            camera.release()
            cv2.destroyAllWindows()

        elif  request.form.get('stop') == 'Stop/Start':
            
            if(switch==1):
                switch=0
                camera.release()
                cv2.destroyAllWindows()
                
            else:
                camera = cv2.VideoCapture(0)
                switch=1
                          
                 
    elif request.method=='GET':
        return redirect('/dashboard/')
    return redirect('/dashboard/')

    camera.release()
    cv2.destroyAllWindows()




#-------------------------------- RECOGNITION ------------------------------------   

def gen_frames1(name_for_rec, status):  

    global camera1
    path = f"Images/{name_for_rec}"
    images = []
    classNames = []
    myList = os.listdir(path)
    # print(myList)
    for cl in myList:
        curImg = cv2.imread(f'{path}/{cl}')
        images.append(curImg)
        classNames.append(os.path.splitext(cl)[0])
    camera1 = cv2.VideoCapture(0)
    #cap = cv2.VideoCapture(0)
    #print("4")
    numpy_load = np.load(f"Trained/{name_for_rec}/{name_for_rec}" + ".npy")
    print(numpy_load)
#----------------------------------- datetime code --------------------------------

    def markTiming(name):
        
        date_time = datetime.now()
        today_date = date_time.strftime("%d-%m-%Y")
        current_time = date_time.strftime("%H:%M:%S")

        if db.employee_time.find_one({ "name": name, "status": status, "date": today_date}):
            pass

        elif status == "check-out":
            if db.employee_time.find_one({ "name": name, "status": "check-in", "date": today_date }):
                checkin_time_for_work = db.employee_time.find_one({ "name": name, "status": "check-in", "date": today_date },{"time":1,"_id":0,})
                checkin_time_for_work1 = checkin_time_for_work.get("time")

                t1 = datetime.strptime(checkin_time_for_work1, "%H:%M:%S")
                t2 = datetime.strptime(current_time, "%H:%M:%S")
                delta = t2 - t1
                ms = delta.total_seconds()
                working_hour = str(timedelta(seconds=ms))

                # current_time_without_:a = current_time.replace(':', '')
                # checkin_time_without_:a = checkin_time_for_work1.replace(':', '')

                # working_hour = str(int(current_time_without_) - int(checkin_time_without_))
                # working_hour1 = ':'.join(working_hour[i:i+2] for i in range(0, len(working_hour), 2))

                time_to_insert_for_checkout = {
                    "name": name,
                    "status": status,
                    "date": today_date,
                    "time": current_time,
                    "working_time": working_hour
                    }

                db.employee_time.insert_one(time_to_insert_for_checkout)
            
        else:      
            time_to_insert = {
                "name": name,
                "status": status,
                "date": today_date,
                "time": current_time
                }
            db.employee_time.insert_one(time_to_insert)

            

    while True:

        success, frame = camera1.read()
        imgS = cv2.resize(frame, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        facesCurFrame = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

        for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame): 
            print(numpy_load)
            matches = face_recognition.compare_faces(numpy_load, encodeFace)
            faceDis = face_recognition.face_distance(numpy_load, encodeFace)
            # print(faceDis)
            matchIndex = np.argmin(faceDis)

            if matches[matchIndex]:
                name_for_rec1 = classNames[matchIndex]
                name_for_rec = classNames[matchIndex].upper()
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(frame, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(frame, name_for_rec, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 0.6, (255, 255, 255), 2)
                markTiming(name_for_rec1)
        try:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        except Exception as e:
            pass

    camera1.release()
    cv2.destroyAllWindows()

#-------------------------------- RECOGNITION ROUTES --------------------------------

@app.route('/video_feed_for_recognition_checkin')
def video_feed_for_recognition_checkin():
    status = "check-in"
    name_for_rec = session['user']['email']
    return Response(gen_frames1(name_for_rec, status), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/video_feed_for_recognition_checkout')
def video_feed_for_recognition_checkout():
    status = "check-out"
    name_for_rec = session['user']['email']
    #name = session['user']['name']
    return Response(gen_frames1(name_for_rec, status), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/attendance_done',methods=['POST','GET'])
def tasks1():
    global camera1
    camera1 = cv2.VideoCapture(0)
    # if request.method == 'POST':
        
    camera1.release()
    cv2.destroyAllWindows()
    return redirect('/dashboard/')
    # elif request.method=='GET':
    #     return redirect('/dashboard/')
    #     camera.release()
    #     cv2.destroyAllWindows()

        
    # return redirect('/dashboard/')
    # camera.release()
    # cv2.destroyAllWindows()

#-------------------------------- admin employee table -------------------------

# db = MongoEngine()
# db.init_app(app)

# class Employee(db.Document):
#     name = db.StringField()
#     status = db.StringField()
#     date = db.StringField()
#     time = db.StringField()
#     pub_date = db.DateTimeField(datetime.now)

@app.route('/admin/dashboard/employee/')
def admin_dashboard_employee():
    # employee_time = Employee.objects.all()
    users = db.users.find()
    #print(employee_time)
    return render_template('admin-dashboard-employee.html', users=users)

@app.route('/admin/dashboard/status/')
def admin_dashboard_status():
    # employee_time = Employee.objects.all()
    employee_time = db.employee_time.find()
    return render_template('admin-dashboard-status.html', employee_time=employee_time)



#----------------------route for deleting the entry of table -----------------------



@app.route('/delete/<string:getid>/<string:email>', methods = ['POST','GET'])
def delete_employee(getid, email):
    #print(getid)
    db.users.delete_one( { "_id": getid } )

    try:
        shutil.rmtree(f'C:/Ayyan/project/Time Clock Project/Images/{email}')
        shutil.rmtree(f'C:/Ayyan/project/Time Clock Project/Trained/{email}')
    except:
        pass
    return redirect('/admin/dashboard/employee/')
    

    
        

