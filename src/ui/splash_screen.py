import customtkinter as ctk
from PIL import Image
import time


class SplashScreen:
    def __init__(self, master, on_finish):
        self.master = master
        self.on_finish = on_finish
        self.frame = ctk.CTkFrame(master, fg_color="#f2ebe5")
        self.frame.pack(fill="both", expand=True)

        image = Image.open("assets/logoSaciar.jpeg")
        ctk_image = ctk.CTkImage(light_image=image, dark_image=image, size=(400, 300))

        label = ctk.CTkLabel(self.frame, image=ctk_image, text="")
        label.image = ctk_image
        label.place(relx=0.5, rely=0.5, anchor="center")

        self.master.after(100, self.fade_in)

    def fade_in(self):
        for i in range(0, 20):
            self.master.attributes("-alpha", i / 20)
            self.master.update()
            time.sleep(0.05)
        time.sleep(1.5)
        self.fade_out()

    def fade_out(self):
        for i in range(20, -1, -1):
            self.master.attributes("-alpha", i / 20)
            self.master.update()
            time.sleep(0.05)

        self.frame.destroy()
        self.master.attributes("-alpha", 1.0)
        self.on_finish()
