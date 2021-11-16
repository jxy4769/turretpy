import serial
import time

arduino = serial.Serial(port='/dev/cu.usbmodem1411301', baudrate=9600, timeout=.1)
def write_read(x):
    arduino.write(bytes(x, 'utf-8'))

while True:
    num = input("Enter a number: ") # Taking input from user
    arduino.write(bytes(num, 'utf-8'))
