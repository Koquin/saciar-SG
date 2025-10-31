# app.py 
import customtkinter as ctk
from ui.splash_screen import SplashScreen 
from ui.main_system import MainSystem 
from ui.login_form import LoginForm 
from utils.setup_utils import setup_window 


def start_main_system(app_root):
    """
    Função chamada após o login ser bem-sucedido.
    Configura e exibe o sistema principal.
    """
    
    # Garante que a janela principal está normalizada (não minimizada)
    app_root.state('normal') 
    
    # 1. Cria a instância do MainSystem DENTRO da janela 'app_root'
    # Passa 'app_root' como master (pai) e 'app_root' como app_root
    main_content = MainSystem(master=app_root, app_root=app_root)
    
    # Adiciona o MainSystem à janela 'app_root' e a faz preencher todo o espaço
    # Se já houver conteúdo (como o Login), o novo conteúdo o substituirá.
    main_content.pack(fill="both", expand=True)
    
    # Ajusta o título após o carregamento da view inicial
    app_root.title("SACIAR - Sistema de Gerenciamento")


def main():
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.title("Inicializando...")
    
    # Prepara a janela para a SplashScreen
    root.geometry("600x400")
    root.eval('tk::PlaceWindow . center')
    root.attributes("-fullscreen", True)
    
    # ------------------------------------------------------------------
    # Lógica de Login integrada
    # ------------------------------------------------------------------
    def on_splash_finish():
        root.destroy() # Fecha a janela da splash
        
        # Cria a janela principal do aplicativo (ctk.CTk)
        app = ctk.CTk()
        setup_window(app) # Aplica a configuração de maximização
        
        # Não usamos app.withdraw() para evitar problemas de modal.
        # A janela principal é criada, mas está vazia.

        # Inicia o formulário de Login, passando a função de callback
        LoginForm(app, lambda: start_main_system(app))
        
        app.mainloop()
    # ------------------------------------------------------------------

    # Inicia a SplashScreen
    SplashScreen(root, on_splash_finish)
    
    # Inicia o loop da janela da splash
    root.mainloop()

if __name__ == "__main__":
    main()