import customtkinter
from PIL import ImageTk
from tkinter import filedialog
from base64 import b64decode
from re import search, DOTALL, sub, MULTILINE
customtkinter.set_appearance_mode("system")
customtkinter.set_default_color_theme("blue")

root = customtkinter.CTk()
root.minsize(1024, 768)
root.title('Thumb_Cutter GUI')
thumbnail_data = b''
filename = ""
label_filename = None


def select_gcode():
    filetypes = (
        ('gcode files', '*.gcode'),
        ('All File', '*.*')
    )
    global filename
    filename = filedialog.askopenfilename(
        title='Select .gcode File to Cut',
        initialdir='~/',
        filetypes=filetypes)


def find_png():
    with open(filename, 'r') as f:
        data = f.read()

    pattern = r'; thumbnail begin \d{3,}x{3,} \d{3,}(.+); thumbnail end'
    match = search(pattern, data, DOTALL)

    if match:
        # logging.info('Thumbnail data found and copied, now to strip and decode using base64')
        global thumbnail_data
        thumbnail_data = match.group(1).strip()
        thumbnail_data = sub(r'^; ', '', thumbnail_data, flags=MULTILINE)
        thumbnail_data = b64decode(thumbnail_data)
    else:
        thumbnail_data = b''
    img = ImageTk.PhotoImage(data=thumbnail_data, format="png")
    frame.image = img
    canvas.create_image(0, 0, image=img, anchor="nw")
    global button2
    button2 = customtkinter.CTkButton(master=frame, text="Save .png", command=save_png)
    global label_filename
    if label_filename is None or not label_filename.winfo_exists():
        label_filename = customtkinter.CTkLabel(master=frame, text=f'Thumbnail cut from {filename}')
        label_filename.pack(before=canvas, side=customtkinter.BOTTOM, pady=12, padx=10)
        button2 = customtkinter.CTkButton(master=frame, text="Save .png", command=save_png)
        button2.pack(before=canvas, side=customtkinter.BOTTOM, anchor='center', expand=True)
    else:
        label_filename.destroy()
        button2.destroy()
        label_filename = customtkinter.CTkLabel(master=frame, text=f'Thumbnail cut from {filename}')
        label_filename.pack(before=canvas, side=customtkinter.BOTTOM, pady=12, padx=10)
        button2 = customtkinter.CTkButton(master=frame, text="Save .png", command=save_png)
        button2.pack(before=canvas, side=customtkinter.BOTTOM, anchor='center', expand=True)


def save_png():
    png = filedialog.asksaveasfilename(defaultextension='.png')
    with open(png, 'wb') as f:
        f.write(thumbnail_data)
    label_filename.destroy()
    button2.destroy()
    label_output = customtkinter.CTkLabel(master=frame, text=f'.png saved as {png}')
    label_output.pack(before=canvas, side=customtkinter.BOTTOM, pady=12, padx=10)


frame = customtkinter.CTkFrame(master=root)
frame.pack(pady=20, padx=60, fill="both", expand=True)

label = customtkinter.CTkLabel(master=frame, text="Thumb_Cutter GUI")
label.pack(pady=12, padx=10)

button0 = customtkinter.CTkButton(master=frame, text="Select .gcode file", command=select_gcode)
button0.pack(side=customtkinter.LEFT, anchor='e', expand=True, padx=2)
button1 = customtkinter.CTkButton(master=frame, text="Cut Thumbnail", command=find_png)
button1.pack(side=customtkinter.RIGHT, anchor='w', expand=True, padx=2)

canvas = customtkinter.CTkCanvas(master=frame, height=500, width=500)
canvas.pack(before=button0, side=customtkinter.BOTTOM, pady=12, padx=10, expand=True, anchor='center')

root.mainloop()
