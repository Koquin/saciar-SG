import customtkinter as ctk
from tkinter import messagebox
from controllers.auth_controller import authenticate_user

class LoginForm(ctk.CTkToplevel):
    def __init__(self, master, login_success_callback):
        super().__init__(master)
        self.master = master
        self.login_success_callback = login_success_callback

        self.after(100, self.grab_set) 
        self.after(100, self.focus_force)

        self.title("Login de Acesso")
        self.geometry("350x250")
        self.resizable(False, False)
        
        # Centraliza o conteúdo
        self.grid_columnconfigure(0, weight=1)

        # Configura o pop-up como modal e bloqueia a janela principal
        self.transient(master)
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self.on_closing) # Intercepta o botão de fechar

        # Campo Usuário
        ctk.CTkLabel(self, text="Usuário:").grid(row=1, column=0, pady=(10, 0), sticky="w", padx=50)
        self.entry_username = ctk.CTkEntry(self, width=250)
        self.entry_username.grid(row=2, column=0, pady=(0, 10))

        # Campo Senha
        ctk.CTkLabel(self, text="Senha:").grid(row=3, column=0, pady=(10, 0), sticky="w", padx=50)
        self.entry_password = ctk.CTkEntry(self, width=250, show="*")
        self.entry_password.grid(row=4, column=0, pady=(0, 20))
        self.entry_password.bind('<Return>', lambda event: self.perform_login())

        # Botão Login
        ctk.CTkButton(self, text="Entrar", command=self.perform_login, fg_color="#E67E22").grid(row=5, column=0, pady=10)

        self.entry_username.focus_set() # Foca no campo de usuário ao abrir
        
    def perform_login(self):
        username = self.entry_username.get().strip()
        password = self.entry_password.get().strip()
        
        if not username or not password:
            messagebox.showwarning("Atenção", "Preencha o usuário e a senha.")
            return

        # 1. Chama a função de autenticação do backend
        if authenticate_user(username, password):
            messagebox.showinfo("Sucesso", "Login efetuado!")
            self.destroy()
            self.login_success_callback()
        else:
            messagebox.showerror("Erro", "Usuário ou senha inválidos.")
            self.entry_password.delete(0, 'end')

    def on_closing(self):
        """Função para forçar o fechamento do aplicativo se o login for fechado."""
        if messagebox.askokcancel("Sair", "Deseja fechar o sistema?"):
            self.master.destroy()