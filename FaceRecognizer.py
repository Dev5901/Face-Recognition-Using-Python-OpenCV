from tkinter import *
from tkinter import messagebox
from PIL import  ImageTk
import os
import getpass


class Login_System:
    def __init__(self,root):
        self.root=root
        self.root.title("Login Page")
        #self.root.geometry("600x300")
        self.root.geometry("1350x700+0+0")

        #self.bg_img = ImageTk.PhotoImage(file = "C:/Users/Dev Prajapati/PycharmProjects/pythonProject1/bg_img.jpg")
        #self.user_img = PhotoImage(file = "C:/Users/Dev Prajapati/PycharmProjects/pythonProject1/user_img.png")
        #self.pass_img = PhotoImage(file="C:/Users/Dev Prajapati/PycharmProjects/pythonProject1/lock-img.jpg")
        #self.logo_img = PhotoImage(file="C:/Users/Dev Prajapati/PycharmProjects/pythonProject1/top-user-icon.jpg")

        self.uname=StringVar()
        self.upass=StringVar()

        #, image = self.bg_img
        bg_lbl = Label(self.root).pack()

        title = Label(self.root,text="Login Page", font = ("Times new Roman",40,"bold"),bg="yellow",fg="red",bd=10, relief=GROOVE)
        title.place(x=0,y=0,relwidth=1)

        Login_Frame = Frame(self.root,width=600, height=700,bg= "white")
        #Login_Frame.grid(row=1,column=1)
        Login_Frame.place(x=400,y=300)
        #image = self.logo_img
        logo_lbl = Label(Login_Frame, bd=0).grid(row=0, column=0,columnspan=2, pady=2)
       #, image = self.user_img
        lbl_user = Label(Login_Frame, text= "Username",compound = LEFT, font = ("Times new Roman",20,"bold"), bg="white").grid(row=1,column= 0, padx=10, pady=20)
        txt_user = Entry(Login_Frame,bd=5,textvariable=self.uname,relief = GROOVE, font=("",15)).grid(row=1,column=1, padx=20)
        #image = self.pass_img,
        lbl_pass = Label(Login_Frame, text="Password",  compound=LEFT,font=("Times new Roman", 20, "bold"), bg="white").grid(row=2, column=0, padx=10, pady=20)
        txt_pass = Entry(Login_Frame, bd=5, relief=GROOVE,show="*",textvariable=self.upass, font=("", 15)).grid(row=2, column=1, padx=20)

        btn_login = Button(Login_Frame,text="Login", width=15,command=self.login, font= ("times new roman",14,"bold"),bg="yellow", fg="red").grid(row=3,column=1, pady=10)

    def login(self):
        if self.uname.get()=="" or self.upass.get()=="":
            messagebox.showerror("Error","All fields are required!")
        elif self.uname.get()=="Dev" and self.upass.get()=="12345":
            messagebox.showinfo("Successfull",f"Welcome {self.uname.get()}")
            filename = 'Gui.py'
            os.system(filename)
        else:
            messagebox.showerror("Error", "Invalid username or Password!")

root=Tk()
obj = Login_System(root)
root.mainloop()
