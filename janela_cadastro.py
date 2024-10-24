import sqlite3
from PyQt5.QtWidgets import QLineEdit, QComboBox, QPushButton, QVBoxLayout, QWidget, QMessageBox

class JanelaCadastro(QWidget):
    def __init__(self):
        super().__init__()

        # Configurações da janela
        self.setWindowTitle("Cadastro de Livros")
        self.setGeometry(100, 100, 400, 300)

        # Layout
        layout = QVBoxLayout()

        # Campos de entrada
        self.nome_input = QLineEdit(self)
        self.nome_input.setPlaceholderText("Digite o nome do livro")

        self.autor_combo = QComboBox(self)
        self.autor_combo.setEditable(True)
        self.autor_combo.lineEdit().setPlaceholderText("Selecione ou digite o autor")
        self.autor_combo.lineEdit().focusInEvent = lambda event: self.autor_combo.showPopup()

        self.editora_combo = QComboBox(self)
        self.editora_combo.setEditable(True)
        self.editora_combo.lineEdit().setPlaceholderText("Selecione ou digite a editora")
        self.editora_combo.lineEdit().focusInEvent = lambda event: self.editora_combo.showPopup()

        self.isbn_input = QLineEdit(self)
        self.isbn_input.setPlaceholderText("Digite o ISBN do livro")

        self.paginas_input = QLineEdit(self)
        self.paginas_input.setPlaceholderText("Digite o número de páginas")

        self.genero_combo = QComboBox(self)
        self.genero_combo.setEditable(True)
        self.genero_combo.lineEdit().setPlaceholderText("Selecione ou digite o gênero")
        self.genero_combo.lineEdit().focusInEvent = lambda event: self.genero_combo.showPopup()

        # Botões
        self.cadastrar_button = QPushButton("Cadastrar", self)
        self.cadastrar_button.clicked.connect(self.cadastrar_livro)

        self.limpar_button = QPushButton("Limpar", self)
        self.limpar_button.clicked.connect(self.limpar_campos)

        # Adiciona os widgets ao layout
        layout.addWidget(self.nome_input)
        layout.addWidget(self.autor_combo)
        layout.addWidget(self.editora_combo)
        layout.addWidget(self.isbn_input)
        layout.addWidget(self.paginas_input)
        layout.addWidget(self.genero_combo)
        layout.addWidget(self.cadastrar_button)
        layout.addWidget(self.limpar_button)

        self.setLayout(layout)

        # Carregar os dados no QComboBox ao iniciar
        self.carregar_dados_combo()

    def carregar_dados_combo(self):
        """Carrega os autores, editoras e gêneros já cadastrados no banco de dados."""
        try:
            conn = sqlite3.connect('biblioteca.db')
            cursor = conn.cursor()

            # Carregar autores
            autores = cursor.execute("SELECT DISTINCT autor FROM livros").fetchall()
            self.autor_combo.clear()  # Limpa itens antes de recarregar
            self.autor_combo.addItem("")  # Adiciona item vazio para mostrar o placeholder
            for autor in autores:
                self.autor_combo.addItem(autor[0])

            # Carregar editoras
            editoras = cursor.execute("SELECT DISTINCT editora FROM livros").fetchall()
            self.editora_combo.clear()  # Limpa itens antes de recarregar
            self.editora_combo.addItem("")  # Adiciona item vazio para mostrar o placeholder
            for editora in editoras:
                self.editora_combo.addItem(editora[0])

            # Carregar gêneros
            generos = cursor.execute("SELECT DISTINCT genero FROM livros").fetchall()
            self.genero_combo.clear()  # Limpa itens antes de recarregar
            self.genero_combo.addItem("")  # Adiciona item vazio para mostrar o placeholder
            for genero in generos:
                self.genero_combo.addItem(genero[0])

            conn.close()
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Erro", f"Ocorreu um erro ao carregar os dados: {e}")

    def cadastrar_livro(self):
        # Coleta os dados dos campos
        nome = self.nome_input.text().strip()
        autor = self.autor_combo.currentText().strip() or self.autor_combo.lineEdit().text().strip()
        editora = self.editora_combo.currentText().strip() or self.editora_combo.lineEdit().text().strip()
        isbn = self.isbn_input.text().strip()
        paginas = self.paginas_input.text().strip()
        genero = self.genero_combo.currentText().strip() or self.genero_combo.lineEdit().text().strip()

        # Validação dos campos
        if not nome or not autor or not editora or not isbn or not paginas or not genero:
            QMessageBox.warning(self, "Erro", "Por favor, preencha todos os campos.")
            return

        # Lógica de inserção no banco de dados
        try:
            conn = sqlite3.connect('biblioteca.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO livros (nome, autor, editora, isbn, paginas, genero) VALUES (?, ?, ?, ?, ?, ?)", 
                           (nome, autor, editora, isbn, paginas, genero))
            conn.commit()
            conn.close()
            QMessageBox.information(self, "Sucesso", "Livro cadastrado com sucesso!")
            self.limpar_campos()  # Limpa os campos após o cadastro
            self.carregar_dados_combo()  # Atualiza os dados nos comboboxes
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Erro", f"Ocorreu um erro ao cadastrar o livro: {e}")

    def limpar_campos(self):
        self.nome_input.clear()
        self.autor_combo.lineEdit().clear()  # Limpa o campo do autor
        self.editora_combo.lineEdit().clear()  # Limpa o campo da editora
        self.isbn_input.clear()
        self.paginas_input.clear()
        self.genero_combo.lineEdit().clear()  # Limpa o campo do gênero
