import sqlite3
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel,
    QHBoxLayout, QTableWidget, QTableWidgetItem,
    QDialog, QLineEdit, QMessageBox
)
from PyQt5 import QtGui, QtCore
from PyQt5 import QtWidgets


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
        self.setStyleSheet("background-color: #F4EFEC;")

        # Layout para o botão de Voltar e Editar no canto superior esquerdo
        button_layout = QHBoxLayout()
        button_layout.setAlignment(QtCore.Qt.AlignLeft)

        # Botão de Voltar
        botao_voltar = QPushButton("Voltar", self)
        botao_voltar.setFixedSize(80, 30)
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
        button_layout.addWidget(botao_voltar)

        # Botão de Editar
        botao_editar = QPushButton("Editar", self)
        botao_editar.setFixedSize(80, 30)
        botao_editar.clicked.connect(self.abrir_tela_edicao)
        botao_editar.setStyleSheet(""" 
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
        button_layout.addWidget(botao_editar)

        layout.addLayout(button_layout)

        # Título
        titulo = QLabel("Lista de Cadastros", self)
        titulo.setFont(QtGui.QFont("Arial", 24, QtGui.QFont.Bold))
        titulo.setStyleSheet("color: #512D7B;")
        titulo.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(titulo)

        # Tabela para exibir os registros
        self.tabela = QTableWidget(self)
        self.tabela.setColumnCount(7)
        self.tabela.setHorizontalHeaderLabels(["ID", "Nome", "Autor", "Editora", "Páginas", "ISBN", "Gênero"])
        self.tabela.verticalHeader().setVisible(False)

        # Estilo da Tabela
        self.tabela.setStyleSheet("""
            QTableWidget {
                background-color: #FFFFFF;
                color: #5E5E61;
                border: 1px solid #B96EC8;
            }
            QHeaderView::section {
                background-color: #512D7B; /* Cor de fundo do cabeçalho */
                color: white; /* Cor do texto do cabeçalho */
                padding: 5px;
                border: 1px solid #B96EC8; /* Borda do cabeçalho */
            }
            QTableWidget::item {
                border: 1px solid #B96EC8;
                padding: 5px;
            }
            QTableWidget::item:selected {
                background-color: #DDB7AC; /* Cor de fundo quando o item é selecionado */
                color: #5E5E61; /* Cor do texto quando o item é selecionado */
            }
            QTableWidget::item:focus {
                outline: none; /* Remove a borda de foco padrão */
            }
        """)

        layout.addWidget(self.tabela)

        header = self.tabela.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        # Conectar sinal de clique na tabela
        self.tabela.itemClicked.connect(self.selecionar_linha)

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
                item = QTableWidgetItem(str(valor))
                item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)  # Torna o item somente leitura
                self.tabela.setItem(i, j, item)

        # Atualizar visibilidade dos botões de navegação
        self.botao_anterior.setEnabled(self.pagina_atual > 1)
        self.botao_proxima.setEnabled(self.pagina_atual < total_paginas)

    def selecionar_linha(self, item):
        linha = item.row()
        self.tabela.selectRow(linha)  # Seleciona toda a linha

    def pagina_anterior(self):
        if self.pagina_atual > 1:
            self.pagina_atual -= 1
            self.exibir_cadastros()

    def proxima_pagina(self):
        self.pagina_atual += 1
        self.exibir_cadastros()

    def abrir_tela_edicao(self):
        row = self.tabela.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Seleção Inválida", "Por favor, selecione um livro para editar.")
            return

        id_livro = self.tabela.item(row, 0).text()
        nome = self.tabela.item(row, 1).text()
        autor = self.tabela.item(row, 2).text()
        editora = self.tabela.item(row, 3).text()
        paginas = self.tabela.item(row, 4).text()
        isbn = self.tabela.item(row, 5).text()
        genero = self.tabela.item(row, 6).text()

        self.edicao_dialog = EdicaoLivroDialog(id_livro, nome, autor, editora, paginas, isbn, genero, self)
        self.edicao_dialog.exec_()

class EdicaoLivroDialog(QDialog):
    def __init__(self, id_livro, nome, autor, editora, paginas, isbn, genero, parent=None):
        super().__init__(parent)
        self.id_livro = id_livro
        self.initUI(nome, autor, editora, paginas, isbn, genero)

    def initUI(self, nome, autor, editora, paginas, isbn, genero):
        self.setWindowTitle("Editar Livro")
        layout = QVBoxLayout()

        # Campos de edição
        self.nome_input = QLineEdit(nome, self)
        self.autor_input = QLineEdit(autor, self)
        self.editora_input = QLineEdit(editora, self)
        self.paginas_input = QLineEdit(paginas, self)
        self.isbn_input = QLineEdit(isbn, self)
        self.genero_input = QLineEdit(genero, self)

        layout.addWidget(QLabel("Nome do Livro:"))
        layout.addWidget(self.nome_input)
        layout.addWidget(QLabel("Autor:"))
        layout.addWidget(self.autor_input)
        layout.addWidget(QLabel("Editora:"))
        layout.addWidget(self.editora_input)
        layout.addWidget(QLabel("Número de Páginas:"))
        layout.addWidget(self.paginas_input)
        layout.addWidget(QLabel("ISBN:"))
        layout.addWidget(self.isbn_input)
        layout.addWidget(QLabel("Gênero:"))
        layout.addWidget(self.genero_input)

        # Botões de Salvar e Cancelar
        botao_salvar = QPushButton("Salvar", self)
        botao_salvar.clicked.connect(self.salvar)
        botao_cancelar = QPushButton("Cancelar", self)
        botao_cancelar.clicked.connect(self.close)

        layout.addWidget(botao_salvar)
        layout.addWidget(botao_cancelar)

        self.setLayout(layout)

    def salvar(self):
        # Atualizar o registro no banco de dados
        conn = sqlite3.connect("cadastros.db")
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE livros 
            SET nomeLivro = ?, autor = ?, editora = ?, numeroPaginas = ?, isbn = ?, genero = ? 
            WHERE id = ?
        """, (self.nome_input.text(), self.autor_input.text(), self.editora_input.text(),
              self.paginas_input.text(), self.isbn_input.text(), self.genero_input.text(), self.id_livro))
        conn.commit()
        conn.close()

        QMessageBox.information(self, "Sucesso", "Livro editado com sucesso!")
        self.close()
