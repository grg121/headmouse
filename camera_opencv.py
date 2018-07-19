import cv2
import pyautogui
from base_camera import BaseCamera

import numpy as np
# multiple cascades: https://github.com/Itseez/opencv/tree/master/data/haarcascades

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
smile_cascade = cv2.CascadeClassifier('haarcascade_smile.xml')

pyautogui.FAILSAFE = False

class Camera(BaseCamera):
    video_source = 0

    @staticmethod
    def set_video_source(source):
        Camera.video_source = source

    @staticmethod
    def frames():


        def Draw(obj, img, color):
            x, y, w, h = obj
            cv2.rectangle(img,(x,y),(x+w,y+h),color,2) # average


        def CenterOf(obj):

            x, y, w, h = obj

            px = int(x+w/2)
            py = int(y+h/2)

            return px,py




        camera = cv2.VideoCapture(Camera.video_source)
        if not camera.isOpened():
            raise RuntimeError('Could not start camera.')


        _, img = camera.read()

        shape = img.shape

        center_x = int(shape[1]/2)
        center_y = int(shape[0]/2)

        x = y = 0

        rate = 15
        sensibility = 5

        face_buffer = []

        smiling = False
        will_smile = False

        while True:
            # read current frame

            _, img = camera.read()

            img =  cv2.flip( img, 1 )
            grayscale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            detected_faces = face_cascade.detectMultiScale(grayscale, 1.3, 5)
            if len(detected_faces) > 0:
                current_face = max(detected_faces, key=lambda x:x[2]*x[3]) # bigger face detected
                face_buffer.append(current_face)

                if len(face_buffer) == rate: # keep buffer size to rate
                    del face_buffer[0]

                Draw(current_face, img, (0,255,255))

                x,y,w,h = current_face

                roi_gray = grayscale[y:y+h, x:x+w]
                roi_color = img[y:y+h, x:x+w]

                smiles = smile_cascade.detectMultiScale(roi_gray, 1.6,15)

                will_simile = len(smiles) > 0

                if smiling:
                    pyautogui.mouseDown()
                    pyautogui.mouseDown()
                    pyautogui.mouseUp()
                """
                if smiling and not will_smile:
                    pyautogui.mouseUp()
                    cv2.putText(img,"up",(10,150), font , 2,(255,255,255),2,cv2.LINE_AA)
                if not smiling and will_smile:
                    pyautogui.mouseDown()
                    cv2.putText(img,"down",(10,150), font , 2,(255,255,255),2,cv2.LINE_AA)

                """

                smiling = will_smile

                for (sx,sy,sw,sh) in smiles:
                    cv2.rectangle(roi_color,(sx,sy),(sx+sw,sy+sh),(0,255,0),2)



            average_face = np.mean(face_buffer, axis=0) # get average parameters of buffer faces
            # x,y,w,h

            Draw(average_face.astype('int'), img, (0,0,255))

            px,py = CenterOf(average_face)

            h, w,_ = img.shape

            cv2.line(img,(int(w/2),0),(int(w/2),h),(255,123,0),2)
            cv2.line(img,(0,int(h/2)),(w,int(h/2)),(255,123,0),2)

            cv2.circle(img,(px,py), 10, (0,255,255), -1)

            desp_x = int((center_x-px)/sensibility)
            desp_y = int((center_y-py)/sensibility)

            font = cv2.FONT_HERSHEY_SIMPLEX

            pyautogui.moveRel(-desp_x, -desp_y, duration=0)

            # encode as a jpeg image and return it
            yield cv2.imencode('.jpg', img)[1].tobytes()
