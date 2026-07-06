from tkinter import *
from PIL import Image, ImageTk
import subprocess
import sys
from tkinter import messagebox
import os

def open_signup():
    page.destroy()
    subprocess.run([sys.executable, "signup_page.py"])
    

    
page = Tk()
page.geometry("700x600")
page.title("SaTracker")
page.resizable(False, False)


bg_image = Image.open(r"C:/Users/JANAA SIVAKUMAR/OneDrive/Desktop/PYTHON main project - JANAA SIVAKUMAR/images (2).jpg")
bg_image = bg_image.resize((700, 600))
bg_photo = ImageTk.PhotoImage(bg_image)
canvas = Canvas(page, width=700, height=600, highlightthickness=0)
canvas.pack(fill="both", expand=True)


# Background
canvas.create_image(0, 0, image=bg_photo, anchor="nw")
canvas.create_text(353, 253,text="SaTracker",fill="#202020",font=("Exo 2", 38, "bold"))
canvas.create_text(350, 250,text="SaTracker",fill="white",font=("Exo 2", 38, "bold"))
canvas.create_line(220, 315,480, 315,fill="#00BFFF",width=2)
canvas.create_text(350, 360,text="Real-Time Satellite Monitoring System",fill="white",font=("Rajdhani", 16, "bold"))


signup_btn = Button(page,text="SIGN UP",font=("Rajdhani", 14, "bold"),bg="#0078D7",fg="white",activebackground="#0094FF",activeforeground="white",padx=20,pady=5,command=open_signup)
canvas.create_window(350,450,window=signup_btn)
page.mainloop()


    
