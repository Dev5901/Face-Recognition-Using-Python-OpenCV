from tkinter import *
from tkinter import messagebox
import os
import time

class gui:

    def __init__(self,root):
        self.root=root
        self.root.title("Face Recognition Software")
        self.root.geometry("1350x700+0+0")

        title = Label(self.root,text="Face Recognition Software", font = ("Times new Roman",40,"bold"),bg="yellow",fg="red",bd=10, relief=GROOVE)
        title.place(x=0,y=0,relwidth=1)

        Gui = Frame(self.root,width=800, height=900,bg= "white")
        #Login_Frame.grid(row=1,column=1)
        Gui.place(x=400,y=300)

        btn1=Button(Gui,text="Recognize Face through Webcam",width=50,command=self.__web__, font= ("times new roman",14,"bold"),bg="yellow", fg="red").grid(row=4,column=3, pady=5)


        #btn2 = Button(Gui, text="Upload Video for Recognization",command=self.filedDialog1, width=50, font=("times new roman", 14, "bold"),bg="yellow", fg="red").grid(row=4, column=1, pady=5)

        btn3=Button(Gui,text="Train Faces",command=self.__tr__,width=50,font= ("times new roman",14,"bold"),bg="yellow", fg="red").grid(row=2,column=3, pady=5)

        btn4=Button(Gui,text="Recognize Face from video",command=self.__rcg__,width=50,font= ("times new roman",14,"bold"),bg="yellow", fg="red").grid(row=6,column=3, pady=5)

    def __tr__(self):
        filename1='training.py'
        os.system(filename1)
        time.sleep(8)
        messagebox.showinfo("Success", "All faces are trained!")

    def __rcg__(self):
        filename2='recognize.py'
        os.system(filename2)

    def __web__(self):
        filename3='RecognizeThroughWebcam.py'
        os.system(filename3)
        #filename3 = filedialog.askopenfilename(initialdir="/", title="Select a Image",filetype=(("jpg", "*.jpeg"), ("All Files", "*.*")))

root=Tk()
obj = gui(root)
root.mainloop()