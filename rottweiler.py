#!/usr/bin/env python
# coding: utf-8

# In[2]:


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


# incorrect = 0
# password = "1234"
# locked = True



def face_recognize_test(test):
    start = time.time()
    # Load the test image with unknown faces into a numpy array
    test_image = face_recognition.load_image_file(test)

    # Find all the faces in the test image using the default HOG-based model
    face_locations = face_recognition.face_locations(test_image)
    no = len(face_locations)
    print("Number of faces detected: ", no)

    # Predict all the faces in the test image using the trained classifier
    print("Found:")
    for i in range(no):
        test_image_enc = face_recognition.face_encodings(test_image, known_face_locations=[face_locations[i]])[0]
        name = "Unknown"
        predict_name = "Unknown"
        face_distances = face_recognition.face_distance(encodings, test_image_enc)
        # Get the index of the closest matching face
        best_match_index = np.argmin(face_distances)

        # If the distance is less than 0.6, then we have a match
        if face_distances[best_match_index] < 0.55:
            name = names[best_match_index]
            predict_name = name

        print(predict_name)

    end = time.time()
    print('Time taken for testing: ', end - start, 'seconds')








ser = serial.Serial('COM7', 9600, timeout=1)
time.sleep(2)



def main_function():
    print("correct face")


guessed=False 
incorrect_count=0


text=[]

while True:
    line = ser.readline().decode("utf-8")
    if line =="":
        pass
    else:
        try:
            text.append(int(line))
            print(text)
        except:
            if (line[0])== 'A':
                if text == []:
                    pass
                else:
                    text.pop()
                    print(text)

            if (line[0])== 'B':
                if text == []:
                    pass
                else:
                    if text==[1,2,3]:
                        print("correct passsword")
                        guessed=True
                    else:
                        print("incorrect password")
                        incorrect_count+=1
                        if incorrect_count==5:
                            break

            elif (line[0]) == 'C' and guessed:
                print('Is it here?')
                
                
                
                
                
                # yaha se shuru hai webcam


                # Load the face encodings from the CSV file
                df = pd.read_csv('face_encodings.csv')
                df1 = pd.read_csv('names.csv')
                # Convert the DataFrame to a list of lists
                encodings = df.values.tolist()
                names= df1.values.tolist()
                cap = cv2.VideoCapture(0)

                # Check if the camera was opened successfully
                if not cap.isOpened():
                    print("Error opening camera")

                # Loop to capture images
                while True:
                    # Capture frame-by-frame
                    ret, frame = cap.read()

                    # Check if the frame was read successfully
                    if not ret:
                        break

                    # Display the resulting frame
                    cv2.imshow('frame', frame)

                    # Press 's' key to save the image
                    if cv2.waitKey(1) & 0xFF == ord('s'):
                        # Generate a unique filename for the image
                        filename = f"captured_image.jpg"
                        # Save the image
                        cv2.imwrite(filename, frame)
                        print(f"Image saved as {filename}")
                        break

                # Release the camera and close the window
                cap.release()
                cv2.destroyAllWindows()

                # yaha se khatam hai webcam

                parent_dir = "AI Tools"
                test_image = "captured_image.jpg"





                # test_list = ['avenger.jpeg', 'avilol.jpg','avilol1.jpg','avilol2.jpg','avilol3.jpg','avilol4.jpg','avilol5.jpg','avilol6.jpg','avilol7.jpg','avilol8.jpg', 'cast.jpeg', 'hulk.jpeg', 'olsen.jpeg', 'test_image.jpg', 'women.jpeg', 'brie.jpeg', 'liz.jpeg', 'scarlett.jpeg']
                # for image in test_list:
                face_recognize_test(test_image)
                print()
                
                
                
                
                
                
                break
                    



# In[ ]:




