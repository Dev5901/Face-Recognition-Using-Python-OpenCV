First as we get the image via webcam or video input ( extract frame) then we 
convert the image into grey scale then initially detect the face using deploy.prototxt 
and recognize face using openface_nn4.small2.v1.t7 and 
res10_300x300_ssd_iter_140000.caffemode and place a green rectangle on the 
face detected. Then we extract the features of the face and by using face bunch 
graph technique we compare extracted faces with faces already in database that 
were plotted on the graph. The nearest one in the graph is the one which our face is.
And then print the output result by rectangular green frame and person name.
