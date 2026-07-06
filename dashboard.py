from tkinter import *
import tkinter as tk
from tkinter import messagebox
from PIL import Image,ImageTk
import mysql.connector
from satellites import satellites
from skyfield.api import load
from skyfield.api import EarthSatellite
import requests


ts = load.timescale()
def get_live_satellite(norad_id):

    url = (
        f"https://celestrak.org/NORAD/elements/"
        f"gp.php?CATNR={norad_id}&FORMAT=tle"
    )

    response = requests.get(url)

    lines = response.text.strip().splitlines()

    print("Loaded:", lines[0])

    satellite = EarthSatellite(
        lines[1],
        lines[2],
        lines[0],
        ts
    )

    return satellite



def get_satellite_position(satellite_object):

    t = ts.now()

    geocentric = satellite_object.at(t)

    subpoint = geocentric.subpoint()

    return (
        subpoint.latitude.degrees,
        subpoint.longitude.degrees,
        subpoint.elevation.km
    )

satellites_live = load.tle_file(
    "https://celestrak.org/NORAD/elements/gp.php?GROUP=stations&FORMAT=tle"
)
hubble_live = load.tle_file(
    "https://celestrak.org/NORAD/elements/gp.php?CATNR=20580&FORMAT=tle"
)

def find_satellite(name):

    for sat in satellites_live:

        if sat.name.upper() == name.upper():
            return sat

    return None



# ---------------- WINDOW ----------------

page = tk.Tk()




def search_satellite():

    ...

    
page.geometry("1280x720")
page.title("SaTracker Dashboard")
page.config(bg="#16161E")


#Create Selected Satellite Label
selected_satellite_label = Label(page,text="Selected Satellite : ---",bg="#24283B",fg="white",font=("Rajdhani", 12, "bold"))
selected_satellite_label.place(x=350,y=640)
satellite_image_btn = Button(page,text="View Image",bg="#24283B",fg="white")
satellite_image_btn.place(x=600,y=638)
# ---------------- SEARCH FUNCTION/SETTINGS ----------------


def latlon_to_xy(latitude, longitude):
    map_width = 850
    map_height = 450
    x = (longitude + 180) * (map_width / 360)
    y = (90 - latitude) * (map_height / 180)
    return x, y


def search_satellite():
    

    satellite_name = search_entry.get().strip().upper()

    if satellite_name == "":
        messagebox.showerror(
            "Error",
            "Enter a satellite name"
        )
        return
    if satellite_name in satellites:
        sat = satellites[satellite_name]
        name.config(text = f"Name : {satellite_name}")
        norad_label.config(text=f"NORAD ID : {sat['norad']}")
        country_label.config(text=f"Country : {sat['country']}")
        launch_label.config(text=f"Launch Date : {sat['launch']}")
        status_label.config(text=f"Status : {sat['status']}")
        latitude_label.config(text=f"Latitude : {sat['latitude']}")
        longitude_label.config(text=f"Longitude : {sat['longitude']}")
        altitude_label.config(text=f"Altitude : {sat['altitude']}")
        velocity_label.config(text=f"Velocity : {sat['velocity']}")
        selected_satellite_label.config(text=f"Selected Satellite : {satellite_name}")
        norad_id = sat["norad"]
        print("NORAD:", norad_id)

        live_sat = get_live_satellite(norad_id)

        if live_sat:

            lat, lon, alt = get_satellite_position(
                live_sat
            )
            print("Satellite:", satellite_name)
            print("Latitude:", lat)
            print("Longitude:", lon)
            print("Altitude:", alt)

            latitude_label.config(
                text=f"Latitude : {lat:.2f}°"
            )

            longitude_label.config(
                text=f"Longitude : {lon:.2f}°"
            )

            altitude_label.config(
                text=f"Altitude : {alt:.2f} km"
            )
            x, y = latlon_to_xy(lat,lon)

            map_canvas.coords(satellite_marker,x - 6,y - 6,x + 6,y + 6)
            map_canvas.coords(satellite_text,x + 12,y)
            map_canvas.itemconfig(satellite_text,text=satellite_name)
        
    
        
       
    else:
        messagebox.showinfo(
            "Search Result",
            f"Searching for {satellite_name}"
        )

def show_credentials():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="12345",
            database="satracker"
        )

        cursor = conn.cursor()
        query = """
        SELECT email,
               contact_number,
               gender
        FROM users
        WHERE email = %s
        """
        cursor.execute(
            query,
            (logged_in_email,)
        )

        result = cursor.fetchone()

        if result:
            email, phone, gender = result
            messagebox.showinfo(
                "Credentials",
                f"Email: {email}\n\n"
                f"Phone Number: {phone}\n\n"
                f"Gender: {gender}"
            )

        else:

            messagebox.showerror(
                "Error",
                "User not found"
            )

        cursor.close()
        conn.close()

    except Exception as e:

        messagebox.showerror(
            "Database Error",
            str(e)
        )


def show_location():

    messagebox.showinfo(
        "Location",
        "Location feature coming soon"
    )


def logout():

    confirm = messagebox.askyesno(
        "Logout",
        "Are you sure you want to logout?"
    )

    if confirm:
        page.destroy()

def flat_map():
    messagebox.showinfo(
        "Map Type",
        "Flat Map selected"
    )

def satellite_view():
    messagebox.showinfo(
        "Map Type",
        "Satellite View Selected"
    )
def dark_map():
    messagebox.showinfo(
        "Map Type",
        "Dark Mode Map Selected"
    )
        
def show_satellite_image():

    satellite_name = selected_satellite_label.cget("text")
    satellite_name = satellite_name.replace(
        "Selected Satellite : ",
        ""
    )

    try:

        filename = satellite_name.lower()
        filename = filename.replace(" ", "_")
        popup = Toplevel(page)
        popup.title(satellite_name)
        image = Image.open(f"images/{filename}.jpg")
        image = image.resize((500,300))
        photo = ImageTk.PhotoImage(image)
        label = Label(popup,image=photo)
        label.image = photo
        label.pack()

    except:

        messagebox.showerror(
            "Error",
            "Image not found"
        )
    

# ---------------- HEADER ----------------

header = Frame(page,bg="#16161E",height=70)
header.pack(fill="x")

# Search Label

search_label = Label(header,text="🔍 Search Satellite",bg="#16161E",fg="#A9B1D6",font=("Rajdhani", 12, "bold"))
search_label.place(x=350, y=22)

# Search Entry

search_entry = Entry(header,width=25,bg="#24283B",fg="white",insertbackground="white",font=("Rajdhani", 12))
search_entry.place(x=500, y=22)

# Search Button

search_btn = Button(header,text="Search",command=search_satellite,bg="#7AA2F7",fg="white",font=("Rajdhani", 10, "bold"))
search_btn.place(x=720, y=20)

# Cursor automatically inside search box

search_entry.focus_set()



#dropdown menu as:
settings_btn = Menubutton(page,text="Settings ▼",bg="#24283B",fg="#A9B1D6",font=("Rajdhani", 12, "bold"))
settings_menu = Menu(settings_btn,tearoff=0)
settings_menu.add_command(label="Credentials",command=show_credentials)
settings_menu.add_command(label="Location",command=show_location)
settings_menu.add_separator()
settings_menu.add_command(label="Logout",command=logout)
settings_btn.config(menu=settings_menu)
settings_btn.place(x=40,y=22)




#Map Type Dropdown
maptype_btn = Menubutton(page,text = "Map Type ▼",bg="#24283B",fg="#A9B1D6",font=("Rajdhani", 12, "bold"),relief="raised")
maptype_menu = Menu(maptype_btn,tearoff=0)
maptype_menu.add_command(label = "Flat Map",command = flat_map)
maptype_menu.add_command(label = "Satellite View", command = satellite_view)
maptype_menu.add_command(label = "Dark Mode Map", command = dark_map)
maptype_btn.config(menu = maptype_menu)
maptype_btn.place(x = 200, y = 22)



#SATELLITE INFORMATION PANEL
info = Frame(page,bg="#24283B",bd=2,relief="ridge")
info.place(x = 20,y = 100,width = 300,height = 250)
Label(info,text = "SATELLITE INFORMATION",bg="#24283B",fg="#7AA2F7",font=("Rajdhani", 14, "bold")).pack(pady=10)


name = Label(info,text = "Name : ---",bg="#24283B",fg="white",font=("Rajdhani", 12))
name.pack(anchor = "w",padx=15, pady=5)
norad_label = Label(info,text="NORAD ID : ---",bg="#24283B",fg="white",font=("Rajdhani", 12))
norad_label.pack(anchor="w", padx=15, pady=5)
country_label = Label(info,text="Country : ---",bg="#24283B",fg="white",font=("Rajdhani", 12))
country_label.pack(anchor="w", padx=15, pady=5)
launch_label = Label(info,text="Launch Date : ---",bg="#24283B",fg="white",font=("Rajdhani", 12))
launch_label.pack(anchor="w", padx=15, pady=5)
status_label = Label(info,text="Status : ---",bg="#24283B",fg="white",font=("Rajdhani", 12))
status_label.pack(anchor="w", padx=15, pady=5)

#Live Telemetry Panel
telemetry_frame = Frame(page,bg="#24283B",bd=2,relief="ridge")
telemetry_frame.place(x=20,y=370,width=300,height=250)
Label(telemetry_frame,text="LIVE TELEMETRY",bg="#24283B",fg="#7AA2F7",font=("Rajdhani", 14, "bold")).pack(pady=10)


latitude_label = Label(telemetry_frame,text="Latitude : ---",bg="#24283B",fg="white",font=("Rajdhani", 12))
latitude_label.pack(anchor="w", padx=15, pady=5)
longitude_label = Label(telemetry_frame,text="Longitude : ---",bg="#24283B",fg="white",font=("Rajdhani", 12))
longitude_label.pack(anchor="w", padx=15, pady=5)
altitude_label = Label(telemetry_frame,text="Altitude : --- km",bg="#24283B",fg="white",font=("Rajdhani", 12))
altitude_label.pack(anchor="w", padx=15, pady=5)
velocity_label = Label(telemetry_frame,text="Velocity : --- km/s",bg="#24283B",fg="white",font=("Rajdhani", 12))
velocity_label.pack(anchor="w", padx=15, pady=5)
visibility_label = Label(telemetry_frame,text="Visibility : ---",bg="#24283B",fg="white",font=("Rajdhani", 12))
visibility_label.pack(anchor="w", padx=15, pady=5)




#MAIN MAP AREA
map_frame = Frame(page,bg="#24283B",bd=2,relief="ridge")
map_frame.place(x=350,y=100,width=900,height=520)
Label(map_frame,text="LIVE SATELLITE MAP",bg="#24283B",fg="#7AA2F7",font=("Rajdhani", 16, "bold")).pack(pady=1)
map_canvas = Canvas(map_frame,width=850,height=450,bg="#1A1B26",highlightthickness=0)
map_canvas.pack(pady=10)

world_map = Image.open("world_map.jpg")
print("Image loaded successfully")
world_map = world_map.resize((850,450))
world_photo = ImageTk.PhotoImage(world_map)
map_canvas.create_image(0,0,image=world_photo,anchor="nw")
satellite_marker = map_canvas.create_oval(0, 0, 0, 0,fill="red",outline="white",width=2)
satellite_text = map_canvas.create_text(0,0,text="",fill="yellow",font=("Rajdhani", 10, "bold"),anchor="w")

satellite_image_btn.config(command=show_satellite_image)

page.mainloop()
