# import base64
# import re
import customtkinter
from PIL import ImageTk
from tkinter import filedialog
from base64 import b64decode
from re import search, DOTALL, sub, MULTILINE
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

root = customtkinter.CTk()
root.geometry("1024x768")


def select_image():
    filetypes = (
        ('gcode files', '*.gcode'),
        ('All File', '*.*')
    )
    global filename
    filename = filedialog.askopenfilename(
        title='Select .gcode File to Cut',
        initialdir='/home',
        filetypes=filetypes)


def find_png():
    with open(filename, 'r') as f:
        data = f.read()

    pattern = r'; thumbnail begin 500x500 \d{5,}(.+); thumbnail end'
    match = search(pattern, data, DOTALL)

    if match:
        # logging.info('Thumbnail data found and copied, now to strip and decode using base64')
        global thumbnail_data
        thumbnail_data = match.group(1).strip()
        thumbnail_data = sub(r'^; ', '', thumbnail_data, flags=MULTILINE)
        thumbnail_data = b64decode(thumbnail_data)
    else:
        thumbnail_data = 'test'
    img = ImageTk.PhotoImage(data=thumbnail_data, format="png")
    frame.image = img
    canvas.create_image(0, 0, image=img, anchor="nw")
    label.filename = customtkinter.CTkLabel(master=frame, text=f'Thumbnail cut from {filename}')
    label.filename.pack(pady=12, padx=10)


def save_png():
    png = filedialog.asksaveasfilename(defaultextension='.png')
    with open(png, 'wb') as f:
        f.write(thumbnail_data)


frame = customtkinter.CTkFrame(master=root)
frame.pack(pady=20, padx=60, fill="both", expand=True)

label = customtkinter.CTkLabel(master=frame, text="Thumb_Cutter GUI")
label.pack(pady=12, padx=10)

button0 = customtkinter.CTkButton(master=frame, text="Select .gcode file", command=select_image)
button0.pack(pady=12, padx=10)

canvas = customtkinter.CTkCanvas(master=frame, height=500, width=500)
canvas.pack(pady=12, padx=10)

button1 = customtkinter.CTkButton(master=frame, text="Cut Thumbnail", command=find_png)
button1.pack(padx=5, side=customtkinter.LEFT, anchor='e', expand=True)

button2 = customtkinter.CTkButton(master=frame, text="Save .png", command=save_png)
button2.pack(side=customtkinter.RIGHT, anchor='w', expand=True)

root.mainloop()
