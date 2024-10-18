from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel,
    QHBoxLayout, QTableWidget, QTableWidgetItem,
    QDialog, QLineEdit, QMessageBox
)
from PyQt5 import QtGui, QtCore, QtWidgets
import sqlite3

class ListaCadastros(QWidget):
    def __init__(self, voltar_callback):
        super().__init__()
        self.voltar_callback = voltar_callback
        self.pagina_atual = 1
        self.livros_por_pagina = 15
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(50, 20, 50, 20)

        # Layout para o botão de Voltar e Editar e o campo de pesquisa
        button_layout = QHBoxLayout()
        button_layout.setAlignment(QtCore.Qt.AlignRight)

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

        # Espaço entre os botões e o campo de pesquisa
        button_layout.addStretch()

        # Campo de pesquisa modernizado
        self.campo_pesquisa = QLineEdit(self)
        self.campo_pesquisa.setPlaceholderText("Pesquisar...")
        self.campo_pesquisa.setFixedWidth(200)  # Define a largura do campo de pesquisa
        self.campo_pesquisa.setStyleSheet(""" 
            QLineEdit {
                padding: 5px;
                border: 2px solid #B96EC8; /* Cor da borda */
                border-radius: 5px; /* Bordas arredondadas */
            }
            QLineEdit:focus {
                border: 2px solid #512D7B; /* Cor da borda ao focar */
            }
        """)
        self.campo_pesquisa.textChanged.connect(self.pesquisar)
        button_layout.addWidget(self.campo_pesquisa)

        layout.addLayout(button_layout)

        # Título
        titulo = QLabel("Lista de Livros", self)
        titulo.setFont(QtGui.QFont("Arial", 16, QtGui.QFont.Bold))
        titulo.setStyleSheet("color: #512D7B;")
        titulo.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(titulo)

        # Tabela para exibir os registros
        self.tabela = QTableWidget(self)
        self.tabela.setColumnCount(7)
        self.tabela.setHorizontalHeaderLabels(["ID", "Nome", "Autor", "Editora", "Páginas", "ISBN", "Gênero"])
        self.tabela.verticalHeader().setVisible(False)
        self.tabela.setStyleSheet(""" 
            QTableWidget {
                background-color: #FFFFFF; /* Cor de fundo da tabela */
                color: #5E5E61; /* Cor do texto */
                border: none; /* Sem bordas */
                border-radius: 10px; /* Bordas arredondadas */
                padding: 5px; /* Espaçamento interno */
                margin: 10px 0; /* Margens */
            }
            QHeaderView::section {
                background-color: #512D7B; /* Cor de fundo do cabeçalho */
                color: white; /* Cor do texto do cabeçalho */
                padding: 2px; /* Espaçamento interno do cabeçalho */
                font-weight: bold; /* Negrito */
                border-radius: 8px; /* Bordas arredondadas do cabeçalho */
            }
            QTableWidget::item {
                border: none; /* Sem bordas nos itens */
                background-color: #F4EFEC; /* Cor de fundo dos itens */
            }
            QTableWidget::item:selected {
                background-color: #DDB7AC; /* Cor de fundo dos itens selecionados */
                color: #5E5E61; /* Cor do texto dos itens selecionados */
            }
            QTableWidget::item:focus {
                outline: none; /* Sem contorno quando focado */
            }
            QTableWidget::item:selected:focus {
                background-color: #DDB7AC; /* Cor de fundo quando um item selecionado está focado */
            }
        """)

        layout.addWidget(self.tabela)

        # Ajuste de altura baseado no conteúdo
        header = self.tabela.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        # Conexão do sinal para selecionar todos os dados do livro ao clicar em uma célula
        self.tabela.itemClicked.connect(self.selecionar_livro)

        # Botões de navegação (definidos após a tabela)
        self.botao_anterior = QPushButton("Anterior", self)
        self.botao_anterior.setFixedSize(80, 30)
        self.botao_anterior.clicked.connect(self.pagina_anterior)
        self.botao_proxima = QPushButton("Próxima", self)
        self.botao_proxima.setFixedSize(80, 30)
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
                QPushButton:disabled {
                    background-color: #999B85; /* Cor cinza para o botão desativado */
                    color: #FFFFFF; /* Cor do texto do botão desativado */
                }
            """)

        # Layout de navegação abaixo da tabela
        nav_layout = QHBoxLayout()
        nav_layout.setAlignment(QtCore.Qt.AlignCenter)
        nav_layout.addWidget(self.botao_anterior)
        nav_layout.addWidget(self.botao_proxima)

        # Adiciona o layout de navegação ao layout principal
        layout.addLayout(nav_layout)

        # Agora chamamos exibir_cadastros após a criação dos botões
        self.exibir_cadastros()

        self.setLayout(layout)

    def selecionar_livro(self, item):
        row = item.row()
        for column in range(self.tabela.columnCount()):
            self.tabela.item(row, column).setSelected(True)

    def exibir_cadastros(self):
        conn = sqlite3.connect("cadastros.db")
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM livros")
        total_registros = cursor.fetchone()[0]

        offset = (self.pagina_atual - 1) * self.livros_por_pagina
        cursor.execute("SELECT id, nomeLivro, autor, editora, numeroPaginas, isbn, genero FROM livros LIMIT ? OFFSET ?",
                       (self.livros_por_pagina, offset))
        registros = cursor.fetchall()
        conn.close()

        self.tabela.setRowCount(len(registros))

        for i, registro in enumerate(registros):
            for j, valor in enumerate(registro):
                item = QTableWidgetItem(str(valor))
                item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                self.tabela.setItem(i, j, item)

        row_height = 40
        header_height = self.tabela.horizontalHeader().height()
        total_table_height = min(len(registros), self.livros_por_pagina) * row_height + header_height
        self.tabela.setFixedHeight(total_table_height)

        self.botao_anterior.setEnabled(self.pagina_atual > 1)
        self.botao_proxima.setEnabled(len(registros) == self.livros_por_pagina)

    def pesquisar(self):
        pesquisa = self.campo_pesquisa.text().lower()
        conn = sqlite3.connect("cadastros.db")
        cursor = conn.cursor()
        
        if pesquisa:  # Se houver texto na pesquisa
            cursor.execute("SELECT id, nomeLivro, autor, editora, numeroPaginas, isbn, genero FROM livros WHERE nomeLivro LIKE ? OR autor LIKE ? OR editora LIKE ?",
                        (f'%{pesquisa}%', f'%{pesquisa}%', f'%{pesquisa}%'))
        else:  # Se o campo de pesquisa estiver vazio, exibe todos os cadastros
            cursor.execute("SELECT id, nomeLivro, autor, editora, numeroPaginas, isbn, genero FROM livros")

        registros = cursor.fetchall()
        conn.close()

        self.tabela.setRowCount(len(registros))

        for i, registro in enumerate(registros):
            for j, valor in enumerate(registro):
                item = QTableWidgetItem(str(valor))
                item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                self.tabela.setItem(i, j, item)

        self.botao_anterior.setEnabled(False)
        self.botao_proxima.setEnabled(False)

        # Desabilita os botões de navegação se não houver registros
        if not registros:
            self.botao_anterior.setDisabled(True)
            self.botao_proxima.setDisabled(True)
            self.botao_anterior.setStyleSheet("background-color: #999B85; color: #FFFFFF;")  # Cinza
            self.botao_proxima.setStyleSheet("background-color: #999B85; color: #FFFFFF;")  # Cinza
        else:
            self.botao_anterior.setEnabled(self.pagina_atual > 1)
            self.botao_proxima.setEnabled(len(registros) == self.livros_por_pagina)

    def pagina_anterior(self):
        if self.pagina_atual > 1:
            self.pagina_atual -= 1
            self.exibir_cadastros()

    def proxima_pagina(self):
        self.pagina_atual += 1
        self.exibir_cadastros()

    def abrir_tela_edicao(self):
        # Lógica para abrir a tela de edição
        row = self.tabela.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Aviso", "Selecione um livro para editar.")
            return
        livro_id = self.tabela.item(row, 0).text()
        dialog = QDialog(self)
        dialog.setWindowTitle("Edição de Livro")
        dialog.setModal(True)

        layout = QVBoxLayout()
        self.campo_nome = QLineEdit(dialog)
        self.campo_autor = QLineEdit(dialog)
        self.campo_editora = QLineEdit(dialog)
        self.campo_paginas = QLineEdit(dialog)
        self.campo_isbn = QLineEdit(dialog)
        self.campo_genero = QLineEdit(dialog)

        layout.addWidget(QLabel("Nome:", dialog))
        layout.addWidget(self.campo_nome)
        layout.addWidget(QLabel("Autor:", dialog))
        layout.addWidget(self.campo_autor)
        layout.addWidget(QLabel("Editora:", dialog))
        layout.addWidget(self.campo_editora)
        layout.addWidget(QLabel("Páginas:", dialog))
        layout.addWidget(self.campo_paginas)
        layout.addWidget(QLabel("ISBN:", dialog))
        layout.addWidget(self.campo_isbn)
        layout.addWidget(QLabel("Gênero:", dialog))
        layout.addWidget(self.campo_genero)

        botao_salvar = QPushButton("Salvar", dialog)
        botao_salvar.clicked.connect(lambda: self.salvar_edicao(livro_id, dialog))
        layout.addWidget(botao_salvar)

        dialog.setLayout(layout)

        # Carrega os dados do livro na tela de edição
        self.carregar_dados(livro_id)

        dialog.exec_()

    def carregar_dados(self, livro_id):
        conn = sqlite3.connect("cadastros.db")
        cursor = conn.cursor()
        cursor.execute("SELECT nomeLivro, autor, editora, numeroPaginas, isbn, genero FROM livros WHERE id = ?", (livro_id,))
        dados = cursor.fetchone()
        conn.close()

        if dados:
            self.campo_nome.setText(dados[0])
            self.campo_autor.setText(dados[1])
            self.campo_editora.setText(dados[2])
            self.campo_paginas.setText(str(dados[3]))
            self.campo_isbn.setText(dados[4])
            self.campo_genero.setText(dados[5])

    def salvar_edicao(self, livro_id, dialog):
        nome = self.campo_nome.text()
        autor = self.campo_autor.text()
        editora = self.campo_editora.text()
        paginas = self.campo_paginas.text()
        isbn = self.campo_isbn.text()
        genero = self.campo_genero.text()

        conn = sqlite3.connect("cadastros.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE livros SET nomeLivro = ?, autor = ?, editora = ?, numeroPaginas = ?, isbn = ?, genero = ? WHERE id = ?",
                       (nome, autor, editora, paginas, isbn, genero, livro_id))
        conn.commit()
        conn.close()

        QMessageBox.information(self, "Sucesso", "Livro editado com sucesso.")
        dialog.accept()
        self.exibir_cadastros()
