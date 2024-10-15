import sqlite3
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout, QTableWidget, QTableWidgetItem

class ListaCadastros(QWidget):
    def __init__(self, voltar_callback):
        super().__init__()
        self.voltar_callback = voltar_callback
        self.pagina_atual = 1
        self.livros_por_pagina = 15
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Botão de Voltar
        botao_voltar = QPushButton("Voltar", self)
        botao_voltar.clicked.connect(self.voltar_callback)
        layout.addWidget(botao_voltar)

        # Título
        layout.addWidget(QLabel("Lista de Cadastros"))

        # Tabela para exibir os registros
        self.tabela = QTableWidget(self)
        self.tabela.setColumnCount(7)
        self.tabela.setHorizontalHeaderLabels(["ID", "Nome", "Autor", "Editora", "Páginas", "ISBN", "Gênero"])
        layout.addWidget(self.tabela)

        # Botões de navegação
        self.botao_anterior = QPushButton("Anterior", self)
        self.botao_anterior.clicked.connect(self.pagina_anterior)
        self.botao_proxima = QPushButton("Próxima", self)
        self.botao_proxima.clicked.connect(self.proxima_pagina)

        nav_layout = QHBoxLayout()
        nav_layout.addWidget(self.botao_anterior)
        nav_layout.addWidget(self.botao_proxima)

        layout.addLayout(nav_layout)

        self.setLayout(layout)
        self.exibir_cadastros()

    def exibir_cadastros(self):
        conn = sqlite3.connect("cadastros.db")
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM livros")
        total_registros = cursor.fetchone()[0]

        total_paginas = (total_registros // self.livros_por_pagina) + (1 if total_registros % self.livros_por_pagina > 0 else 0)

        offset = (self.pagina_atual - 1) * self.livros_por_pagina
        cursor.execute("SELECT * FROM livros LIMIT ? OFFSET ?", (self.livros_por_pagina, offset))
        registros = cursor.fetchall()
        conn.close()

        self.tabela.setRowCount(len(registros))

        for i, registro in enumerate(registros):
            for j, valor in enumerate(registro):
                self.tabela.setItem(i, j, QTableWidgetItem(str(valor)))

        # Atualizar visibilidade dos botões de navegação
        self.botao_anterior.setEnabled(self.pagina_atual > 1)
        self.botao_proxima.setEnabled(self.pagina_atual < total_paginas)

    def pagina_anterior(self):
        if self.pagina_atual > 1:
            self.pagina_atual -= 1
            self.exibir_cadastros()

    def proxima_pagina(self):
        self.pagina_atual += 1
        self.exibir_cadastros()
