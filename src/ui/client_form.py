# client_form.py
import customtkinter as ctk
from tkinter import messagebox
import re

class ClientForm(ctk.CTkToplevel):
    def __init__(self, master, callback, client=None, mode="Cadastrar"):
        super().__init__(master)
        self.callback = callback
        self.client = client
        self.mode = mode
        self.title(f"{mode} Cliente")
        self.geometry("400x400")
        self.resizable(False, False)

        self.after(250, self.set_focus)

        # Campos
        ctk.CTkLabel(self, text="Nome:").pack(pady=5)
        self.entry_nome = ctk.CTkEntry(self, width=300)
        self.entry_nome.pack()

        ctk.CTkLabel(self, text="CPF:").pack(pady=5)
        self.entry_cpf = ctk.CTkEntry(self, width=300)
        self.entry_cpf.pack()

        ctk.CTkLabel(self, text="Telefone:").pack(pady=5)
        self.entry_telefone = ctk.CTkEntry(self, width=300)
        self.entry_telefone.pack()

        ctk.CTkLabel(self, text="Pontos:").pack(pady=5)
        self.entry_pontos = ctk.CTkEntry(self, width=300)
        self.entry_pontos.pack()

        # Preenche se for atualização
        if client:
            self.entry_nome.insert(0, client.get("nome", ""))
            self.entry_cpf.insert(0, client.get("cpf", ""))
            self.entry_telefone.insert(0, client.get("telefone", ""))
            self.entry_pontos.insert(0, str(client.get("pontos", 0)))
            
            # Bloquear edição do CPF na atualização
            if mode == "Atualizar":
                 self.entry_cpf.configure(state="disabled")

        ctk.CTkButton(self, text=mode, command=self.submit).pack(pady=15)
        
        # --- NOVO: Ligar a tecla Enter (Return) à função de submissão ---
        self.bind('<Return>', self.submit_on_enter)
        # ---------------------------------------------------------------

    # ---------------- VALIDAÇÕES ----------------
    def validar_cpf(self, cpf: str) -> bool:
        """Valida formato e tamanho do CPF"""
        cpf = re.sub(r"\D", "", cpf)
        return len(cpf) == 11 and cpf.isdigit()

    def validar_telefone(self, telefone: str) -> bool:
        """Valida formato de telefone (ex: (11) 98888-0000 ou 11988880000)"""
        telefone = telefone.strip()
        padrao = r"^\(?\d{2}\)?\s?\d{4,5}-?\d{4}$"
        return re.match(padrao, telefone) is not None

    def validar_pontos(self, pontos: str) -> bool:
        """Permite apenas números inteiros e positivos"""
        try:
            p = int(pontos)
            return p >= 0 and p <= 10
        except ValueError:
            return False
            
    def submit_on_enter(self, event):
        """Função wrapper para chamar submit() quando a tecla Enter for pressionada."""
        # O bind passa o objeto Event como primeiro argumento, que ignoramos na função submit original.
        self.submit()

    # ---------------- SUBMIT ----------------
    def submit(self):
        nome = self.entry_nome.get().strip()
        
        # Pega o CPF do campo, ou do objeto self.client se estiver desabilitado (Atualizar)
        cpf = self.client.get("cpf") if self.mode == "Atualizar" and self.client else self.entry_cpf.get().strip()
        
        telefone = self.entry_telefone.get().strip()
        pontos = self.entry_pontos.get().strip()

        # ---------- Verificações ----------
        if not nome or not cpf or not telefone:
            messagebox.showwarning("Campos obrigatórios", "Preencha todos os campos obrigatórios!")
            return

        if not self.validar_cpf(cpf):
            messagebox.showerror("CPF inválido", "O CPF deve conter 11 números válidos (somente dígitos).")
            return

        if not self.validar_telefone(telefone):
            messagebox.showerror("Telefone inválido", "O telefone deve estar no formato (XX) XXXXX-XXXX ou XXXXXXXXXXX.")
            return

        if pontos and not self.validar_pontos(pontos):
            messagebox.showerror("Pontos inválidos", "Os pontos devem ser numéricos, positivos e no maximo ser 10")
            return

        # ---------- Se tudo estiver certo ----------
        client_data = {
            "nome": nome,
            "cpf": cpf, # CPF que será usado para identificação no CRUD
            "telefone": telefone,
            "pontos": int(pontos) if pontos else 0
        }

        self.callback(client_data)
        self.destroy()

    def set_focus(self):
        """Método chamado via after() para garantir que a janela está visível antes de bloquear."""
        self.grab_set()
        self.focus_force()