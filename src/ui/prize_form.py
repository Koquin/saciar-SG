import customtkinter as ctk
from tkinter import messagebox
from controllers.prize_controller import get_prizes, update_prizes

class PrizeForm(ctk.CTkToplevel):
    def __init__(self, master, controller, prizes_data):
        super().__init__(master)
        self.controller = controller
        self.prizes_data = prizes_data
        self.entry_widgets = []
        self.next_row = 1
        self.add_button = None
        self.title("Editar Prêmios de Fidelidade")
        self.geometry("500x450")
        self.resizable(False, False)
        self.after(10, self.grab_set)
        self.after(10, self.focus_force)
        ctk.CTkLabel(self, text="Configuração de Prêmios",
                     font=ctk.CTkFont(size=18, weight="bold")).pack(pady=10)
        self.scroll_frame = ctk.CTkScrollableFrame(self, width=450, height=300)
        self.scroll_frame.pack(padx=20, pady=5, fill="both", expand=True)
        self.setup_prize_entries()
        ctk.CTkButton(self, text="Salvar Prêmios", fg_color="#E67E22", command=self.save_prizes).pack(pady=15)

    def setup_prize_entries(self):
        ctk.CTkLabel(self.scroll_frame, text="Pontos Necessários", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, padx=10, pady=5)
        ctk.CTkLabel(self.scroll_frame, text="Mensagem / Descrição do Prêmio", font=ctk.CTkFont(weight="bold")).grid(row=0, column=1, padx=10, pady=5)
        self.next_row = 1
        for i, prize in enumerate(self.prizes_data):
            entry_pontos = ctk.CTkEntry(self.scroll_frame, width=150)
            entry_pontos.insert(0, str(prize.get('pontos', '')))
            entry_pontos.grid(row=self.next_row, column=0, padx=10, pady=5)
            entry_premio = ctk.CTkEntry(self.scroll_frame, width=250)
            entry_premio.insert(0, prize.get('premio', ''))
            entry_premio.grid(row=self.next_row, column=1, padx=10, pady=5)
            self.entry_widgets.append({
                'pontos': entry_pontos,
                'premio': entry_premio
            })
            self.next_row += 1
        self.add_button = ctk.CTkButton(self.scroll_frame, text="+ Adicionar Novo", command=self.add_new_prize_row)
        self.add_button.grid(row=self.next_row, column=0, columnspan=2, pady=10)


    def add_new_prize_row(self):
        entry_pontos = ctk.CTkEntry(self.scroll_frame, width=150)
        entry_pontos.grid(row=self.next_row, column=0, padx=10, pady=5)
        entry_premio = ctk.CTkEntry(self.scroll_frame, width=250)
        entry_premio.grid(row=self.next_row, column=1, padx=10, pady=5)
        self.entry_widgets.append({
            'pontos': entry_pontos,
            'premio': entry_premio
        })
        self.next_row += 1
        self.add_button.grid(row=self.next_row, column=0, columnspan=2, pady=10)
        
    def save_prizes(self):
        new_prizes = []
        for i, entry_set in enumerate(self.entry_widgets):
            pontos_str = entry_set['pontos'].get().strip()
            premio = entry_set['premio'].get().strip()
            if not pontos_str and not premio:
                continue
            try:
                pontos = int(pontos_str)
                if pontos <= 0:
                    messagebox.showerror("Erro de Entrada", f"Pontos '{pontos_str}' devem ser um número inteiro positivo.")
                    return
            except ValueError:
                messagebox.showerror("Erro de Entrada", f"Pontos '{pontos_str}' inválidos ou zero.")
                return
            if not premio:
                messagebox.showerror("Erro de Entrada", f"O prêmio para {pontos} pontos não pode estar vazio.")
                return
            new_prizes.append({
                'pontos': pontos,
                'premio': premio
            })
        try:
            if not new_prizes:
                confirm = messagebox.askyesno("Confirmação", "Deseja remover TODOS os prêmios de fidelidade?")
                if not confirm:
                    return
            result = update_prizes(new_prizes)
            if result:
                messagebox.showinfo("Sucesso", f"Prêmios atualizados com sucesso! {len(new_prizes)} prêmios salvos.")
                self.destroy()
            else:
                messagebox.showerror("Erro de API", "Falha ao salvar prêmios no banco de dados.")
        except Exception as e:
            messagebox.showerror("Erro de API", f"Falha ao salvar prêmios: {e}")