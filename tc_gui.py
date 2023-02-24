from base64 import b64decode
from re import search, DOTALL, sub, MULTILINE
from tkinter import filedialog

import customtkinter
from PIL import ImageTk


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.img = None
        self.thumbnail_data = None
        self.label_filename = None
        self.filename = None
        customtkinter.set_appearance_mode("system")
        customtkinter.set_default_color_theme("blue")

        self.minsize(1024, 768)
        self.title('Thumb_Cutter GUI')

        self.label = customtkinter.CTkLabel(master=self, text="Welcome, select .gcode file to begin.")
        self.label.pack(pady=12, padx=10)
        self.button0 = customtkinter.CTkButton(master=self, text="Select .gcode file", command=self.select_gcode)
        self.button0.pack(side=customtkinter.LEFT, anchor='e', expand=True, padx=2)
        self.button1 = customtkinter.CTkButton(master=self, text="Cut Thumbnail", command=self.cut_thumbnail)
        self.button1.pack(side=customtkinter.RIGHT, anchor='w', expand=True, padx=2)
        self.button2 = customtkinter.CTkButton(master=self, text="Save .png", command=self.save_png)
        self.canvas = customtkinter.CTkCanvas(master=self, height=500, width=500)
        self.canvas.pack(before=self.button0, side=customtkinter.BOTTOM, pady=2, padx=10, expand=True, anchor='center')

    def select_gcode(self):
        filetypes = (
            ('gcode files', '*.gcode'),
            ('All File', '*.*')
        )
        self.filename = filedialog.askopenfilename(
            title='Select .gcode File to Cut',
            initialdir='~/',
            filetypes=filetypes)
        self.label_filename = customtkinter.CTkLabel(master=self, text=f'Thumbnail cut from {self.filename}')

    def find_png(self):
        with open(self.filename, 'r') as f:
            data = f.read()

        pattern = r'; thumbnail begin 500x500 \d{5,}(.+); thumbnail end'
        match = search(pattern, data, DOTALL)

        if match:
            # logging.info('Thumbnail data found and copied, now to strip and decode using base64')
            self.thumbnail_data = match.group(1).strip()
            self.thumbnail_data = sub(r'^; ', '', self.thumbnail_data, flags=MULTILINE)
            self.thumbnail_data = b64decode(self.thumbnail_data)

    def cut_thumbnail(self):
        self.find_png()
        self.img = ImageTk.PhotoImage(data=self.thumbnail_data, format="png")
        self.canvas.create_image(0, 0, image=self.img, anchor="nw")
        self.label.configure(text=f'Thumbnail cut from {self.filename}')
        self.button2.pack(before=self.button0, pady=4, side=customtkinter.BOTTOM, anchor='n', expand=True)

    def save_png(self):
        png = filedialog.asksaveasfilename(defaultextension='.png')
        with open(png, 'wb') as f:
            f.write(self.thumbnail_data)
        self.label.configure(text=f'.png saved as {png}')


if __name__ == "__main__":
    app = App()
    app.mainloop()
