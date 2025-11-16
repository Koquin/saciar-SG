# main_system.py
import customtkinter as ctk
from .client_view import ClientView
from .purchase_view import PurchaseView

class MainSystem(ctk.CTkFrame):
    def __init__(self, master, app_root):
        super().__init__(master)
        self.app_root = app_root
        self._frame = None
        self.current_view_name = None
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.create_navigation_sidebar()
        self.main_view_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.main_view_frame.grid(row=0, column=1, sticky="nsew")
        self.main_view_frame.grid_rowconfigure(0, weight=1)
        self.main_view_frame.grid_columnconfigure(0, weight=1)
        self.show_view("clientes")

    def create_navigation_sidebar(self):
        self.sidebar_frame = ctk.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_columnconfigure(0, weight=1)
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        ctk.CTkLabel(self.sidebar_frame, text="SACIAR", font=ctk.CTkFont(size=20, weight="bold")).grid(
            row=0, column=0, padx=20, pady=20)
        ctk.CTkButton(self.sidebar_frame, text="Clientes", command=lambda: self.show_view("clientes")).grid(
            row=1, column=0, padx=20, pady=10)
        ctk.CTkButton(self.sidebar_frame, text="Compras", command=lambda: self.show_view("compras")).grid(
            row=2, column=0, padx=20, pady=10)
        ctk.CTkButton(self.sidebar_frame, text="Sair", fg_color="red", command=self.app_root.destroy).grid(
            row=5, column=0, padx=20, pady=10)


    def show_view(self, view_name):
        if self._frame is not None:
            self._frame.destroy()
            self._frame = None
        self.current_view_name = view_name
        if view_name == "clientes":
            self.app_root.title("SACIAR - Gerenciamento de Clientes")
            self._frame = ClientView(self.main_view_frame, self.app_root)
        elif view_name == "compras":
            self.app_root.title("SACIAR - Histórico de Compras")
            self._frame = PurchaseView(self.main_view_frame, self.app_root)
        if self._frame:
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