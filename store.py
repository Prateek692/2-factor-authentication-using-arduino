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

encodings = []
names = []

def face_recognize_train(dir):
    start = time.time()

    # Training the SVC classifier
    # The training data would be all the face encodings from all the known images and the labels are their names

    # Training directory
    if not dir.endswith('/'):
        dir += '/'
    train_dir = os.listdir(dir)

    # Loop through each person in the training directory
    for person in train_dir:
        pix = os.listdir(dir + person)

        # Loop through each training image for the current person
        for person_img in pix:
            # Get the face encodings for the face in each image file
            face = face_recognition.load_image_file(dir + person + "/" + person_img)
            face_bounding_boxes = face_recognition.face_locations(face)

            # If training image contains exactly one face
            if len(face_bounding_boxes) == 1:
                face_enc = face_recognition.face_encodings(face)[0]
                # Add face encoding for current image with corresponding label (name) to the training data
                encodings.append(face_enc)
                names.append(person)
            else:
                print(person + "/" + person_img + " can't be used for training")

    # Create and train the SVC classifier
    clf = svm.SVC(gamma='scale')
    clf.fit(encodings, names)
    end = time.time()
    print('Time taken for training: ', end - start, 'seconds')
    
parent_dir = "AI Tools"
train_dir = os.path.join(parent_dir, 'train_dir')
face_recognize_train(train_dir)

df = pd.DataFrame(columns=[f'col_{i+1}' for i in range(128)])
df1 = pd.DataFrame(columns=[f'col_{i+1}' for i in range(1)])
for row in encodings:
    df = df.append(pd.Series(row, index=df.columns), ignore_index=True)
for row in names:
    df1 = df1.append(pd.Series(row, index=df1.columns), ignore_index=True)
df.to_csv('AI Tools/face_encodings.csv', index=False)
df1.to_csv('AI Tools/names.csv',index=False)