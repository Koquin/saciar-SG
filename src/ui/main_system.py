# main_system.py
import customtkinter as ctk

# Importa as views necessárias (ajuste os caminhos conforme sua estrutura de pastas)
from .client_view import ClientView 
from .purchase_view import PurchaseView

class MainSystem(ctk.CTkFrame):
    """
    Controlador principal que contém a barra de navegação (Sidebar) e 
    gerencia a alternância entre as views (Clientes, Compras, etc.).
    """
    def __init__(self, master, app_root): 
        super().__init__(master)
        
        self.app_root = app_root
        
        self._frame = None
        self.current_view_name = None
        
        # Configuração do grid do MainSystem Frame para expansão
        # Coluna 0: Sidebar (fixa)
        # Coluna 1: Conteúdo Principal (expande)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1) 
        
        # 1. Adicionar o Menu de Navegação (Sidebar)
        self.create_navigation_sidebar()
        
        # 2. Frame principal para as Views (Clientes/Compras)
        self.main_view_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        # main_view_frame fica na coluna 1 e expande
        self.main_view_frame.grid(row=0, column=1, sticky="nsew")
        self.main_view_frame.grid_rowconfigure(0, weight=1)
        self.main_view_frame.grid_columnconfigure(0, weight=1)

        # 3. Exibir a view inicial
        self.show_view("clientes")

    def create_navigation_sidebar(self):
        """Cria a barra de navegação lateral."""
        # Frame lateral (Coluna 0 do MainSystem)
        self.sidebar_frame = ctk.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        
        # Configuração interna da Sidebar para centralização dos botões
        self.sidebar_frame.grid_columnconfigure(0, weight=1)
        self.sidebar_frame.grid_rowconfigure(4, weight=1) # Faz o botão de sair ir para o fundo
        
        # Título
        ctk.CTkLabel(self.sidebar_frame, text="SACIAR", font=ctk.CTkFont(size=20, weight="bold")).grid(
            row=0, column=0, padx=20, pady=20)
        
        # Botões de navegação
        ctk.CTkButton(self.sidebar_frame, text="Clientes", command=lambda: self.show_view("clientes")).grid(
            row=1, column=0, padx=20, pady=10)
            
        ctk.CTkButton(self.sidebar_frame, text="Compras", command=lambda: self.show_view("compras")).grid(
            row=2, column=0, padx=20, pady=10)
        
        # Botão de sair (alinhado ao fundo na row 5)
        ctk.CTkButton(self.sidebar_frame, text="Sair", fg_color="red", command=self.app_root.destroy).grid(
            row=5, column=0, padx=20, pady=10)


    def show_view(self, view_name):
        """Alterna a visualização entre 'clientes' e 'compras'."""
        
        # 1. Destruir a view antiga
        if self._frame is not None:
            self._frame.destroy()
            self._frame = None

        self.current_view_name = view_name
        
        # 2. Instanciar a nova view DENTRO do main_view_frame
        if view_name == "clientes":
            self.app_root.title("SACIAR - Gerenciamento de Clientes") 
            self._frame = ClientView(self.main_view_frame, self.app_root) 
        elif view_name == "compras":
            self.app_root.title("SACIAR - Histórico de Compras") 
            self._frame = PurchaseView(self.main_view_frame, self.app_root) 
        
        # 3. Empacotar a nova view
        if self._frame:
            # O sticky="nsew" garante que a view preencha o main_view_frame
            self._frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)


# O bloco de teste no final foi atualizado para usar a nova classe MainApp,
# garantindo que a estrutura de autenticação (mesmo que bypassada) seja seguida.
if __name__ == "__main__":
    # Teste rápido simulando o MockApp
    class MockApp(ctk.CTk):
        def __init__(self):
            super().__init__()
            self.geometry("1000x600")
            self.title("SACIAR - Teste")
            self.grid_rowconfigure(0, weight=1)
            self.grid_columnconfigure(0, weight=1)
            
            main_content = MainSystem(master=self, app_root=self)
            main_content.grid(row=0, column=0, sticky="nsew")

    app = MockApp()
    app.mainloop()