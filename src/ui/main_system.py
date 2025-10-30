# main_system.py (CORRIGIDO)
import customtkinter as ctk
# Importa as novas views e o utilitário
from .client_view import ClientView
from .purchase_view import PurchaseView
# Note que 'setup_window' não é mais usado aqui, ele vai para o app.py


class MainSystem(ctk.CTkFrame): # <-- MUDANÇA PRINCIPAL: Agora herda de CTkFrame
    def __init__(self, master, app_root): # <-- master é o pai (app_root é a referência da janela principal)
        super().__init__(master)
        
        # Guardamos a referência da janela principal (o ctk.CTk que chamou)
        self.app_root = app_root
        
        # A configuração inicial da janela (title, geometry) fica no app.py
        
        self._frame = None
        self.current_view_name = None
        
        # Configuração da grade do MainSystem Frame para expansão
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Adicionar o Menu de Navegação (Sidebar)
        self.create_navigation_sidebar()
        
        # Exibir a view inicial (pode ser o menu inicial ou a primeira view)
        self.show_view("clientes")

    def create_navigation_sidebar(self):
        """Cria a barra de navegação lateral."""
        # Frame lateral
        self.sidebar_frame = ctk.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1) # Faz o botão de baixo ir para o final
        
        ctk.CTkLabel(self.sidebar_frame, text="SACIAR", font=ctk.CTkFont(size=20, weight="bold")).grid(row=0, column=0, padx=20, pady=20)
        
        # Botões de navegação
        ctk.CTkButton(self.sidebar_frame, text="Clientes", command=lambda: self.show_view("clientes")).grid(row=1, column=0, padx=20, pady=10)
        ctk.CTkButton(self.sidebar_frame, text="Compras", command=lambda: self.show_view("compras")).grid(row=2, column=0, padx=20, pady=10)
        
        # Um botão de exemplo para sair, alinhado ao fundo
        ctk.CTkButton(self.sidebar_frame, text="Sair", fg_color="red", command=self.app_root.destroy).grid(row=5, column=0, padx=20, pady=(10, 20))
        
        # Frame principal para as Views (Clientes/Compras)
        self.main_view_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.main_view_frame.grid(row=0, column=1, rowspan=4, sticky="nsew")
        self.main_view_frame.grid_rowconfigure(0, weight=1)
        self.main_view_frame.grid_columnconfigure(0, weight=1)
        
        # Configurar a expansão da coluna 1 (onde fica o conteúdo)
        self.grid_columnconfigure(1, weight=1)


    def show_view(self, view_name):
        """Alterna a visualização entre 'clientes' e 'compras'."""
        
        # 1. Destruir a view antiga
        if self._frame is not None:
            self._frame.destroy()
            self._frame = None

        self.current_view_name = view_name
        
        # 2. Instanciar a nova view DENTRO do main_view_frame
        if view_name == "clientes":
            self.app_root.title("Sistema de Gerenciamento - Clientes") # Atualiza o título da Janela principal
            self._frame = ClientView(self.main_view_frame, self) # Passa o main_view_frame como master
        elif view_name == "compras":
            self.app_root.title("Sistema de Gerenciamento - Histórico de Compras") # Atualiza o título da Janela principal
            self._frame = PurchaseView(self.main_view_frame, self) # Passa o main_view_frame como master
        
        # 3. Empacotar a nova view
        if self._frame:
            # Usamos grid para que a view preencha o main_view_frame
            self._frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)


def start_app():
    # Esta função não é mais necessária, o app.py fará o controle.
    # Mas se você quiser manter um teste rápido, mantenha assim, 
    # desde que NÃO use o app.py para iniciar.
    pass 

if __name__ == "__main__":
    # Teste rápido se o módulo for executado diretamente
    app = ctk.CTk()
    MainSystem(app, app)
    app.mainloop()