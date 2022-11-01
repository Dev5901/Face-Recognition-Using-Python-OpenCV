import numpy as np
import cv2
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
import pickle
import os
import imutils

curr_path = os.getcwd()#current working directory

print("Loading face detection model")
proto_path = os.path.join(curr_path, 'model', 'deploy.prototxt')#joining various path components
model_path = os.path.join(curr_path, 'model', 'res10_300x300_ssd_iter_140000.caffemodel')
face_detector = cv2.dnn.readNetFromCaffe(prototxt=proto_path, caffeModel=model_path) #load model from disk

print("Loading face recognition model")
recognition_model = os.path.join(curr_path, 'model', 'openface_nn4.small2.v1.t7')#joining various path components
face_recognizer = cv2.dnn.readNetFromTorch(model=recognition_model)

data_base_path = os.path.join(curr_path, 'database')

filenames = [] #list for storing path of each png or jpg file in database
for path, subdirs, files in os.walk(data_base_path):
    for name in files:
        filenames.append(os.path.join(path, name))

face_embeddings = []
face_names = []

for (i, filename) in enumerate(filenames):
    n=1
    print("Processing image {}".format(filename))

    image = cv2.imread(filename) #loading images into image variable
    image = imutils.resize(image, width=600) #preserves actual aspect ratio

    (h, w) = image.shape[:2]#getting height and width

    image_blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0), False, False) #creating  image blob, blobs can store binary data, they can be used to store images

    face_detector.setInput(image_blob) #providing image to face detector model
    face_detections = face_detector.forward() #fetching results

    i = np.argmax(face_detections[0, 0, :, 2])
    confidence = face_detections[0, 0, i, 2]



    if confidence >= 0.5: #consider only if confidence score is > 50% else ignore it

        box = face_detections[0, 0, i, 3:7] * np.array([w, h, w, h]) #extracting face box
        (startX, startY, endX, endY) = box.astype("int")

        face = image[startY:endY, startX:endX] #contains the img of face, cropped face

        face_blob = cv2.dnn.blobFromImage(face, 1.0/255, (96, 96), (0, 0), True, False) #creating face blob

        face_recognizer.setInput(face_blob) #providing face to face recognizer model
        face_recognitions = face_recognizer.forward() #fetching results

        name = filename.split(os.path.sep)[-2] #extracting name of person of that face i.e folder name

        face_embeddings.append(face_recognitions.flatten()) #storing face embeddings in list
        face_names.append(name) #storing face name in list


data = {"embeddings": face_embeddings, "names": face_names} #creating dictionary

le = LabelEncoder()
labels = le.fit_transform((data["names"]))#Fit label encoder and return encoded labels

recognizer = SVC(C=1.0, kernel="linear", probability=True) #Support Vector Classifier, to fit data on graph for comparison
recognizer.fit(data["embeddings"], labels)#Fit label encoder

#saving all data
f = open('recognizer.pickle', "wb")
f.write(pickle.dumps(recognizer))
f.close()

f = open("le.pickle", "wb")
f.write(pickle.dumps(le))
f.close()

#after running training.py file it will create two pickel files, 1)recognizer.pickle, 2)le.pickle
#Python pickle module is used for serializing and de-serializing a Python object structure. Any object in Python can be pickled so that it can be saved on disk. What pickle does is that it “serializes” the object first before writing it to file. Pickling is a way to convert a python object (list, dict, etc.) into a character stream. The idea is that this character stream contains all the information necessary to reconstruct the object in another python script.