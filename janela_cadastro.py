import sqlite3
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QComboBox, QStackedWidget, QSizePolicy, QMessageBox, QLabel
from PyQt5.QtCore import Qt

from lista_cadastros import ListaCadastros

class JanelaCadastro(QWidget):
    def __init__(self):
        super().__init__()

        # Configurações da janela
        self.setWindowTitle("Cadastro de Livros")
        self.setGeometry(100, 100, 400, 300)

        # Layout principal
        self.layout_principal = QVBoxLayout()

        # Cria um widget empilhado para alternar entre telas
        self.stacked_widget = QStackedWidget(self)

        # Tela de cadastro
        self.cadastro_widget = self.criar_tela_cadastro()
        self.stacked_widget.addWidget(self.cadastro_widget)

        # Tela de lista de cadastros
        self.lista_widget = ListaCadastros()
        self.stacked_widget.addWidget(self.lista_widget)

        # Adiciona o QStackedWidget ao layout principal
        self.layout_principal.addWidget(self.stacked_widget)

        self.setLayout(self.layout_principal)

    def criar_tela_cadastro(self):
        """Cria a interface de cadastro."""
        layout = QVBoxLayout()

        # Título da janela
        self.titulo = QLabel("Cadastrar Livros", self)
        self.titulo.setStyleSheet("font-size: 24px; font-weight: bold;")  # Estiliza o título
        self.titulo.setAlignment(Qt.AlignCenter)  # Centraliza o título

        # Campos de entrada
        self.nome_input = QLineEdit(self)
        self.nome_input.setPlaceholderText("Digite o nome do livro")
        self.nome_input.setMinimumSize(200, 30)  # Tamanho mínimo
        self.nome_input.setMaximumSize(400, 30)  # Tamanho máximo

        self.autor_combo = QComboBox(self)
        self.autor_combo.setEditable(True)
        self.autor_combo.lineEdit().setPlaceholderText("Selecione ou digite o autor")
        self.autor_combo.setMinimumSize(200, 30)  # Tamanho mínimo
        self.autor_combo.setMaximumSize(400, 30)  # Tamanho máximo

        self.editora_combo = QComboBox(self)
        self.editora_combo.setEditable(True)
        self.editora_combo.lineEdit().setPlaceholderText("Selecione ou digite a editora")
        self.editora_combo.setMinimumSize(200, 30)  # Tamanho mínimo
        self.editora_combo.setMaximumSize(400, 30)  # Tamanho máximo

        self.isbn_input = QLineEdit(self)
        self.isbn_input.setPlaceholderText("Digite o ISBN do livro")
        self.isbn_input.setMinimumSize(200, 30)  # Tamanho mínimo
        self.isbn_input.setMaximumSize(400, 30)  # Tamanho máximo

        self.paginas_input = QLineEdit(self)
        self.paginas_input.setPlaceholderText("Digite o número de páginas")
        self.paginas_input.setMinimumSize(200, 30)  # Tamanho mínimo
        self.paginas_input.setMaximumSize(400, 30)  # Tamanho máximo

        self.genero_combo = QComboBox(self)
        self.genero_combo.setEditable(True)
        self.genero_combo.lineEdit().setPlaceholderText("Selecione ou digite o gênero")
        self.genero_combo.setMinimumSize(200, 30)  # Tamanho mínimo
        self.genero_combo.setMaximumSize(400, 30)  # Tamanho máximo


        # Botões
        self.limpar_button = QPushButton("Limpar", self)
        self.limpar_button.setMinimumSize(100, 30)  # Tamanho mínimo
        self.limpar_button.setMaximumSize(150, 30)  # Tamanho máximo

        self.cadastrar_button = QPushButton("Cadastrar", self)
        self.cadastrar_button.setMinimumSize(100, 30)  # Tamanho mínimo
        self.cadastrar_button.setMaximumSize(150, 30)  # Tamanho máximo

        self.exibir_button = QPushButton("Exibir Cadastros", self)
        self.exibir_button.setMinimumSize(100, 30)  # Tamanho mínimo
        self.exibir_button.setMaximumSize(250, 100)  # Tamanho máximo


        # Layout para os botões
        botoes_layout = QHBoxLayout()
        botoes_layout.addWidget(self.limpar_button)
        botoes_layout.addStretch()  # Espaço para empurrar os botões para o centro
        botoes_layout.addWidget(self.cadastrar_button)
        botoes_layout.addStretch()  # Espaço entre o botão cadastrar e exibir
        botoes_layout.addWidget(self.exibir_button)

        # Adiciona o título e os widgets ao layout
        layout.addWidget(self.titulo)  # Adiciona o título ao layout
        layout.addWidget(self.nome_input)
        layout.addWidget(self.autor_combo)
        layout.addWidget(self.editora_combo)
        layout.addWidget(self.isbn_input)
        layout.addWidget(self.paginas_input)
        layout.addWidget(self.genero_combo)
        layout.addLayout(botoes_layout)  # Adiciona o layout dos botões

        # Cria um widget para a tela de cadastro e define seu layout
        cadastro_widget = QWidget()
        cadastro_widget.setLayout(layout)

        # Carregar os dados no QComboBox ao iniciar
        self.carregar_dados_combo()

        return cadastro_widget

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

    def exibir_cadastros(self):
        """Troca para a tela de lista de cadastros."""
        self.stacked_widget.setCurrentWidget(self.lista_widget)

    def resizeEvent(self, event):
        """Ajusta o tamanho da fonte do título quando a janela é redimensionada."""
        nova_largura = event.size().width()
        nova_altura = event.size().height()

        # Calcula o novo tamanho da fonte com base na altura da janela
        novo_tamanho_fonte = max(20, nova_altura // 20)  # Define um tamanho mínimo

        self.titulo.setStyleSheet(f"font-size: {novo_tamanho_fonte}px; font-weight: bold;")  # Atualiza o estilo

        super().resizeEvent(event)

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    janela = JanelaCadastro()
    janela.show()
    sys.exit(app.exec_())
