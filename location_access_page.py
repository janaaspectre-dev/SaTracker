from tkinter import *
from tkinter import messagebox
import tkinter as tk
from PIL import Image, ImageTk
import subprocess
import sys    

page = tk.Tk()
page.geometry("500x300")
page.title("Location Access")
page.resizable(False, False)

def open_dashboard():
    page.destroy()
    subprocess.Popen([sys.executable, "dashboard.py"])


bg_image = Image.open("vivid-purple-and-orange-nebula-forming-swirling-cosmic-clouds-in-a-colorful-dramatic-galaxy-scene-photo.jpg")
bg_image = bg_image.resize((700, 500))
bg_photo = ImageTk.PhotoImage(bg_image)

canvas = Canvas(page, width=700, height=500, highlightthickness=0)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=bg_photo, anchor="nw")


canvas.create_text(250, 60,  text="Enter Your City", font=("Arial", 16, "bold"),fill="white"  )


city_entry = Entry(page, width=30)
canvas.create_window(250, 110, window=city_entry)

def continue_to_dashboard():
    city = city_entry.get()

    if city == "":
        messagebox.showerror(
            "Error",
            "Please enter your city"
        )
        return

    messagebox.showinfo(
        "Success",
        f"Location saved: {city}"
    )
    open_dashboard()



continue_btn = Button(page,text="Continue",command=continue_to_dashboard)
canvas.create_window(250, 170, window=continue_btn)
page.mainloop()
