from tkinter import *
import tkinter as tk
import mysql.connector
from tkinter import messagebox
from PIL import Image, ImageTk
import subprocess
import sys

# ---------------- WINDOW ----------------

page = tk.Tk()
page.geometry("700x500")
page.title("SaTracker - Login")
page.resizable(False, False)

# ---------------- BACKGROUND IMAGE ----------------

bg_image = Image.open("istockphoto-2209587191-612x612.jpg")
bg_image = bg_image.resize((700, 500))
bg_photo = ImageTk.PhotoImage(bg_image)

# ---------------- CANVAS ----------------

canvas = Canvas(page, width=700, height=500, highlightthickness=0)
canvas.pack(fill="both", expand=True)

canvas.create_image(0, 0, image=bg_photo, anchor="nw")

# ---------------- TITLE ----------------

canvas.create_text(350,60,text="LOGIN TO CONTINUE",fill="white",font=("Exo 2", 24, "bold"))
canvas.create_text(350,100,text="Access Real-Time Satellite Monitoring",fill="white",font=("Rajdhani", 18, "bold"))

# ---------------- LABELS ----------------

canvas.create_text(220,180,text="Email",fill="white",font=("Rajdhani", 14, "bold"))
canvas.create_text(220,240,text="Password",fill="white",font=("Rajdhani", 14, "bold"))

# ---------------- ENTRY BOXES ----------------

email_entry = Entry(page, width=30)
password_entry = Entry(page, width=30, show="*")
canvas.create_window(420,180,window=email_entry)
canvas.create_window(420,240,window=password_entry)

# ---------------- LOGIN FUNCTION ----------------

def login():

    email = email_entry.get()
    password = password_entry.get()

    if email == "" or password == "":
        messagebox.showerror(
            "Error",
            "Please fill all fields"
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
        SELECT *
        FROM users
        WHERE email = %s
        AND password = %s
        """

        values = (email, password)

        cursor.execute(query, values)

        result = cursor.fetchone()

        if result:

            messagebox.showinfo(
                "Success",
                "Login Successful"
            )
            page.destroy()
            subprocess.Popen([
                sys.executable,
                "location_access_page.py"
            ])

            

        else:

            messagebox.showerror(
                "Login Failed",
                "Email or Password is Incorrect"
            )

        cursor.close()
        conn.close()

    except Exception as e:

        messagebox.showerror(
            "Database Error",
            str(e)
        )



login_btn = Button(page,text="LOGIN",font=("Rajdhani", 12, "bold"),bg="#0078D7",fg="white",activebackground="#0094FF",activeforeground="white",width=15,command=login)
canvas.create_window(350,330,window=login_btn)



page.mainloop()
