from tkinter import *
import tkinter as tk
import mysql.connector
from tkinter import messagebox
from PIL import Image, ImageTk
import subprocess
import sys
import os

login_path = os.path.join(
    os.path.dirname(__file__),
    "login_page.py"
)

# ---------------- WINDOW ----------------

page = tk.Tk()
page.geometry("700x600")
page.title("SaTracker - Sign Up")
page.resizable(False, False)

# ---------------- BACKGROUND IMAGE ----------------


bg_image = Image.open("images.jpg")
bg_image = bg_image.resize((700, 600))
bg_photo = ImageTk.PhotoImage(bg_image)

# ---------------- CANVAS ----------------

canvas = Canvas(page, width=700, height=600, highlightthickness=0)
canvas.pack(fill="both", expand=True)

canvas.create_image(0, 0, image=bg_photo, anchor="nw")

# ---------------- LABELS ----------------

canvas.create_text(350,60,text="SIGN UP TO CONTINUE",fill="white",font=("Exo 2", 24, "bold"))
canvas.create_text(180,130,text="Email",fill="white",font=("Rajdhani",14,"bold"))
canvas.create_text(180,180,text="Password",fill="white",font=("Rajdhani",14,"bold"))
canvas.create_text(180,230,text="Repeat Password",fill="white",font=("Rajdhani",14,"bold"))
canvas.create_text(180,280,text="Age",fill="white",font=("Rajdhani",14,"bold"))
canvas.create_text(180,330,text="Contact Number",fill="white",font=("Rajdhani",14,"bold"))
canvas.create_text(180,380,text="Gender",fill="white",font=("Rajdhani",14,"bold"))

# ---------------- ENTRY BOXES ----------------

we = Entry(page, width=25)
xe = Entry(page, width=25, show="*")
ve = Entry(page, width=25, show="*")
ae = Entry(page, width=25)
ce = Entry(page, width=25)

canvas.create_window(420,130,window=we)
canvas.create_window(420,180,window=xe)
canvas.create_window(420,230,window=ve)
canvas.create_window(420,280,window=ae)
canvas.create_window(420,330,window=ce)

# ---------------- GENDER ----------------

gender = StringVar(value="Male")

rb1 = Radiobutton(page,text="Male",variable=gender,value="Male",bg="white")
rb2 = Radiobutton(page,text="Female",variable=gender,value="Female",bg="white")
rb3 = Radiobutton(page,text="Others",variable=gender,value="Others",bg="white")

canvas.create_window(380,380,window=rb1)
canvas.create_window(380,410,window=rb2)
canvas.create_window(380,440,window=rb3)

# ---------------- SIGNUP FUNCTION ----------------

def signup():

    email = we.get()
    password = xe.get()
    repeat_password = ve.get()
    age = ae.get()
    contact = ce.get()
    gender_val = gender.get()

    if email == "" or password == "":
        messagebox.showerror(
            "Error",
            "Please fill all required fields"
        )
        return

    if password != repeat_password:
        messagebox.showerror(
            "Error",
            "Passwords do not match"
        )
        return

    try:

        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="12345",
            database="satracker"
        )

        cursor = conn.cursor()

        query = """
        INSERT INTO users
        (email,password,age,contact_number,gender)
        VALUES (%s,%s,%s,%s,%s)
        """

        values = (
            email,
            password,
            age,
            contact,
            gender_val
        )

        cursor.execute(query, values)
        conn.commit()

        messagebox.showinfo(
            "Success",
            "Account Created Successfully"
        )

        cursor.close()
        conn.close()
        page.destroy()
        subprocess.Popen([sys.executable,"login_page.py"])

    except Exception as e:

        messagebox.showerror(
            "Database Error",
            str(e)
        )

# ---------------- BUTTON ----------------

signup_btn = Button(
    page,
    text="SIGN UP",
    width=15,
    bg="#0078D7",
    fg="white",
    font=("Rajdhani",12,"bold"),
    command=signup
)

canvas.create_window(
    350,
    520,
    window=signup_btn
)

page.mainloop()
