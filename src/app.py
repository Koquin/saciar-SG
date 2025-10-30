# app.py (CORRIGIDO)
import customtkinter as ctk
from ui.splash_screen import SplashScreen # Importa a classe SplashScreen
from ui.main_system import MainSystem # Importa a classe MainSystem
from utils.setup_utils import setup_window # Importa o utilitário de setup


def main():
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.title("Inicializando...")
    
    # Prepara a janela para a SplashScreen (pequena e centralizada)
    root.geometry("600x400")
    root.eval('tk::PlaceWindow . center')
    root.attributes("-fullscreen", True)
    
    # Função que será chamada após a SplashScreen terminar
    def on_splash_finish():
        root.destroy() # Fecha a janela da splash
        
        # Cria a nova janela principal
        app = ctk.CTk()
        # app.title é definido pelo MainSystem.show_view
        setup_window(app) # Aplica a configuração de maximização
        
        # Cria a instância do MainSystem DENTRO da janela 'app'
        # Passa 'app' como master (pai) e 'app' como app_root
        main_content = MainSystem(master=app, app_root=app)
        
        # Adiciona o MainSystem à janela 'app' e a faz preencher todo o espaço
        main_content.pack(fill="both", expand=True)
        
        app.mainloop()

    # Inicia a SplashScreen
    SplashScreen(root, on_splash_finish)
    
    # Inicia o loop da janela da splash
    root.mainloop()

if __name__ == "__main__":
    main()