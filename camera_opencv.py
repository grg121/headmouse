import cv2
import pyautogui
from base_camera import BaseCamera

import numpy as np
# multiple cascades: https://github.com/Itseez/opencv/tree/master/data/haarcascades

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')


class Camera(BaseCamera):
    video_source = 0

    @staticmethod
    def set_video_source(source):
        Camera.video_source = source

    @staticmethod
    def frames():


        def DrawFace(face, img, color):
            x, y, w, h = face
            cv2.rectangle(img,(x,y),(x+w,y+h),color,2) # average

        def DrawReferences2(img, left, right, top, bot):
            cv2.line(img,(left,0),(left,img.shape[0]),(123,213,321),5)
            cv2.line(img,(right,0),(right,img.shape[0]),(123,213,321),5)
            cv2.line(img,(0,top),(img.shape[1],top),(123,213,321),5)
            cv2.line(img,(0,bot),(img.shape[1],bot),(123,213,321),5)

        def DrawReferences(img, horizontal, vertical):
            cv2.line(img,(horizontal,0),(horizontal,img.shape[0]),(255,255,0),5)
            cv2.line(img,(0,vertical),(img.shape[1],vertical),(255,255,0),5)

        def CenterOf(face):

            if(len(face) == 4):
                x, y, w, h = face
            else:
                x, y, w, h = 0, 0, 0, 0
                
            px = int(x+w/2)
            py = int(y+h/2)

            return px,py

        camera = cv2.VideoCapture(Camera.video_source)
        if not camera.isOpened():
            raise RuntimeError('Could not start camera.')


        _, img = camera.read()

        shape = img.shape

        x = y = 0

        left = right = int(shape[0]/2)

        top = bot = int(shape[1]/2)

        rate = 25

        face_buffer = []

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

                DrawFace(current_face, img, (0,255,255))

            average_face = np.mean(face_buffer, axis=0) # get average parameters of buffer faces
            # x,y,w,h

            DrawFace(average_face.astype('int'), img, (0,0,255))

            px,py = CenterOf(average_face)

            left = min(left,px)
            right = max(right, px)
            top = min(top, py)
            bot = max(bot, py)

            horizontal = int(left+(right-left)/2)
            vertical = int(top+(bot-top)/2)

            DrawReferences(img, horizontal, vertical)
            DrawReferences2(img, left, right, top, bot)

            cv2.circle(img,(px,py), 10, (0,255,255), -1)

            # encode as a jpeg image and return it
            yield cv2.imencode('.jpg', img)[1].tobytes()
