from tkinter import *
import serial
import time
import throttle
from PIL import ImageTk, Image

arduino = serial.Serial(port='/dev/cu.usbmodem1431401', baudrate=9600, timeout=.1)
master = Tk()
canvas_width = 800
canvas_height = 800

def serial_write(x):
    arduino.write(bytes(x, 'utf-8'))

def convertToDegrees(x,y):
    x = x/(canvas_width/180)
    y = y/(canvas_height/180)
    return int(x),int(y)

def motion(event):
    x, y = event.x, event.y
    if 0 <= x <= canvas_width and 0 <= y <= canvas_height:
        y = canvas_height-y
        x = canvas_width-x
        x,y = convertToDegrees(x,y)
        serial_write(f'X{x}Y{y}')
    # time.sleep(15)

def leftclick(event):
    serial_write('F')

w = Canvas(master, 
           width=canvas_width,
           height=canvas_height, background='gray75')
w.pack()
img = ImageTk.PhotoImage(Image.open("bill.jpg"))    
w.create_image(canvas_width/2,canvas_height/2, anchor=CENTER, image=img)   

master.bind('<Motion>', motion)
master.bind("<Button-1>", leftclick)
mainloop()