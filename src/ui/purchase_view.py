# src/ui/purchase_view.py
import customtkinter as ctk
from tkinter import ttk, messagebox, BooleanVar
from utils.api_utils import get_purchases, post_purchase, delete_purchase
import datetime

class PurchaseView(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.purchase_data = []
        
        # Configurações do Grid para Expansão da Tabela
        self.grid_rowconfigure(0, weight=1)    # Linha 0 (tabela) expande verticalmente
        self.grid_columnconfigure(0, weight=1) # Coluna 0 (tabela) expande horizontalmente

        # Tabela (agora usa grid)
        self.create_purchase_table()

        # Botões de Ação
        self.btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_frame.grid(row=1, column=0, pady=10, sticky="ew") 

        ctk.CTkButton(self.btn_frame, text="Criar Compra", fg_color="#E67E22", command=self.criar_compra).pack(side="left", padx=10)
        
        ctk.CTkButton(self.btn_frame, text="Apagar Compra", fg_color="#C0392B", command=self.delete_purchase_entry).pack(side="left", padx=10)
        
        self.load_purchases()

    def delete_purchase_entry(self):
        """Obtém a compra selecionada e chama a função de deleção."""
        selected_item = self.tree.focus()
        
        if not selected_item:
            messagebox.showwarning("Seleção", "Selecione uma compra na tabela para apagar.")
            return

        # Obtém os valores da linha selecionada: (cliente, cpf, valor, data, pontos, delivery)
        values = self.tree.item(selected_item, 'values')
        
        # Extraímos os dados que o backend precisa (CPF e Data)
        cpf = values[1] 
        data = values[3]
        
        # Confirmação
        if messagebox.askyesno("Confirmação", f"Tem certeza que deseja apagar a compra de {cpf} na data {data}?"):
            try:
                # Chama a função de deleção na API
                deleted_count = delete_purchase(cpf, data)
                
                if deleted_count > 0:
                    messagebox.showinfo("Sucesso", "Compra apagada com sucesso!")
                    self.load_purchases() # Recarrega a tabela
                else:
                    messagebox.showerror("Erro", "Falha ao apagar compra. Item não encontrado no banco de dados.")
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
            # ADICIONADO: 'pontos_ganhos', 'delivery_status'
            columns=("cliente", "cpf", "valor", "data", "pontos_ganhos", "delivery_status"),
            show="headings",
            selectmode="browse",
        )
        self.tree.heading("cliente", text="CLIENTE")
        self.tree.heading("cpf", text="CPF")
        self.tree.heading("valor", text="VALOR (R$)")
        self.tree.heading("data", text="DATA")
        # NOVOS HEADINGS
        self.tree.heading("pontos_ganhos", text="PONTOS GANHOS")
        self.tree.heading("delivery_status", text="DELIVERY")

        self.tree.column("cliente", width=180, anchor='w')
        self.tree.column("cpf", width=120, anchor='center')
        self.tree.column("valor", width=100, anchor='e')
        self.tree.column("data", width=150, anchor='center')
        # NOVAS COLUNAS
        self.tree.column("pontos_ganhos", width=80, anchor='center')
        self.tree.column("delivery_status", width=80, anchor='center')
        
        # MUDANÇA: Usar grid no lugar de pack para preencher o CTkFrame
        self.tree.grid(row=0, column=0, sticky="nsew", padx=10, pady=10) 

    def load_purchases(self):
        """Carrega histórico de compras do backend usando API"""
        try:
            self.purchase_data = get_purchases()
            self.display_purchases(self.purchase_data)
        except Exception as e:
            messagebox.showerror("Erro de API", f"Falha ao carregar compras: {e}")

    def display_purchases(self, purchases):
        """Preenche a tabela com os dados das compras"""
        self.tree.delete(*self.tree.get_children())
        for compra in purchases:
            valor_formatado = f"R$ {compra.get('valor', 0.0):.2f}"
            
            # CONVERSÃO: True/False para SIM/NÃO
            is_delivery = compra.get("is_delivery", False)
            delivery_status_str = "Sim" if is_delivery else "Não"
            
            # Valor dos pontos (assumimos que o backend retorna 'pontos_ganhos')
            pontos = compra.get("pontos_ganhos", 0) 

            self.tree.insert("", "end", values=(
                compra.get("cliente", "N/A"),
                compra.get("cpf", "N/A"),
                valor_formatado,
                compra.get("data", "N/A"),
                pontos,                   # ADICIONADO
                delivery_status_str       # ADICIONADO
            ))

    def criar_compra(self):
        """Abre o formulário para registrar uma nova compra com opção Delivery."""
        
        # CORREÇÃO 1: Usar self.controller.app_root como master para o pop-up
        popup = ctk.CTkToplevel(self.controller.app_root)        
        popup.title("Registrar Compra")
        popup.geometry("350x300")
        popup.resizable(False, False)
        
        # CORREÇÃO 2: Adiar grab_set e focus_force
        popup.after(250, popup.grab_set)
        popup.after(250, popup.focus_force)

        # 1. Campo CPF
        ctk.CTkLabel(popup, text="CPF do Cliente:").pack(pady=(10, 5))
        entry_cpf = ctk.CTkEntry(popup, width=300)
        entry_cpf.pack(pady=5)

        # 2. Campo Valor
        ctk.CTkLabel(popup, text="Valor da Compra (R$):").pack(pady=5)
        entry_valor = ctk.CTkEntry(popup, width=300)
        entry_valor.pack(pady=5)
        
        # 3. Campo Delivery (Checkbox)
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
                print(is_delivery)
                
            except ValueError:
                messagebox.showerror("Erro de Entrada", "O valor da compra deve ser um número.")
                return

            if not cpf or valor <= 0:
                messagebox.showwarning("Campos Obrigatórios", "Preencha o CPF e um valor válido.")
                return

            compra = {
                # O backend deve buscar o nome e calcular a pontuação
                "cliente": "Cliente Registrado",
                "cpf": cpf,
                "valor": valor,
                "is_delivery": is_delivery,
                "data": datetime.date.today().strftime("%Y-%m-%d")
            }
            
            result = post_purchase(compra)
            if result:
                messagebox.showinfo("Sucesso", "Compra registrada com sucesso!")
                self.load_purchases()
                popup.destroy()
            elif result == None:
                messagebox.showerror("Erro", "CPF não localizado.")
            else:
                messagebox.showerror("Erro", "Falha ao registrar compra. Verifique o servidor.")

        ctk.CTkButton(popup, text="Salvar", fg_color="#E67E22", command=salvar_compra).pack(pady=(15, 10))