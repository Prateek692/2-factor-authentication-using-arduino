#imported necessary files and libraries
import serial
import time
import face_recognition
import cv2
import numpy
import numpy as np
import pandas as pd
import docopt
from sklearn import svm
import os
import time

ser = serial.Serial('COM8', 9600, timeout=1)
time.sleep(2)

while True:
    data = ser.readline().decode().strip()
    if data:
        print(data)

    what=input('Enter pass:')
    if what=='open':
        ser.write(bytes('786', 'utf-8'))
        what2=input('Enter 2nd:')
        if what2=='now':
            ser.write(bytes('592', 'utf-8'))
            data = ser.readline().decode().strip()
            print(data)
        #print(ser.readline())
        continue
    elif what=='shut':
        break
    
ser.close()