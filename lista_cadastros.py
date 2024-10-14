import customtkinter as ctk
import sqlite3

class ListaCadastros:
    def __init__(self, master, voltar_callback):
        self.master = master
        self.voltar_callback = voltar_callback
        self.row_count = 0  # Inicializa row_count para evitar erros
        self.livros_por_pagina = 15  # Mudança para 15 livros por página
        self.pagina_atual = 1  # Página inicial
        self.total_paginas = 1  # Inicialização para evitar erros

        # Criar a estrutura da tela uma vez
        self.criar_interface()

    def criar_interface(self):
        # Configurando a responsividade da janela
        self.master.grid_columnconfigure(0, weight=1)
        for i in range(1, 6):
            self.master.grid_columnconfigure(i, weight=1)  # Ajuste aqui para todas as colunas

        self.master.grid_rowconfigure(0, weight=0)  # Para o título e botão de voltar
        self.master.grid_rowconfigure(1, weight=1)  # Para a lista de registros
        self.master.grid_rowconfigure(2, weight=0)  # Para os botões de navegação

        # Botão de Voltar no canto superior esquerdo
        self.botao_voltar = ctk.CTkButton(self.master, text="Voltar", command=self.voltar_callback, width=70, height=30)
        self.botao_voltar.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

        # Título da nova tela
        self.titulo = ctk.CTkLabel(self.master, text="Lista de Cadastros", font=ctk.CTkFont(size=18, weight="bold"))
        self.titulo.grid(row=0, column=1, padx=20, pady=20, columnspan=5, sticky="ew")

    def exibir_cadastros(self):
        conn = sqlite3.connect("cadastros.db")
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM livros")
        total_registros = cursor.fetchone()[0]  # Contagem total de registros
        self.total_paginas = (total_registros // self.livros_por_pagina) + (1 if total_registros % self.livros_por_pagina > 0 else 0)

        offset = (self.pagina_atual - 1) * self.livros_por_pagina
        cursor.execute("SELECT * FROM livros LIMIT ? OFFSET ?", (self.livros_por_pagina, offset))
        registros = cursor.fetchall()
        conn.close()

        # Limpar tabela anterior, se houver (exceto o botão "Voltar" e o título)
        for widget in self.master.grid_slaves():
            if isinstance(widget, ctk.CTkLabel) and widget not in (self.titulo, self.botao_voltar):
                widget.destroy()

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
                label.grid(row=i + 2, column=j, padx=5, pady=5, sticky="ew")

        # Atualiza o número de linhas, para posicionar os botões de paginação corretamente
        self.row_count = len(registros) + 2

        # Configurando a responsividade para as linhas da tabela
        for i in range(self.row_count):
            self.master.grid_rowconfigure(i + 2, weight=1)

        # Remover apenas os botões de navegação, se existirem
        if hasattr(self, 'botao_anterior') and self.botao_anterior is not None:
            self.botao_anterior.destroy()
        if hasattr(self, 'botao_proxima') and self.botao_proxima is not None:
            self.botao_proxima.destroy()

        # Botões de navegação de página
        if self.pagina_atual > 1:
            self.botao_anterior = ctk.CTkButton(self.master, text="Anterior", command=self.pagina_anterior)
            self.botao_anterior.grid(row=self.row_count, column=1, padx=10, pady=10, sticky="w")

        if self.pagina_atual < self.total_paginas:
            self.botao_proxima = ctk.CTkButton(self.master, text="Próxima", command=self.proxima_pagina)
            self.botao_proxima.grid(row=self.row_count, column=4, padx=10, pady=10, sticky="e")

        # Label para mostrar a página atual
        self.label_pagina = ctk.CTkLabel(self.master, text=f"Página {self.pagina_atual} de {self.total_paginas}")
        self.label_pagina.grid(row=self.row_count, column=2, columnspan=2, padx=10, pady=10, sticky="ew")

    def pagina_anterior(self):
        if self.pagina_atual > 1:
            self.pagina_atual -= 1
            self.exibir_cadastros()

    def proxima_pagina(self):
        if self.pagina_atual < self.total_paginas:
            self.pagina_atual += 1
            self.exibir_cadastros()
