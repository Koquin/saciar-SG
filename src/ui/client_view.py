# client_view.py
import customtkinter as ctk
from tkinter import ttk, messagebox
import pandas as pd
from .client_form import ClientForm
from utils.api_utils import get_clients, post_client, put_client, delete_client

class ClientView(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.client_data = []
        self.selected_client_index = None

        # Tabela
        self.create_client_table()
        
        # Botões de Ação
        self.btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_frame.pack(pady=10)

        ctk.CTkButton(self.btn_frame, text="Cadastrar Cliente", command=self.cadastrar_cliente).pack(side="left", padx=10)
        ctk.CTkButton(self.btn_frame, text="Atualizar Cliente", command=self.atualizar_cliente).pack(side="left", padx=10)
        ctk.CTkButton(self.btn_frame, text="Remover Cliente", command=self.remover_cliente).pack(side="left", padx=10)
        ctk.CTkButton(self.btn_frame, text="Exportar Excel", command=self.export_to_excel).pack(side="left", padx=10)
        
        self.load_clients() # Carrega os dados na inicialização

    def create_client_table(self):
        """Tabela de clientes"""
        # Configuração do estilo da Treeview (necessária para aparecer)
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview.Heading", font=("Helvetica", 14, "bold"))
        style.configure("Treeview", font=("Helvetica", 12))
        style.map('Treeview', background=[('selected', '#2E86DE')])

        self.tree = ttk.Treeview(
            self,
            columns=("nome", "cpf", "telefone", "pontos"),
            show="headings",
            selectmode="browse",
        )
        self.tree.heading("nome", text="NOME")
        self.tree.heading("cpf", text="CPF")
        self.tree.heading("telefone", text="TELEFONE")
        self.tree.heading("pontos", text="PONTOS")

        self.tree.column("nome", width=200, anchor='w')
        self.tree.column("cpf", width=120, anchor='center')
        self.tree.column("telefone", width=120, anchor='center')
        self.tree.column("pontos", width=80, anchor='center')
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        self.tree.bind("<<TreeviewSelect>>", self.on_select)

    def load_clients(self):
        """Carrega clientes do backend usando API"""
        try:
            self.client_data = get_clients()
            self.display_clients(self.client_data)
        except Exception as e:
            messagebox.showerror("Erro de API", f"Falha ao carregar clientes: {e}")

    def display_clients(self, clients):
        """Preenche a tabela com os dados dos clientes"""
        self.tree.delete(*self.tree.get_children())
        for client in clients:
            pontos = client.get("pontos", 0)
            self.tree.insert("", "end", values=(
                client["nome"],
                client["cpf"],
                client["telefone"],
                pontos,
            ))

    def on_select(self, event):
        """Atualiza o índice do cliente selecionado"""
        selected = self.tree.selection()
        if selected:
            item_id = selected[0]
            values = self.tree.item(item_id, 'values')
            if values:
                cpf = values[1] 
                # Encontra o índice na lista de dados
                for i, client in enumerate(self.client_data):
                    if client.get('cpf') == cpf:
                        self.selected_client_index = i
                        return
        self.selected_client_index = None

    def handle_client_callback(self, client_data, mode):
        """Processa o retorno do ClientForm após Salvar/Atualizar"""
        if mode == "Cadastrar":
            result = post_client(client_data)
            if result:
                messagebox.showinfo("Sucesso", "Cliente cadastrado com sucesso!")
            else:
                messagebox.showerror("Erro", "Falha ao cadastrar. O CPF já pode existir ou houve um erro no servidor.")
        elif mode == "Atualizar":
            result = put_client(client_data)
            if result:
                messagebox.showinfo("Sucesso", "Cliente atualizado com sucesso!")
            else:
                messagebox.showerror("Erro", "Falha ao atualizar cliente.")
        
        # Sempre recarrega a tabela após a tentativa de operação
        self.load_clients()
        self.selected_client_index = None # Limpa a seleção

    def cadastrar_cliente(self):
        """Abre o formulário de cadastro"""
        ClientForm(self.controller.app_root,
                   callback=lambda data: self.handle_client_callback(data, "Cadastrar"), 
                   mode="Cadastrar")

    def atualizar_cliente(self):
        """Abre o formulário de atualização com dados preenchidos"""
        if self.selected_client_index is None:
            messagebox.showwarning("Atualizar", "Selecione um cliente para atualizar!")
            return
        
        client_to_update = self.client_data[self.selected_client_index]
        
        # 🚨 CORRIGIDO: Usando self.controller.app_root
        ClientForm(self.controller.app_root, 
                   callback=lambda data: self.handle_client_callback(data, "Atualizar"), 
                   client=client_to_update, 
                   mode="Atualizar")
    def remover_cliente(self):
        """Remove o cliente selecionado"""
        if self.selected_client_index is None:
            messagebox.showwarning("Remover", "Selecione um cliente!")
            return

        client = self.client_data[self.selected_client_index]
        confirm = messagebox.askyesno("Remover", f"Confirmar a remoção de {client['nome']} (CPF: {client['cpf']})?")
        
        if confirm:
            deleted_count = delete_client(client["cpf"])
            if deleted_count > 0:
                messagebox.showinfo("Sucesso", "Cliente removido com sucesso!")
            else:
                messagebox.showerror("Erro", "Falha ao remover cliente. Nenhuma alteração feita.")
            
            # Recarrega a tabela e limpa a seleção
            self.load_clients()
            self.selected_client_index = None

    def export_to_excel(self):
        """Exporta os dados da tabela para Excel"""
        if not self.client_data:
            messagebox.showwarning("Exportar", "Nenhum cliente para exportar!")
            return

        df = pd.DataFrame(self.client_data)
        arquivo = "clientes_saciar.xlsx"
        try:
            df.to_excel(arquivo, index=False)
            messagebox.showinfo("Exportar", f"Exportado com sucesso: {arquivo}")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao exportar: {e}")