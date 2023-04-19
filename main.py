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

#face recognition function
def face_recognize_test(test):
    start = time.time() #noting the start time
    test_image = face_recognition.load_image_file(test)     # Load the test image with unknown faces into a numpy array

    # Find all the faces in the test image using the default HOG-based model
    face_locations = face_recognition.face_locations(test_image)
    no = len(face_locations)
    print("Number of faces detected: ", no)
    identified=True
    # Predict all the faces in the test image using the trained classifier
    print("Found:")
    for i in range(no):
        test_image_enc = face_recognition.face_encodings(test_image, known_face_locations=[face_locations[i]])[0]
        name = "Unknown"
        predict_name = "Unknown"
        face_distances = face_recognition.face_distance(encodings, test_image_enc)
        # Get the index of the closest matching face
        best_match_index = np.argmin(face_distances)

        # If the euclidean distance is less than 0.55, then we have a match
        if face_distances[best_match_index] < 0.55:
            name = names[best_match_index]
            predict_name = name
        if predict_name=='Unknown':
            identified=False
        print(predict_name) #print name of recognized person, print Unknown if person not recognized
        # move_servo('open')

    end = time.time() #noting the end time
    print('Time taken for testing: ', end - start, 'seconds') #Printing total processing time to recognize people in single images
    if no==0:
        identified=False
    return identified
#establishing serial connection with arduino using port com7



ser = serial.Serial('COM8', 9600, timeout=1)
time.sleep(2)


guessed=False 
incorrect_count=0
current_password="123"
password=""
while 1:
    data=ser.readline().decode().strip()
    if(data==""):
        continue 
    if data>='1' and data<='9':
        ser.write(bytes('written', 'utf-8'))
        password+=data
    if data=='A':
        if password!="":
            password=password[:-1]
    if data=='B':
        if password!="":
            if password==current_password:
                print('Correct Password')
                guessed=True
                ser.write(bytes('part1', 'utf-8'))
            else:
                print('Incorrect Password')
                incorrect_count+=1
                if incorrect_count==5:
                    print('Too many incorrect attempts')
                    ser.write(bytes('enough', 'utf-8'))
                    break
                ser.write(bytes('wrong', 'utf-8'))
        
    if guessed==True:
        # yaha se shuru hai webcam
        # Load the face encodings from the CSV file
        df = pd.read_csv('AI Tools/face_encodings.csv')
        df1 = pd.read_csv('AI Tools/names.csv')
        # Convert the DataFrame to a list of lists
        encodings = df.values.tolist()
        names= df1.values.tolist()
        cap = cv2.VideoCapture(0)

        # Check if the camera was opened successfully
        if not cap.isOpened():
            print("Error opening camera")

        prev=time.time()

        # Loop to capture images
        while True:
            # Capture frame-by-frame
            ret, frame = cap.read()

            # Check if the frame was read successfully
            if not ret:
                break

            # Display the resulting frame
            cv2.imshow('frame', frame)
            curr=time.time()
            # Press 's' key to save the image
            if cv2.waitKey(1) & (0xFF == ord('s') or curr-prev>=10 ):
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
        unlock=face_recognize_test(test_image)
        if unlock==True:
            ser.write(bytes('part2', 'utf-8'))
        else:
            ser.write(bytes('wrong', 'utf-8'))
        print()
        os.remove(test_image)
        break
    if data=='*':
        ser.write(bytes('wrong', 'utf-8'))
        break
    print(password)

