import customtkinter as ctk
import sqlite3

class ListaCadastros:
    def __init__(self, master, voltar_callback):
        self.master = master
        self.voltar_callback = voltar_callback
        self.row_count = 0  # Inicializa row_count para evitar erros

        # Limpar a tela principal
        for widget in self.master.winfo_children():
            widget.destroy()

        # Configurando a responsividade da janela
        self.master.grid_columnconfigure(0, weight=1)  # Coluna do ID com menos peso
        for i in range(1, 6):  # Outras colunas com mais espaço
            self.master.grid_columnconfigure(i, weight=2)  # Peso maior para dar mais espaço

        self.master.grid_rowconfigure(0, weight=1)

        # Botão de Voltar no canto superior esquerdo
        self.botao_voltar = ctk.CTkButton(self.master, text="Voltar", command=self.voltar_callback, width=70, height=30)
        self.botao_voltar.grid(row=0, column=0, padx=10, pady=10, sticky="nw")  # Posiciona no canto superior esquerdo

        # Título da nova tela
        self.titulo = ctk.CTkLabel(self.master, text="Lista de Cadastros", font=ctk.CTkFont(size=18, weight="bold"))
        self.titulo.grid(row=0, column=1, padx=20, pady=20, columnspan=5, sticky="ew")

        # Exibir cadastros
        self.exibir_cadastros()

    def exibir_cadastros(self):
        conn = sqlite3.connect("cadastros.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM livros")
        registros = cursor.fetchall()
        conn.close()

        if not registros:
            self.msg = ctk.CTkLabel(self.master, text="Nenhum cadastro foi realizado ainda.")
            self.msg.grid(row=1, column=0, padx=20, pady=10, columnspan=6, sticky="ew")
            self.row_count = 1  # Atualiza para garantir que o botão volte após a mensagem
            return

        # Criar cabeçalhos da tabela
        headers = ["ID", "Nome", "Autor", "Editora", "Páginas", "ISBN", "Gênero"]
        for i, header in enumerate(headers):
            label = ctk.CTkLabel(self.master, text=header, font=ctk.CTkFont(size=12, weight="bold"), fg_color="#3d8bd9", padx=10, pady=5)
            label.grid(row=1, column=i, padx=5, pady=5, sticky="ew")

        # Exibir os registros da tabela
        for i, registro in enumerate(registros):
            for j, valor in enumerate(registro):
                label = ctk.CTkLabel(self.master, text=str(valor), font=ctk.CTkFont(size=12), fg_color="#333333", padx=10, pady=5, corner_radius=8)
                label.grid(row=i+2, column=j, padx=5, pady=5, sticky="ew")

        # Atualiza o número de linhas, para posicionar o botão de voltar corretamente
        self.row_count = len(registros) + 2
        # Configurando a responsividade para as linhas da tabela
        for i in range(self.row_count):
            self.master.grid_rowconfigure(i+2, weight=1)
