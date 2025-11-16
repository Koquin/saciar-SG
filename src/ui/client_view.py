# src/ui/client_view.py
import customtkinter as ctk
from tkinter import ttk, messagebox, filedialog
import csv
from .prize_form import PrizeForm
from .client_form import ClientForm
from controllers.cliente_controller import get_clients, post_client, put_client, delete_client, search_clients
from controllers.prize_controller import get_prizes

class ClientView(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.client_data = []
        self.selected_client_index = None
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)
        self.grid_columnconfigure(0, weight=1)
        self.create_search_form()
        self.create_client_table()
        self.btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_frame.grid(row=2, column=0, pady=10, sticky="ew")
        self.btn_frame.grid_columnconfigure(0, weight=1)
        self.btn_frame.grid_columnconfigure(6, weight=1)
        ctk.CTkButton(self.btn_frame, text="Cadastrar Cliente", command=self.cadastrar_cliente).grid(row=0, column=1, padx=10)
        ctk.CTkButton(self.btn_frame, text="Atualizar Cliente", command=self.atualizar_cliente).grid(row=0, column=2, padx=10)
        ctk.CTkButton(self.btn_frame, text="Remover Cliente", command=self.remover_cliente).grid(row=0, column=3, padx=10)
        ctk.CTkButton(self.btn_frame, text="Editar Prêmios", command=self.editar_premios).grid(row=0, column=4, padx=10)
        ctk.CTkButton(self.btn_frame, text="Exportar Excel", fg_color="#27AE60", command=self.export_to_excel).grid(row=0, column=5, padx=10)
        self.load_clients()

    def create_search_form(self):
        self.search_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.search_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))
        self.search_frame.grid_columnconfigure(0, weight=1)
        self.entry_search = ctk.CTkEntry(self.search_frame, placeholder_text="Buscar por Nome, CPF ou Telefone", width=300)
        self.entry_search.grid(row=0, column=0, padx=(0, 10), sticky="w")
        ctk.CTkButton(self.search_frame, text="Filtrar", command=self.filter_clients).grid(row=0, column=1, padx=(0, 10))
        ctk.CTkButton(self.search_frame, text="Limpar", command=self.clear_filter).grid(row=0, column=2)
        self.entry_search.bind('<Return>', lambda event: self.filter_clients())

    def filter_clients(self):
        """Chama a função de busca e recarrega a tabela com os resultados."""
        query = self.entry_search.get().strip()
        try:
            self.client_data = search_clients(query)
            self.display_clients(self.client_data)
        except Exception as e:
            messagebox.showerror("Erro de Filtro", f"Falha ao filtrar clientes: {e}")

    def clear_filter(self):
        """Limpa o campo de busca e recarrega todos os clientes."""
        self.entry_search.delete(0, 'end')
        self.load_clients() 

    def create_client_table(self):
        """Tabela de clientes"""
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview.Heading", font=("Helvetica", 14, "bold"))
        style.configure("Treeview", font=("Helvetica", 12))
        style.map('Treeview', background=[('selected', '#2E86DE')])

        self.tree = ttk.Treeview(
            self,
            columns=("id", "nome", "cpf", "telefone", "pontos"),
            show="headings",
            selectmode="browse",
        )
        self.tree.heading("id", text="ID")
        self.tree.heading("nome", text="NOME")
        self.tree.heading("cpf", text="CPF")
        self.tree.heading("telefone", text="TELEFONE")
        self.tree.heading("pontos", text="PONTOS")

        # Ocultar a coluna ID (existirá nos dados mas não será exibida)
        self.tree.column("id", width=0, anchor='center', stretch=False, minwidth=0)
        self.tree.column("nome", width=200, anchor='w')
        self.tree.column("cpf", width=120, anchor='center')
        self.tree.column("telefone", width=120, anchor='center')
        self.tree.column("pontos", width=80, anchor='center')
        
        self.tree.grid(row=1, column=0, sticky="nsew", padx=10, pady=10) # row=1

        self.tree.bind("<<TreeviewSelect>>", self.on_select)

    def load_clients(self):
        """Carrega todos os clientes do backend."""
        try:
            self.client_data = get_clients()
            self.display_clients(self.client_data)
            print("Clientes carregados:", self.client_data)
        except Exception as e:
            messagebox.showerror("Erro de API", f"Falha ao carregar clientes: {e}")

    def display_clients(self, clients):
        """Preenche a tabela com os dados dos clientes"""
        self.tree.delete(*self.tree.get_children())
        for client in clients:
            pontos = client.get("pontos", 0)
            self.tree.insert("", "end", values=(
                client["id"],
                client["nome"],
                client["cpf"],
                client["telefone"],
                pontos,
            ))

    def on_select(self, event):
        """Atualiza o índice do cliente selecionado"""
        selected = self.tree.selection()
        if selected:
            print("Item selecionado na tabela:", selected)
            item_id = selected[0]
            values = self.tree.item(item_id, 'values')
            if values:
                id = values[0] 
                print("Valores do item selecionado:", values)
                for i, client in enumerate(self.client_data):
                    if client.get('id') == id:
                        self.selected_client_index = i
                        print("Cliente selecionado:", client)
                        return
        print("Nenhum cliente selecionado.")
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
        
        self.load_clients()
        self.selected_client_index = None

    def cadastrar_cliente(self):
        """Abre o formulário de cadastro"""
        ClientForm(self.controller,
                   callback=lambda data: self.handle_client_callback(data, "Cadastrar"), 
                   mode="Cadastrar")

    def atualizar_cliente(self):
        print("Índice do cliente selecionado para atualização:", self.selected_client_index)
        if self.selected_client_index is None:
            messagebox.showwarning("Atualizar", "Selecione um cliente para atualizar!")
            return
        
        client_to_update = self.client_data[self.selected_client_index]
        print("Cliente a ser atualizado:", client_to_update)
        ClientForm(self.controller, 
                   callback=lambda data: self.handle_client_callback(data, "Atualizar"), 
                   client=client_to_update, 
                   mode="Atualizar")
                   
    def remover_cliente(self):
        if self.selected_client_index is None:
            messagebox.showwarning("Remover", "Selecione um cliente!")
            return

        client = self.client_data[self.selected_client_index]
        confirm = messagebox.askyesno("Remover", f"Confirmar a remoção de {client['nome']} (CPF: {client['cpf']})?")
        
        if confirm:
            deleted = delete_client(client["id"])
            print("Resultado da deleção no ClientView:", deleted)
            if deleted:
                messagebox.showinfo("Sucesso", "Cliente removido com sucesso!")
            else:
                messagebox.showerror("Erro", "Falha ao remover cliente. Nenhuma alteração feita.")
            
            self.load_clients()
            self.selected_client_index = None

            
    def editar_premios(self):
        """Busca os prêmios atuais e abre o formulário modal de edição."""
        try:
            prizes_data = get_prizes() 
            
            PrizeForm(self.controller, self.controller, prizes_data)
            
        except Exception as e:
            messagebox.showerror("Erro de API", f"Falha ao carregar a lista de prêmios: {e}")

    def export_to_excel(self):
        """Exporta os dados da tabela de clientes para um arquivo CSV (compatível com Excel)."""
        if not self.client_data:
            messagebox.showwarning("Exportar", "Nenhum cliente para exportar!")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title="Salvar Lista de Clientes"
        )

        if not file_path:
            return 
            
        try:
            # Excluir a coluna 'id' dos headers exportados (é oculta)
            headers = [self.tree.heading(col)['text'] for col in self.tree['columns'] if col != 'id']
            
            with open(file_path, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file, delimiter=';') 
                writer.writerow(headers)
                
                for client in self.client_data:
                    row = [
                        client.get("nome", "N/A"),
                        client.get("cpf", "N/A"),
                        client.get("telefone", "N/A"),
                        client.get("pontos", 0)
                    ]
                    writer.writerow(row)
            
            messagebox.showinfo("Exportar", f"Lista de clientes exportada com sucesso para:\n{file_path}")
            
        except Exception as e:
            messagebox.showerror("Erro de Exportação", f"Ocorreu um erro ao salvar o arquivo: {e}")
