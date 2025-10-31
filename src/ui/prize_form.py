import customtkinter as ctk
from tkinter import messagebox
from utils.api_utils import get_prizes, update_prizes 

class PrizeForm(ctk.CTkToplevel):
    def __init__(self, master, controller, prizes_data):
        super().__init__(master)
        print("DEBUG: Iniciando PrizeForm.__init__")
        self.controller = controller
        self.prizes_data = prizes_data
        self.entry_widgets = []
        self.next_row = 1 # Variável de estado para controlar a próxima linha livre
        self.add_button = None # Referência para o botão "Adicionar Novo"

        self.title("Editar Prêmios de Fidelidade")
        self.geometry("500x450")
        self.resizable(False, False)
        
        # Faz o pop-up ser modal
        self.after(10, self.grab_set)
        self.after(10, self.focus_force)

        ctk.CTkLabel(self, text="Configuração de Prêmios", 
                     font=ctk.CTkFont(size=18, weight="bold")).pack(pady=10)

        # Frame de Rolagem para os campos
        self.scroll_frame = ctk.CTkScrollableFrame(self, width=450, height=300)
        self.scroll_frame.pack(padx=20, pady=5, fill="both", expand=True)

        self.setup_prize_entries()

        # Botão Salvar
        ctk.CTkButton(self, text="Salvar Prêmios", fg_color="#E67E22", command=self.save_prizes).pack(pady=15)
        print("DEBUG: PrizeForm.__init__ concluído.")

    def setup_prize_entries(self):
        """Cria os campos de entrada para cada prêmio e o botão inicial."""
        print("DEBUG: Iniciando setup_prize_entries")
        
        # Títulos das colunas
        ctk.CTkLabel(self.scroll_frame, text="Pontos Necessários", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, padx=10, pady=5)
        ctk.CTkLabel(self.scroll_frame, text="Mensagem / Descrição do Prêmio", font=ctk.CTkFont(weight="bold")).grid(row=0, column=1, padx=10, pady=5)

        self.next_row = 1 # Começa na primeira linha de dados

        for i, prize in enumerate(self.prizes_data):
            print(f"DEBUG: Criando Entry para prêmio {i+1}: {prize}")
            # Entry para Pontos
            entry_pontos = ctk.CTkEntry(self.scroll_frame, width=150)
            entry_pontos.insert(0, str(prize.get('pontos', '')))
            entry_pontos.grid(row=self.next_row, column=0, padx=10, pady=5)

            # Entry para Prêmio/Mensagem
            entry_premio = ctk.CTkEntry(self.scroll_frame, width=250)
            entry_premio.insert(0, prize.get('premio', ''))
            entry_premio.grid(row=self.next_row, column=1, padx=10, pady=5)
            
            self.entry_widgets.append({
                'pontos': entry_pontos,
                'premio': entry_premio
            })
            self.next_row += 1 # Prepara para a próxima linha
            
        print(f"DEBUG: Total de {len(self.entry_widgets)} Entry Widgets criados inicialmente.")
        
        # Cria o botão "Adicionar Novo" e armazena a referência
        self.add_button = ctk.CTkButton(self.scroll_frame, text="+ Adicionar Novo", command=self.add_new_prize_row)
        self.add_button.grid(row=self.next_row, column=0, columnspan=2, pady=10)
        print("DEBUG: setup_prize_entries concluído.")


    def add_new_prize_row(self):
        """Adiciona uma nova linha vazia para um novo prêmio e move o botão."""
        print(f"DEBUG: Iniciando add_new_prize_row. Próxima linha livre: {self.next_row}")
        
        # Cria os novos widgets na linha atual
        # Entry para Pontos (Vazio)
        entry_pontos = ctk.CTkEntry(self.scroll_frame, width=150)
        entry_pontos.grid(row=self.next_row, column=0, padx=10, pady=5)
        
        # Entry para Prêmio/Mensagem (Vazio)
        entry_premio = ctk.CTkEntry(self.scroll_frame, width=250)
        entry_premio.grid(row=self.next_row, column=1, padx=10, pady=5)
        
        self.entry_widgets.append({
            'pontos': entry_pontos,
            'premio': entry_premio
        })

        # Atualiza a variável de estado para a próxima linha livre
        self.next_row += 1 

        # CORREÇÃO CHAVE: Move o botão "Adicionar Novo" para a nova linha livre
        self.add_button.grid(row=self.next_row, column=0, columnspan=2, pady=10)
        print(f"DEBUG: Nova linha adicionada. Novo next_row: {self.next_row}")
        
    def save_prizes(self):
        """Coleta os dados editados e chama a função de atualização da API."""
        print("DEBUG: Iniciando save_prizes.")
        new_prizes = []
        
        for i, entry_set in enumerate(self.entry_widgets):
            pontos_str = entry_set['pontos'].get().strip()
            premio = entry_set['premio'].get().strip()
            
            print(f"DEBUG: Processando widget {i+1}. Pontos='{pontos_str}', Prêmio='{premio}'")
            
            # Ignora linhas totalmente vazias
            if not pontos_str and not premio:
                print(f"DEBUG: Widget {i+1} ignorado (vazio).")
                continue

            try:
                pontos = int(pontos_str)
                if pontos <= 0:
                    messagebox.showerror("Erro de Entrada", f"Pontos '{pontos_str}' devem ser um número inteiro positivo.")
                    print("ERROR: Pontos inválidos ou zero. Retornando.")
                    return
            except ValueError:
                messagebox.showerror("Erro de Entrada", f"Pontos '{pontos_str}' inválidos ou zero.")
                print("ERROR: ValueError na conversão de pontos. Retornando.")
                return

            if not premio:
                messagebox.showerror("Erro de Entrada", f"O prêmio para {pontos} pontos não pode estar vazio.")
                print("ERROR: Prêmio vazio. Retornando.")
                return

            new_prizes.append({
                'pontos': pontos,
                'premio': premio
            })
            print(f"DEBUG: Prêmio válido adicionado. new_prizes atual tem {len(new_prizes)} itens.")
        
        # FIM DO LOOP
        
        print(f"DEBUG: Fim do loop de validação. new_prizes final: {new_prizes}")

        # Chama a função de atualização da API (agora fora do loop)
        try:
            # Verifica se há algo para salvar antes de chamar a API
            if not new_prizes:
                print("DEBUG: new_prizes está vazia.")
                confirm = messagebox.askyesno("Confirmação", "Deseja remover TODOS os prêmios de fidelidade?")
                if not confirm:
                    print("DEBUG: Remoção de todos os prêmios cancelada.")
                    return

            print(f"DEBUG: Chamando update_prizes com {len(new_prizes)} item(s).")
            result = update_prizes(new_prizes)
            
            if result:
                print("DEBUG: update_prizes retornou sucesso.")
                messagebox.showinfo("Sucesso", f"Prêmios atualizados com sucesso! {len(new_prizes)} prêmios salvos.")
                self.destroy()
            else:
                print("DEBUG: update_prizes retornou falha (False).")
                # update_prizes retorna False em caso de erro no MongoDB
                messagebox.showerror("Erro de API", "Falha ao salvar prêmios no banco de dados.")

        except Exception as e:
            print(f"ERROR: Exceção na chamada de update_prizes: {e}")
            messagebox.showerror("Erro de API", f"Falha ao salvar prêmios: {e}")