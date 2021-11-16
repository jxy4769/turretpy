import serial
import time
import cv2
import sys
import os
import throttle
from time import sleep
from threading import Thread

arduino = serial.Serial(port='/dev/cu.usbmodem1431401', baudrate=9600, timeout=.1)
canvas_width = 800
canvas_height = 800

n = 0
@throttle.wrap(5, 1)
def fire():
    # global n
    # if n == 0 or n > 1:
    #     n += 1
    #     return
    serial_write('F')
    # n+=1

def serial_write(x):
    arduino.write(bytes(x, 'utf-8'))

def convertToDegrees(x,y):
    x = x/(canvas_width/180)
    y = y/(canvas_height/180)
    return int(x),int(y)

def motion(x, y):
    if 0 <= x <= canvas_width and 0 <= y <= canvas_height:
        y = canvas_height-y
        x = canvas_width-x
        x = x - (canvas_width*0.15) # CORRECTION
        x,y = convertToDegrees(x,y)
        print(f'X:{x} Y:{y}') # TODO: DELETE THIS LATER
        serial_write(f'X{x}Y{90}')

class ThreadedCamera(object):
    def __init__(self, src=0):
        self.capture = cv2.VideoCapture(0)
        self.capture.set(cv2.CAP_PROP_BUFFERSIZE, 2)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH,canvas_width)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT,canvas_height)

        self.FPS = 1/30
        self.FPS_MS = int(self.FPS * 1000)

        # Start frame retrieval thread
        self.thread = Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()

    def process(self):
        frame = self.frame
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )
        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            motion(x,y)

    def update(self):
        while True:
            if self.capture.isOpened():
                (self.status, self.frame) = self.capture.read()
                self.process()
            time.sleep(self.FPS)

    def show_frame(self):
        cv2.imshow('frame', self.frame)
        cv2.waitKey(self.FPS_MS)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            sys.exit()
        
        if cv2.waitKey(1) & 0xFF == ord('f'):
            fire()



cascPath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)

threaded_camera = ThreadedCamera()

while True:
    try:
        threaded_camera.show_frame()
    except AttributeError:
        pass