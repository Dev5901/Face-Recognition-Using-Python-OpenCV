import numpy as np
import pickle
import os
import cv2
import time
import datetime
import imutils
import collections
from tkinter import *
from tkinter import messagebox, filedialog

from self import self

curr_path = os.getcwd()

print("Loading face detection model")
proto_path = os.path.join(curr_path, 'model', 'deploy.prototxt')
model_path = os.path.join(curr_path, 'model', 'res10_300x300_ssd_iter_140000.caffemodel')
face_detector = cv2.dnn.readNetFromCaffe(prototxt=proto_path, caffeModel=model_path)

print("Loading face recognition model")
recognition_model = os.path.join(curr_path, 'model', 'openface_nn4.small2.v1.t7')
face_recognizer = cv2.dnn.readNetFromTorch(model=recognition_model)

recognizer = pickle.loads(open('recognizer.pickle', "rb").read())
le = pickle.loads(open('le.pickle', "rb").read())

def filedDialog1(self):
    self.filename4 = filedialog.askopenfilename(initialdir="/", title="Select a Video",
                                                filetype=(("mp4", ".mp4"), ("All Files", ".*")))
    messagebox.showinfo("Success", "Video file chosen! \nPath= " + self.filename4)
    return self.filename4

vs = cv2.VideoCapture(filedDialog1(self))
time.sleep(3) #delay of 3 sec
print("Starting test video file")

names = []
dictinitial = {}
dictfinal= {}

def most_frequent(List):
    counter = 0
    num = List[0]

    for i in List:
        curr_frequency = List.count(i)
        if (curr_frequency > counter):
            counter = curr_frequency
            num = i

    return num

while True:

    ret, frame = vs.read()#read face from frame
    frame = imutils.resize(frame, width=600)#resizing frame

    (h, w) = frame.shape[:2]#extracting height and width

    image_blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0), False, False)

    face_detector.setInput(image_blob)#providing face blob to face detector
    face_detections = face_detector.forward()#fetching results

    #iterating through fetched results
    for i in range(0, face_detections.shape[2]):
        confidence = face_detections[0, 0, i, 2]

        if confidence >= 0.5:#consider only if confidence score is > 50% else ignore it
            box = face_detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            face = frame[startY:endY, startX:endX]#contains face in particular frame

            (fH, fW) = face.shape[:2]#extracting width and height

            face_blob = cv2.dnn.blobFromImage(face, 1.0/255, (96, 96), (0, 0, 0), True, False)

            face_recognizer.setInput(face_blob)#providing face blob to face recogniser
            vec = face_recognizer.forward()#fetching results

            preds = recognizer.predict_proba(vec)[0]#predicting confidence score
            j = np.argmax(preds)
            proba= preds[j]#confidence score
            name = le.classes_[j]#fetching name of face

            text = "{}: {:.2f}".format(name, proba* 100)#person name and confidence score
            y = startY - 10 if startY - 10 > 10 else startY + 10
            cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 0, 255), 2)#drawing rectangle on face of input video
            cv2.putText(frame, text, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 0, 255), 2)#putting text on that frame showing rectangle

            names.append(name)#inserting name in names list
            camtime = vs.get(cv2.CAP_PROP_POS_MSEC) / 1000.  # this is the timestamp in camera time
            if name not in dictinitial:
                dictinitial[name] = camtime
            dictfinal[name]= camtime
            sec = "{:.2f}".format(camtime)
            cv2.putText(frame, sec, (10,30),cv2.FONT_HERSHEY_SIMPLEX, 1,(255,255,255),2,cv2.LINE_AA)
            print(name,":",sec,"seconds")
            if proba*100>60:
                break


    cv2.imshow("Frame", frame)#displaying frames of video
    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):#stop program on pressing q button
        break

#count the number of frames
frames = vs.get(cv2.CAP_PROP_FRAME_COUNT)
fps = int(vs.get(cv2.CAP_PROP_FPS))

# calculate duration of the video
seconds = int(frames / fps)
video_time = str(datetime.timedelta(seconds=seconds))
#print("duration in seconds:", seconds)
#print("\nLength of the video is:", video_time)
#Count how many times a particular person name is shown
#x=collections.Counter(names)
#print("Most common faces are: ")
#print(x.most_common())
#print("\nMost frequently occuring face is :  ")
#print(most_frequent(names))
#listToStr = ' '.join([str(elem) for elem in x.most_common()])

class gui:

    def __init__(self,root):
        self.root=root
        self.root.title("Face Recognition Software")
        self.root.geometry("1350x700+0+0")

        title = Label(self.root,text="Face Recognition Software", font = ("Times new Roman",40,"bold"),bg="yellow",fg="red",bd=10, relief=GROOVE)
        title.place(x=0,y=0,relwidth=1)

        Gui = Frame(self.root,width=800, height=900,bg= "white")
        #Login_Frame.grid(row=1,column=1)
        Gui.pack(fill=BOTH)
        Gui.place(x=100,y=100)

        lbl_length = Label(Gui, text="Length of the video is: "+video_time, font=("Times new Roman", 20, "bold"),
                         bg="white").grid(row=1,column=1)

        #lbl_mostcommon = Label(Gui, text="Most common faces are: "+listToStr, compound=LEFT, font=("Times new Roman", 20, "bold"),
                         #bg="white").grid(row=3,column=2)

        lbl_mostfrequent = Label(Gui, text="Most frequently occuring face is : " + most_frequent(names),font=("Times new Roman", 20, "bold"),bg="white").grid(row=2,column=1)
        lbl_initial_final = Label(Gui, text="The first and last appearance of person in format (name : seconds) is given below: \n",font=("Times new Roman", 20, "bold"),bg="white").grid(row=3,column=1)
        i=5
        for key, value in dictinitial.items():
            lbl_1 = Label(Gui, text="First appearnce column: \n", font=("Times new Roman", 20, "bold"), bg="white").grid(row=4,column=1)
            lbl_initial = Label(Gui, text=(key, ':', value), font=("Times new Roman", 20), bg="white").grid(row=i,column=1)
            i=i+1
            print("\n")
        i=5
        for key, value in dictfinal.items():
            lbl_1 = Label(Gui, text="Last appearnce column: \n", font=("Times new Roman", 20, "bold"), bg="white").grid(row=4,column=3)
            lbl_final = Label(Gui, text=(key, ':', value), font=("Times new Roman", 20),bg="white").grid(row=i, column=3)
            i=i+1
            print("\n")
        #print("Initial name and time: ", dictinitial)
        #print("Final name and time: ", dictfinal)


root=Tk()
obj = gui(root)
root.mainloop()
cv2.destroyAllWindows()

#to increase confidence score use more number of images of that person

