import sqlite3
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout, QTableWidget, QTableWidgetItem
from PyQt5 import QtGui, QtCore, QtWidgets

class ListaCadastros(QWidget):
    def __init__(self, voltar_callback):
        super().__init__()
        self.voltar_callback = voltar_callback
        self.pagina_atual = 1
        self.livros_por_pagina = 15
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        self.setStyleSheet("background-color: #F4EFEC;")  # Cor de fundo da janela

        # Layout para o botão de Voltar no canto superior esquerdo
        voltar_layout = QHBoxLayout()
        voltar_layout.setAlignment(QtCore.Qt.AlignLeft)  # Alinhar à esquerda

        # Botão de Voltar
        botao_voltar = QPushButton("Voltar", self)
        botao_voltar.setFixedSize(80, 30)  # Tamanho fixo para o botão
        botao_voltar.clicked.connect(self.voltar_callback)
        botao_voltar.setStyleSheet("""
            QPushButton {
                background-color: #512D7B;
                color: white;
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #B96EC8;
            }
        """)
        voltar_layout.addWidget(botao_voltar)

        layout.addLayout(voltar_layout)

        # Título
        titulo = QLabel("Lista de Cadastros", self)
        titulo.setFont(QtGui.QFont("Arial", 24, QtGui.QFont.Bold))
        titulo.setStyleSheet("color: #512D7B;")
        titulo.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(titulo)

        # Tabela para exibir os registros
        self.tabela = QTableWidget(self)
        self.tabela.setColumnCount(7)  # Agora com 7 colunas, incluindo o ISBN
        self.tabela.setHorizontalHeaderLabels(["ID", "Nome", "Autor", "Editora", "Páginas", "ISBN", "Gênero"])
        self.tabela.verticalHeader().setVisible(False)  # Remover a numeração das linhas
        self.tabela.setStyleSheet("""
            QTableWidget {
                background-color: #FFFFFF;
                color: #5E5E61;
                border: 1px solid #B96EC8;
            }
            QHeaderView::section {
                background-color: #512D7B;
                color: white;
                padding: 5px;
            }
            QTableWidget::item {
                border: 1px solid #B96EC8;
                padding: 5px;
            }
        """)
        layout.addWidget(self.tabela)

        # Configuração da responsividade
        header = self.tabela.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)  # Redimensionar automaticamente as colunas

        # Botões de navegação
        self.botao_anterior = QPushButton("Anterior", self)
        self.botao_anterior.clicked.connect(self.pagina_anterior)
        self.botao_proxima = QPushButton("Próxima", self)
        self.botao_proxima.clicked.connect(self.proxima_pagina)

        for botao in [self.botao_anterior, self.botao_proxima]:
            botao.setStyleSheet("""
                QPushButton {
                    background-color: #512D7B;
                    color: white;
                    border-radius: 5px;
                    padding: 10px;
                }
                QPushButton:hover {
                    background-color: #B96EC8;
                }
            """)

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
        cursor.execute("SELECT id, nomeLivro, autor, editora, numeroPaginas, isbn, genero FROM livros LIMIT ? OFFSET ?", (self.livros_por_pagina, offset))
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
