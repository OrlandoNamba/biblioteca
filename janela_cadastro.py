from PyQt5.QtWidgets import QLineEdit, QComboBox, QPushButton, QVBoxLayout, QWidget, QMessageBox
import sqlite3

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
        self.nome_input.setStyleSheet("color: #5E5E61;")  # Cor do texto

        self.autor_combo = QComboBox(self)
        self.autor_combo.setEditable(True)
        self.autor_combo.setStyleSheet("color: #5E5E61;")  # Cor do texto do combobox
        self.autor_combo.lineEdit().setPlaceholderText("Selecione ou digite o autor")

        self.editora_combo = QComboBox(self)
        self.editora_combo.setEditable(True)
        self.editora_combo.setStyleSheet("color: #5E5E61;")  # Cor do texto do combobox
        self.editora_combo.lineEdit().setPlaceholderText("Selecione ou digite a editora")

        self.isbn_input = QLineEdit(self)
        self.isbn_input.setPlaceholderText("Digite o ISBN do livro")
        self.isbn_input.setStyleSheet("color: #5E5E61;")  # Cor do texto

        self.paginas_input = QLineEdit(self)
        self.paginas_input.setPlaceholderText("Digite o número de páginas")
        self.paginas_input.setStyleSheet("color: #5E5E61;")  # Cor do texto

        self.genero_combo = QComboBox(self)
        self.genero_combo.setEditable(True)
        self.genero_combo.setStyleSheet("color: #5E5E61;")  # Cor do texto do combobox
        self.genero_combo.lineEdit().setPlaceholderText("Selecione ou digite o gênero")

        # Conectar os sinais
        self.autor_combo.lineEdit().textChanged.connect(lambda: self.atualizar_placeholder(self.autor_combo))
        self.autor_combo.lineEdit().editingFinished.connect(lambda: self.restore_placeholder(self.autor_combo))
        self.autor_combo.lineEdit().editingFinished.connect(lambda: self.adicionar_item_combo(self.autor_combo))

        self.editora_combo.lineEdit().textChanged.connect(lambda: self.atualizar_placeholder(self.editora_combo))
        self.editora_combo.lineEdit().editingFinished.connect(lambda: self.restore_placeholder(self.editora_combo))
        self.editora_combo.lineEdit().editingFinished.connect(lambda: self.adicionar_item_combo(self.editora_combo))

        self.genero_combo.lineEdit().textChanged.connect(lambda: self.atualizar_placeholder(self.genero_combo))
        self.genero_combo.lineEdit().editingFinished.connect(lambda: self.restore_placeholder(self.genero_combo))
        self.genero_combo.lineEdit().editingFinished.connect(lambda: self.adicionar_item_combo(self.genero_combo))

        # Botões
        self.cadastrar_button = QPushButton("Cadastrar", self)
        self.cadastrar_button.clicked.connect(self.cadastrar_livro)

        self.limpar_button = QPushButton("Limpar", self)
        self.limpar_button.clicked.connect(self.limpar_campos)

        self.exibir_button = QPushButton("Exibir Cadastros", self)

        # Adiciona os widgets ao layout
        layout.addWidget(self.nome_input)
        layout.addWidget(self.autor_combo)
        layout.addWidget(self.editora_combo)
        layout.addWidget(self.isbn_input)
        layout.addWidget(self.paginas_input)
        layout.addWidget(self.genero_combo)
        layout.addWidget(self.cadastrar_button)
        layout.addWidget(self.limpar_button)
        layout.addWidget(self.exibir_button)

        self.setLayout(layout)

    def eventFilter(self, source, event):
        if event.type() == 6:  # Focus In Event
            if source in (self.autor_combo.lineEdit(), self.editora_combo.lineEdit(), self.genero_combo.lineEdit()):
                source.parent().showPopup()  # Mostra o popup do combobox
        return super().eventFilter(source, event)

    def atualizar_placeholder(self, combo):
        # Define o texto do placeholder conforme o tipo de campo
        if combo.lineEdit().text().strip() == "":
            if combo == self.autor_combo:
                combo.lineEdit().setPlaceholderText("Selecione ou digite o autor")
            elif combo == self.editora_combo:
                combo.lineEdit().setPlaceholderText("Selecione ou digite a editora")
            elif combo == self.genero_combo:
                combo.lineEdit().setPlaceholderText("Selecione ou digite o gênero")
            else:
                combo.lineEdit().setPlaceholderText("Selecione ou digite tal coisa")  # Texto padrão para outros campos
        else:
            # Remove o texto de placeholder
            if combo.lineEdit().text() == "Selecione tal coisa":
                combo.lineEdit().setText("")  # Remove o texto de placeholder

    def restore_placeholder(self, combo):
        # Restaura o placeholder se o campo estiver vazio ao sair
        if combo.lineEdit().text().strip() == "":
            if combo == self.autor_combo:
                combo.lineEdit().setPlaceholderText("Selecione ou digite o autor")
            elif combo == self.editora_combo:
                combo.lineEdit().setPlaceholderText("Selecione ou digite a editora")
            elif combo == self.genero_combo:
                combo.lineEdit().setPlaceholderText("Selecione ou digite o gênero")
            else:
                combo.lineEdit().setPlaceholderText("Selecione ou digite tal coisa")  # Texto padrão para outros campos

    def adicionar_item_combo(self, combo):
        # Adiciona o item digitado ao combobox se não existir
        item = combo.lineEdit().text().strip()
        if item and item not in [combo.itemText(i) for i in range(combo.count())]:
            combo.addItem(item)

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
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Erro", f"Ocorreu um erro ao cadastrar o livro: {e}")

    def limpar_campos(self):
        self.nome_input.clear()
        self.autor_combo.lineEdit().setText("")  # Limpa o campo do combobox
        self.autor_combo.lineEdit().setPlaceholderText("Selecione ou digite o autor")  # Restaura o placeholder
        self.editora_combo.lineEdit().setText("")  # Limpa o campo do combobox
        self.editora_combo.lineEdit().setPlaceholderText("Selecione ou digite a editora")  # Restaura o placeholder
        self.isbn_input.clear()
        self.paginas_input.clear()
        self.genero_combo.lineEdit().setText("")  # Limpa o campo do combobox
        self.genero_combo.lineEdit().setPlaceholderText("Selecione ou digite o gênero")  # Restaura o placeholder
