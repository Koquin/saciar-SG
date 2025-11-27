import customtkinter as ctk
from tkinter import ttk, messagebox, filedialog
from controllers.redeem_controller import get_redeems, post_redeem, delete_redeem, search_redeems
from controllers.prize_controller import get_prizes
from controllers.cliente_controller import search_clients
from datetime import datetime
import csv

class RedeemView(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.redeem_data = []
        self.prizes_data = []
        self.selected_redeem_index = None
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)
        self.grid_columnconfigure(0, weight=1)
        self.create_search_form()
        self.create_redeem_table()
        self.btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_frame.grid(row=2, column=0, pady=10, sticky="ew")
        self.btn_frame.grid_columnconfigure(0, weight=1)
        self.btn_frame.grid_columnconfigure(4, weight=1)
        ctk.CTkButton(self.btn_frame, text="Criar Resgate", command=self.criar_resgate).grid(
            row=0, column=1, padx=10, pady=0)
        ctk.CTkButton(self.btn_frame, text="Apagar Resgate", command=self.delete_redeem_entry).grid(
            row=0, column=2, padx=10, pady=0)
        ctk.CTkButton(self.btn_frame, text="Exportar para Excel", fg_color="#27AE60", command=self.export_to_excel).grid(
            row=0, column=3, padx=10, pady=0)
        self.load_redeems()

    def create_search_form(self):
        self.search_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.search_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))
        self.search_frame.grid_columnconfigure(0, weight=1)
        self.entry_search = ctk.CTkEntry(self.search_frame, placeholder_text="Buscar por Cliente ou Prêmio", width=300)
        self.entry_search.grid(row=0, column=0, padx=(0, 10), sticky="w")
        ctk.CTkButton(self.search_frame, text="Filtrar", command=self.filter_redeems).grid(row=0, column=1, padx=(0, 10))
        ctk.CTkButton(self.search_frame, text="Limpar", command=self.clear_filter).grid(row=0, column=2)
        self.entry_search.bind('<Return>', lambda event: self.filter_redeems())

    def filter_redeems(self):
        query = self.entry_search.get().strip()
        try:
            self.redeem_data = search_redeems(query)
            self.display_redeems(self.redeem_data)
        except Exception as e:
            messagebox.showerror("Erro de Filtro", f"Falha ao filtrar resgates: {e}")

    def clear_filter(self):
        self.entry_search.delete(0, 'end')
        self.load_redeems()

    def export_to_excel(self):
        if not self.redeem_data:
            messagebox.showwarning("Exportação", "Não há dados de resgate para exportar.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title="Salvar Histórico de Resgates"
        )

        if not file_path:
            return 

        try:
            headers = [self.tree.heading(col)['text'] for col in self.tree['columns']]
            
            with open(file_path, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file, delimiter=';') 
                writer.writerow(headers)
                
                for resgate in self.redeem_data:
                    data_str = resgate.get("data", "N/A")
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

                    row = [
                        resgate.get("cliente", "N/A"),
                        resgate.get("telefone", "N/A"),
                        resgate.get("premio", "N/A"),
                        data_formatada,
                    ]
                    writer.writerow(row)
            
            messagebox.showinfo("Exportação", f"Dados exportados com sucesso para:\n{file_path}")

        except Exception as e:
            messagebox.showerror("Erro de Exportação", f"Ocorreu um erro ao salvar o arquivo: {e}")

    def delete_redeem_entry(self):
        selected_item = self.tree.focus()
        
        if not selected_item:
            messagebox.showwarning("Seleção", "Selecione um resgate na tabela para apagar.")
            return

        values = self.tree.item(selected_item, 'values')
        
        redeem_id = values[0]
        cliente = values[1]
        premio = values[3]
        
        if messagebox.askyesno("Confirmação", f"Tem certeza que deseja apagar o resgate de {cliente} - {premio}?"):
            try:
                deleted_count = delete_redeem(redeem_id)
                
                if deleted_count > 0:
                    messagebox.showinfo("Sucesso", "Resgate apagado com sucesso!")
                    self.load_redeems() 
                else:
                    messagebox.showerror("Erro", "Falha ao apagar resgate. Item não encontrado no banco de dados.")
            except Exception as e:
                messagebox.showerror("Erro", f"Ocorreu um erro ao apagar: {e}")

    def create_redeem_table(self):
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview.Heading", font=("Helvetica", 14, "bold"))
        style.configure("Treeview", font=("Helvetica", 12))
        style.map('Treeview', background=[('selected', '#9B59B6')])

        self.tree = ttk.Treeview(
            self,
            columns=("id", "cliente", "telefone", "premio", "data"),
            show="headings",
            selectmode="browse",
        )
        self.tree.heading("id", text="ID")
        self.tree.column("id", width=0, stretch=False)
        
        self.tree.heading("cliente", text="CLIENTE")
        self.tree.heading("telefone", text="TELEFONE")
        self.tree.heading("premio", text="PRÊMIO")
        self.tree.heading("data", text="DATA DO RESGATE")

        self.tree.column("cliente", width=180, anchor='w')
        self.tree.column("telefone", width=150, anchor='center')
        self.tree.column("premio", width=180, anchor='center')
        self.tree.column("data", width=150, anchor='center')
        
        self.tree.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

    def load_redeems(self):
        try:
            self.redeem_data = get_redeems() 
            self.display_redeems(self.redeem_data)
        except Exception as e:
            messagebox.showerror("Erro de API", f"Falha ao carregar resgates: {e}")

    def display_redeems(self, redeems):
        self.tree.delete(*self.tree.get_children())
        for resgate in redeems:
            data_str = resgate.get("created_at", "N/A")
            data_exibicao = data_str
            try:
                date_obj = datetime.strptime(data_str, "%Y-%m-%d %H:%M:%S")
                data_exibicao = date_obj.strftime("%d/%m/%Y %H:%M:%S")
            except Exception:
                pass 

            self.tree.insert("", "end", values=(
                resgate.get("id", ""),
                resgate.get("cliente_nome", "N/A"),
                resgate.get("telefone", "N/A"),
                resgate.get("premio", "N/A"),
                data_exibicao
            ))

    def criar_resgate(self):
        try:
            self.prizes_data = get_prizes()
        except Exception as e:
            messagebox.showerror("Erro de API", f"Falha ao carregar prêmios: {e}")
            return

        if not self.prizes_data:
            messagebox.showwarning("Prêmios", "Nenhum prêmio disponível para resgate.")
            return


        popup = ctk.CTkToplevel(self.controller)        
        popup.title("Registrar Resgate")
        popup.geometry("350x150")
        popup.resizable(False, False)

        popup.after(250, popup.grab_set)
        popup.after(250, popup.focus_force)

        ctk.CTkLabel(popup, text="Telefone do Cliente:").pack(pady=(30, 5))
        entry_telefone = ctk.CTkEntry(popup, width=300)
        entry_telefone.pack(pady=5)

        def salvar_resgate():
            try:
                telefone = entry_telefone.get().strip()
                if not telefone:
                    messagebox.showwarning("Campos Obrigatórios", "Preencha o telefone do cliente.")
                    return

                # Buscar o cliente pelo telefone para obter a quantidade de pontos
                clients_found = search_clients(telefone)
                client = None
                for c in clients_found:
                    if c.get("telefone") == telefone:
                        client = c
                        break
                if not client and clients_found:
                    client = clients_found[0]

                if not client:
                    messagebox.showerror("Erro", "Cliente não encontrado para o telefone informado.")
                    return

                pontos = client.get("pontos", 0)

                # Envia apenas telefone e pontos conforme solicitado
                resgate = {
                    "telefone": telefone,
                    "pontos": pontos,
                }

                result = post_redeem(resgate)
                if result:
                    print("Resultado: ", result)
                    messagebox.showinfo("Resultado", result.get("message"))
                    self.load_redeems()
                    popup.destroy()
                else:
                    messagebox.showerror("Erro", "Falha ao registrar resgate. Verifique o servidor.")
            except Exception as e:
                messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

        ctk.CTkButton(popup, text="Salvar", fg_color="#9B59B6", command=salvar_resgate).pack(pady=(15, 10))
