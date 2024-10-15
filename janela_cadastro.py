import sqlite3
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QLineEdit, QPushButton, QMessageBox
from PyQt5 import QtWidgets, QtGui, QtCore

class JanelaCadastro(QWidget):
    def __init__(self, show_lista_callback):
        super().__init__()
        self.show_lista_callback = show_lista_callback
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)  # Espaçamento entre widgets
        layout.setContentsMargins(20, 20, 20, 20)  # Margens ao redor do layout

        # Título
        titulo = QtWidgets.QLabel("Cadastro de Livros", self)
        titulo.setFont(QtGui.QFont("Arial", 24, QtGui.QFont.Bold))
        titulo.setAlignment(QtCore.Qt.AlignCenter)
        titulo.setStyleSheet("color: #512D7B;")  # Cor do título
        layout.addWidget(titulo)

        # Campos de entrada
        self.entrada_nomeLivro = self.criar_campo("Nome do Livro:", layout)
        self.entrada_autor = self.criar_campo("Autor:", layout)
        self.entrada_editora = self.criar_campo("Editora:", layout)
        self.entrada_numeroPaginas = self.criar_campo("Número de Páginas:", layout)
        self.entrada_isbn = self.criar_campo("ISBN:", layout)

        # Campo de Gênero
        self.combobox_genero = self.criar_campo_genero("Gênero:", layout)

        # Botões
        botao_cadastrar = QPushButton("Cadastrar", self)
        botao_cadastrar.clicked.connect(self.cadastrar)
        botao_cadastrar.setStyleSheet("background-color: #512D7B; color: white; border-radius: 5px; padding: 10px;")
        botao_cadastrar.setFixedSize(150, 40)  # Ajusta o tamanho dos botões (largura, altura)
        
        botao_lista = QPushButton("Ver Cadastros", self)
        botao_lista.clicked.connect(self.show_lista_callback)
        botao_lista.setStyleSheet("background-color: #512D7B; color: white; border-radius: 5px; padding: 10px;")
        botao_lista.setFixedSize(150, 40)  # Ajusta o tamanho dos botões (largura, altura)

        # Adicionando os botões dentro de um layout horizontal para centralizar
        botao_layout = QtWidgets.QHBoxLayout()

        # Adicionando "spacers" para centralizar os botões
        botao_layout.addStretch()  # Espaço vazio à esquerda
        botao_layout.addWidget(botao_cadastrar)
        botao_layout.addWidget(botao_lista)
        botao_layout.addStretch()  # Espaço vazio à direita

        # Adiciona o layout dos botões ao layout principal vertical
        layout.addLayout(botao_layout)

        self.setLayout(layout)
        self.atualizar_generos_combobox()

    def criar_campo(self, label_text, layout):
        """Cria um campo de entrada com rótulo e adiciona ao layout fornecido."""
        label = QLabel(label_text)
        label.setStyleSheet("color: #5E5E61;")  # Cor do rótulo
        entrada = QLineEdit(self)
        entrada.setPlaceholderText(f"Digite o {label_text.lower()}")
        entrada.setStyleSheet("background-color: #FFFFFF; border: 1px solid #B96EC8; border-radius: 5px; padding: 5px; font-size: 14px;")  # Cor do fundo alterada
        
        layout.addWidget(label)
        layout.addWidget(entrada)
        return entrada

    def criar_campo_genero(self, label_text, layout):
        """Cria o campo de seleção de gênero com rótulo e adiciona ao layout fornecido."""
        label = QLabel(label_text)
        label.setStyleSheet("color: #5E5E61;")  # Cor do rótulo
        combo_box = QComboBox(self)
        combo_box.setStyleSheet("background-color: #FFFFFF; border: 1px solid #B96EC8; border-radius: 5px; padding: 5px; font-size: 14px;")  # Cor do fundo alterada
        
        layout.addWidget(label)
        layout.addWidget(combo_box)
        return combo_box

    def carregar_generos(self):
        conn = sqlite3.connect("cadastros.db")
        cursor = conn.cursor()
        cursor.execute("SELECT genero FROM generos")
        generos = [row[0] for row in cursor.fetchall()]
        conn.close()
        return generos

    def cadastrar(self):
        nomeLivro = self.entrada_nomeLivro.text()
        autor = self.entrada_autor.text()
        editora = self.entrada_editora.text()
        numeroPaginas = self.entrada_numeroPaginas.text()
        isbn = self.entrada_isbn.text()
        genero = self.combobox_genero.currentText()

        if nomeLivro == "" or autor == "" or editora == "" or numeroPaginas == "" or isbn == "" or genero == "":
            QMessageBox.warning(self, "Atenção", "Todos os campos devem ser preenchidos!")
        else:
            conn = sqlite3.connect("cadastros.db")
            cursor = conn.cursor()
            cursor.execute("INSERT OR IGNORE INTO generos (genero) VALUES (?)", (genero,))
            cursor.execute("INSERT INTO livros (nomeLivro, autor, editora, numeroPaginas, isbn, genero) VALUES (?, ?, ?, ?, ?, ?)",
                           (nomeLivro, autor, editora, numeroPaginas, isbn, genero))
            conn.commit()
            conn.close()

            self.atualizar_generos_combobox()
            QMessageBox.information(self, "Sucesso", "Cadastro realizado com sucesso!")
            self.limpar_campos()

    def limpar_campos(self):
        self.entrada_nomeLivro.clear()
        self.entrada_autor.clear()
        self.entrada_editora.clear()
        self.entrada_numeroPaginas.clear()
        self.entrada_isbn.clear()
        self.combobox_genero.setCurrentIndex(-1)

    def atualizar_generos_combobox(self):
        generos = self.carregar_generos()
        self.combobox_genero.clear()
        self.combobox_genero.addItem("Selecione o gênero")  # Adiciona a opção inicial
        self.combobox_genero.addItems(generos)
        self.combobox_genero.setCurrentIndex(0)  # Define a opção "Selecione o gênero" como a padrão

