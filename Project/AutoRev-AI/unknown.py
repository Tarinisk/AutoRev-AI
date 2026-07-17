import socket
import tkinter as tk
from tkinter import ttk

# -------- CHANGE THIS --------
ESP_IP = "192.168.1.42"
PORT = 4210
# -----------------------------

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def send(msg):
    print("Send:", msg)
    sock.sendto(msg.encode(), (ESP_IP, PORT))

# ======================================================
# UI SETUP
# ======================================================
root = tk.Tk()
root.title("🔥 ESP32 Smart Robot Controller 🔥")
root.geometry("520x620")
root.config(bg="#101820")

# Nice looking style
style = ttk.Style(root)
style.theme_use("clam")

style.configure("TButton",
                font=("Segoe UI", 11, "bold"),
                padding=6,
                relief="flat",
                background="#00ADB5",
                foreground="white")

style.map("TButton",
          background=[("active", "#08D9D6")])

title = tk.Label(root, text="ESP32 WiFi Robot Controller",
                 font=("Segoe UI", 18, "bold"),
                 fg="#08D9D6", bg="#101820")
title.pack(pady=10)

# ======================================================
# MODE
# ======================================================
box = tk.LabelFrame(root, text="Mode",
                    font=("Segoe UI", 12, "bold"),
                    fg="#EEEEEE", bg="#101820")
box.pack(pady=8)

mode_frame = tk.Frame(box, bg="#101820")
mode_frame.pack(pady=5)

ttk.Button(mode_frame, text="AUTO",
           width=18,
           command=lambda: send("MODE AUTO")).grid(row=0, column=0, padx=8)

ttk.Button(mode_frame, text="MANUAL",
           width=18,
           command=lambda: send("MODE MANUAL")).grid(row=0, column=1, padx=8)

# ======================================================
# ULTRASONIC
# ======================================================
us = tk.LabelFrame(root, text="Obstacle Detection",
                   font=("Segoe UI", 12, "bold"),
                   fg="#EEEEEE", bg="#101820")
us.pack(pady=8)

u = tk.Frame(us, bg="#101820")
u.pack(pady=5)

ttk.Button(u, text="Enable",
           width=16,
           command=lambda: send("USON")).grid(row=0, column=0, padx=6)

ttk.Button(u, text="Disable",
           width=16,
           command=lambda: send("USOFF")).grid(row=0, column=1, padx=6)

tk.Label(us, text="Stop Distance (cm)",
         font=("Segoe UI", 11),
         fg="white", bg="#101820").pack()

dist_val = tk.StringVar(value="15")
dist_entry = tk.Entry(us, textvariable=dist_val,
                      width=10, justify="center",
                      font=("Segoe UI", 12))
dist_entry.pack(pady=2)

def set_distance():
    try:
        d = float(dist_val.get())
        send("USD" + str(int(d)))
    except:
        print("Invalid distance")

ttk.Button(us, text="Set Distance",
           command=set_distance).pack(pady=3)

# ======================================================
# MOVEMENT
# ======================================================
mv = tk.LabelFrame(root, text="Movement",
                   font=("Segoe UI", 12, "bold"),
                   fg="#EEEEEE", bg="#101820")
mv.pack(pady=10)

d = tk.Frame(mv, bg="#101820")
d.pack()

ttk.Button(d, text="Forward", width=18,
           command=lambda: send("F")).grid(row=0, column=1, pady=6)

ttk.Button(d, text="Left", width=16,
           command=lambda: send("L")).grid(row=1, column=0, pady=6)

ttk.Button(d, text="STOP", width=18,
           command=lambda: send("S")).grid(row=1, column=1, pady=6)

ttk.Button(d, text="Right", width=16,
           command=lambda: send("R")).grid(row=1, column=2, pady=6)

ttk.Button(d, text="Backward", width=18,
           command=lambda: send("B")).grid(row=2, column=1, pady=6)

# ======================================================
# SPEED
# ======================================================
tk.Label(root, text="Speed",
         font=("Segoe UI", 12, "bold"),
         fg="#EEEEEE", bg="#101820").pack()

speed = tk.IntVar(value=180)

def update_speed(val):
    send("V" + str(int(speed.get())))

slider = ttk.Scale(root, from_=0, to=255,
                   orient="horizontal",
                   variable=speed,
                   command=update_speed,
                   length=350)
slider.pack(pady=5)

tk.Label(root, textvariable=speed,
         font=("Segoe UI", 12),
         fg="white", bg="#101820").pack()

# ======================================================
# KEYBOARD CONTROL 😎
# ======================================================
def keypress(event):
    k = event.keysym.lower()
    if k == "w": send("F")
    elif k == "s": send("B")
    elif k == "a": send("L")
    elif k == "d": send("R")
    elif k == "space": send("S")

root.bind("<KeyPress>", keypress)

root.mainloop()
