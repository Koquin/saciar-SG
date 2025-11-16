import os
import customtkinter as ctk
from ui.splash_screen import SplashScreen
from ui.main_system import MainSystem
from ui.login_form import LoginForm
from utils.setup_utils import setup_window

if os.name == 'nt':
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(2)
    except Exception:
        pass

def start_main_system(app_root):
    app_root.state('normal')
    main_content = MainSystem(master=app_root, app_root=app_root)
    main_content.pack(fill="both", expand=True)
    app_root.title("SACIAR - Sistema de Gerenciamento")


def main():
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    root = ctk.CTk()
    root.title("Inicializando...")
    root.geometry("600x400")
    root.eval('tk::PlaceWindow . center')
    setup_window(root)
    
    def on_splash_finish():
        root.destroy()
        app = ctk.CTk()
        setup_window(app)
        LoginForm(app, lambda: start_main_system(app))
        app.mainloop()

    SplashScreen(root, on_splash_finish)
    root.mainloop()

if __name__ == "__main__":
    main()