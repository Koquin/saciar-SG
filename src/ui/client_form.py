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
        
        self.cliente_doc_id = None
        
        self.title(f"{mode} Cliente")
        self.geometry("400x350")
        self.resizable(False, False)

        self.after(250, self.set_focus)

        ctk.CTkLabel(self, text="Nome:").pack(pady=5)
        self.entry_nome = ctk.CTkEntry(self, width=300)
        self.entry_nome.pack()

        ctk.CTkLabel(self, text="Telefone:").pack(pady=5)
        self.entry_telefone = ctk.CTkEntry(self, width=300)
        self.entry_telefone.pack()

        ctk.CTkLabel(self, text="Pontos:").pack(pady=5)
        self.entry_pontos = ctk.CTkEntry(self, width=300)
        self.entry_pontos.pack()

        ctk.CTkLabel(self, text="Troco:").pack(pady=5)
        self.entry_troco = ctk.CTkEntry(self, width=300)
        self.entry_troco.pack()

        if client:
            self.entry_nome.insert(0, client.get("nome", ""))
            self.entry_telefone.insert(0, client.get("telefone", ""))
            self.entry_pontos.insert(0, str(client.get("pontos", 0)))
            self.entry_troco.insert(0, str(client.get("troco", 0.0)))
            self.cliente_doc_id = client.get("id") 
        ctk.CTkButton(self, text=mode, command=self.submit).pack(pady=15)
        self.bind('<Return>', self.submit_on_enter)

    def validar_telefone(self, telefone: str) -> bool:
        telefone = telefone.strip()
        padrao = r"^\(?\d{2}\)?\s?\d{4,5}-?\d{4}$"
        return re.match(padrao, telefone) is not None

    def validar_pontos(self, pontos: str) -> bool:
        try:
            p = int(pontos)
            return p >= 0 and p <= 10
        except ValueError:
            return False
            
    def submit_on_enter(self, event):
        self.submit()

    def submit(self):
        nome = self.entry_nome.get().strip()
        telefone = self.entry_telefone.get().strip()
        pontos = self.entry_pontos.get().strip()
        troco = self.entry_troco.get().strip()

        if not nome or not telefone:
            messagebox.showwarning("Campos obrigatórios", "Preencha todos os campos obrigatórios!")
            return

        if not self.validar_telefone(telefone):
            messagebox.showerror("Telefone inválido", "O telefone deve estar no formato (XX) XXXXX-XXXX ou XXXXXXXXXXX.")
            return

        if pontos and not self.validar_pontos(pontos):
            messagebox.showerror("Pontos inválidos", "Os pontos devem ser numéricos, positivos e no maximo ser 10")
            return

        try:
            troco_float = float(troco) if troco else 0.0
        except ValueError:
            messagebox.showerror("Troco inválido", "O troco deve ser um número válido.")
            return

        client_data = {
            "nome": nome,
            "telefone": telefone,
            "pontos": int(pontos) if pontos else 0,
            "troco": troco_float
        }
        
        if self.mode == "Atualizar" and self.cliente_doc_id:
            client_data["id"] = self.cliente_doc_id

        self.callback(client_data)
        self.destroy()

    def set_focus(self):
        self.grab_set()
        self.focus_force()