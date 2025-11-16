# src/ui/purchase_view.py
import customtkinter as ctk
from tkinter import ttk, messagebox, BooleanVar, filedialog
from controllers.purchase_controller import get_purchases, post_purchase, delete_purchase, search_purchases
from datetime import datetime
import csv 

class PurchaseView(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.purchase_data = []
        
        # Configurações do Grid
        self.grid_rowconfigure(0, weight=0)    # Linha 0 (Busca) é fixa
        self.grid_rowconfigure(1, weight=1)    # Linha 1 (Tabela) expande verticalmente
        self.grid_rowconfigure(2, weight=0)    # Linha 2 (Botões) é fixa
        self.grid_columnconfigure(0, weight=1) 

        # 1. Formulário de Busca (row=0)
        self.create_search_form()

        # 2. Tabela (row=1)
        self.create_purchase_table()

        # 3. Botões de Ação (row=2)
        self.btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_frame.grid(row=2, column=0, pady=10, sticky="ew") 

        # --- CENTRALIZAÇÃO E NOVO BOTÃO ---
        self.btn_frame.grid_columnconfigure(0, weight=1)
        self.btn_frame.grid_columnconfigure(4, weight=1)

        ctk.CTkButton(self.btn_frame, text="Criar Compra", command=self.criar_compra).grid(
            row=0, column=1, padx=10, pady=0)
        
        ctk.CTkButton(self.btn_frame, text="Apagar Compra", command=self.delete_purchase_entry).grid(
            row=0, column=2, padx=10, pady=0)

        ctk.CTkButton(self.btn_frame, text="Exportar para Excel", fg_color="#27AE60", command=self.export_to_excel).grid(
            row=0, column=3, padx=10, pady=0)
        
        self.load_purchases()

    def create_search_form(self):
        """Cria o campo de busca e botão."""
        self.search_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.search_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))
        self.search_frame.grid_columnconfigure(0, weight=1)
        
        # Campo de entrada
        self.entry_search = ctk.CTkEntry(self.search_frame, placeholder_text="Buscar por Cliente, CPF ou Data", width=300)
        self.entry_search.grid(row=0, column=0, padx=(0, 10), sticky="w")
        
        # Botão de Busca
        ctk.CTkButton(self.search_frame, text="Filtrar", command=self.filter_purchases).grid(row=0, column=1, padx=(0, 10))
        
        # Botão de Limpar
        ctk.CTkButton(self.search_frame, text="Limpar", command=self.clear_filter).grid(row=0, column=2)
        
        # Permite buscar ao pressionar Enter
        self.entry_search.bind('<Return>', lambda event: self.filter_purchases())

    def filter_purchases(self):
        """Chama a função de busca e recarrega a tabela com os resultados."""
        query = self.entry_search.get().strip()
        try:
            self.purchase_data = search_purchases(query)
            self.display_purchases(self.purchase_data)
        except Exception as e:
            messagebox.showerror("Erro de Filtro", f"Falha ao filtrar compras: {e}")

    def clear_filter(self):
        """Limpa o campo de busca e recarrega todas as compras."""
        self.entry_search.delete(0, 'end')
        self.load_purchases() 

    def export_to_excel(self):
        """Exporta os dados da tabela de compras para um arquivo CSV, formatando a data."""
        
        if not self.purchase_data:
            messagebox.showwarning("Exportação", "Não há dados de compra para exportar.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title="Salvar Histórico de Compras"
        )

        if not file_path:
            return 

        try:
            headers = [self.tree.heading(col)['text'] for col in self.tree['columns']]
            
            with open(file_path, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file, delimiter=';') 
                writer.writerow(headers)
                
                for compra in self.purchase_data:
                    valor_formatado = f"{compra.get('valor', 0.0):.2f}".replace('.', ',') 
                    
                    data_str = compra.get("data", "N/A")
                    data_formatada = data_str
                    try:
                        date_obj = datetime.strptime(data_str, "%Y-%m-%d %H:%M:%S")
                        data_formatada = date_obj.strftime("%d/%m/%Y %H:%M:%S") 
                    except (ValueError, TypeError):
                        try:
                             date_obj = datetime.strptime(data_str, "%Y-%m-%d")
                             data_formatada = date_obj.strftime("%d/%m/%Y")
                        except (ValueError, TypeError):
                             pass

                    is_delivery = compra.get("is_delivery", False)
                    delivery_status_str = "Sim" if is_delivery else "Não"
                    pontos = compra.get("pontos_ganhos", 0)

                    row = [
                        compra.get("cliente", "N/A"),
                        compra.get("cpf", "N/A"),
                        valor_formatado,
                        data_formatada, 
                        pontos,
                        delivery_status_str
                    ]
                    writer.writerow(row)
            
            messagebox.showinfo("Exportação", f"Dados exportados com sucesso para:\n{file_path}")

        except Exception as e:
            messagebox.showerror("Erro de Exportação", f"Ocorreu um erro ao salvar o arquivo: {e}")

    def delete_purchase_entry(self):
        """Obtém a compra selecionada e chama a função de deleção."""
        selected_item = self.tree.focus()
        
        if not selected_item:
            messagebox.showwarning("Seleção", "Selecione uma compra na tabela para apagar.")
            return

        values = self.tree.item(selected_item, 'values')
        
        purchase_id = values[0]  # ID é a primeira coluna (oculta)
        cpf = values[2]  # CPF agora é o índice 2
        data_hora = values[4]  # Data agora é o índice 4
        
        if messagebox.askyesno("Confirmação", f"Tem certeza que deseja apagar a compra de {cpf} na data/hora {data_hora}?"):
            try:
                deleted_count = delete_purchase(purchase_id)
                
                if deleted_count > 0:
                    messagebox.showinfo("Sucesso", "Compra apagada com sucesso!")
                    self.load_purchases() 
                else:
                    messagebox.showerror("Erro", "Falha ao apagar compra. Item não encontrado no banco de dados. (Verifique o formato da data/hora)")
            except Exception as e:
                messagebox.showerror("Erro", f"Ocorreu um erro ao apagar: {e}")

    def create_purchase_table(self):
        """Tabela de histórico de compras"""
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview.Heading", font=("Helvetica", 14, "bold"))
        style.configure("Treeview", font=("Helvetica", 12))
        style.map('Treeview', background=[('selected', '#E67E22')])

        self.tree = ttk.Treeview(
            self,
            columns=("id", "cliente", "cpf", "valor", "data", "pontos_ganhos", "delivery_status"),
            show="headings",
            selectmode="browse",
        )
        # ID é uma coluna oculta que usaremos para deleção
        self.tree.heading("id", text="ID")
        self.tree.column("id", width=0, stretch=False)  # Oculta a coluna
        
        self.tree.heading("cliente", text="CLIENTE")
        self.tree.heading("cpf", text="CPF")
        self.tree.heading("valor", text="VALOR (R$)")
        self.tree.heading("data", text="DATA")
        self.tree.heading("pontos_ganhos", text="PONTOS GANHOS")
        self.tree.heading("delivery_status", text="DELIVERY")

        self.tree.column("cliente", width=180, anchor='w')
        self.tree.column("cpf", width=120, anchor='center')
        self.tree.column("valor", width=100, anchor='e')
        self.tree.column("data", width=150, anchor='center')
        self.tree.column("pontos_ganhos", width=80, anchor='center')
        self.tree.column("delivery_status", width=80, anchor='center')
        
        self.tree.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

    def load_purchases(self):
        """Carrega todas as compras do backend."""
        try:
            self.purchase_data = get_purchases() 
            self.display_purchases(self.purchase_data)
        except Exception as e:
            messagebox.showerror("Erro de API", f"Falha ao carregar compras: {e}")

    def display_purchases(self, purchases):
        """Preenche a tabela com os dados das compras"""
        self.tree.delete(*self.tree.get_children())
        for compra in purchases:
            valor_formatado = f"{compra.get('valor', 0.0):.2f}"
            is_delivery = compra.get("is_delivery", False)
            delivery_status_str = "Sim" if is_delivery else "Não"
            pontos = compra.get("pontos_ganhos", 0) 
            
            data_str = compra.get("data", "N/A")
            data_exibicao = data_str
            try:
                date_obj = datetime.strptime(data_str, "%Y-%m-%d %H:%M:%S")
                data_exibicao = date_obj.strftime("%d/%m/%Y %H:%M:%S")
            except Exception:
                pass 

            self.tree.insert("", "end", values=(
                compra.get("id", ""),  # ID oculto
                compra.get("cliente", "N/A"),
                compra.get("cpf", "N/A"),
                valor_formatado,
                data_exibicao, 
                pontos,
                delivery_status_str
            ))

    def criar_compra(self):
        """Abre o formulário para registrar uma nova compra com opção Delivery."""
        
        popup = ctk.CTkToplevel(self.controller)        
        popup.title("Registrar Compra")
        popup.geometry("350x300")
        popup.resizable(False, False)
        
        popup.after(250, popup.grab_set)
        popup.after(250, popup.focus_force)

        ctk.CTkLabel(popup, text="CPF do Cliente (Opcional):").pack(pady=(10, 5))
        entry_cpf = ctk.CTkEntry(popup, width=300)
        entry_cpf.pack(pady=5)

        ctk.CTkLabel(popup, text="Valor da Compra (R$):").pack(pady=5)
        entry_valor = ctk.CTkEntry(popup, width=300)
        entry_valor.pack(pady=5)
        
        self.check_delivery_var = BooleanVar(value=False) 
        
        check_delivery = ctk.CTkCheckBox(
            popup, 
            text="Delivery?", 
            variable=self.check_delivery_var, 
            onvalue=True, 
            offvalue=False
        )
        check_delivery.pack(pady=10)


        def salvar_compra():
            try:
                cpf = entry_cpf.get().strip()
                valor = float(entry_valor.get() or 0)
                is_delivery = self.check_delivery_var.get()
                
            except ValueError:
                messagebox.showerror("Erro de Entrada", "O valor da compra deve ser um número.")
                return

            if valor <= 0:
                messagebox.showwarning("Campos Obrigatórios", "Preencha um valor válido.")
                return

            data_hora_agora = datetime.now()
            
            compra = {
                "cliente": "Cliente Registrado",
                "cpf": cpf,
                "valor": valor,
                "is_delivery": is_delivery,
                "data": data_hora_agora.strftime("%Y-%m-%d %H:%M:%S")            
                }
            
            result = post_purchase(compra)
            if result:
                messagebox.showinfo("Sucesso", "Compra registrada com sucesso!")
                self.load_purchases()
                popup.destroy()
            else:
                messagebox.showerror("Erro", "Falha ao registrar compra. Verifique o servidor.")

        ctk.CTkButton(popup, text="Salvar", fg_color="#E67E22", command=salvar_compra).pack(pady=(15, 10))