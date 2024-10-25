import sqlite3
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton,
    QComboBox, QStackedWidget, QSizePolicy, QMessageBox, QLabel, QSpacerItem
)
from PyQt5.QtCore import Qt

from lista_cadastros import ListaCadastros

class JanelaCadastro(QWidget):
    def __init__(self):
        super().__init__()

        # Configurações da janela
        self.setWindowTitle("Cadastro de Livros")
        self.setGeometry(100, 100, 900, 800)

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
        self.titulo.setStyleSheet("font-size: 24px; font-weight: bold;")
        self.titulo.setAlignment(Qt.AlignCenter)  # Centraliza o título
        self.titulo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)  # Título expansível
        layout.addWidget(self.titulo, alignment=Qt.AlignTop)  # Alinhamento superior para o título

        # Adiciona um espaço maior abaixo do título
        layout.addItem(QSpacerItem(0, 30, QSizePolicy.Minimum, QSizePolicy.Expanding))  # Espaço de 30px abaixo do título

        # Campos de entrada
        self.nome_input = self.criar_campo("Nome do Livro")
        self.autor_combo = self.criar_combo("Autor")
        self.editora_combo = self.criar_combo("Editora")
        self.isbn_input = self.criar_campo("ISBN do Livro")
        self.paginas_input = self.criar_campo("Número de Páginas")
        self.genero_combo = self.criar_combo("Gênero")

        # Adiciona os layouts dos campos ao layout principal
        for campo in [self.nome_input, self.autor_combo, self.editora_combo, self.isbn_input, self.paginas_input, self.genero_combo]:
            layout.addLayout(campo[0])  # Adiciona o layout do campo

        # Adiciona um espaço responsivo abaixo do campo de gênero
        layout.addItem(QSpacerItem(0, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))  # Espaço de 20px abaixo dos campos

        # Armazena os campos em atributos para uso posterior
        self.nome_field = self.nome_input[1]
        self.autor_field = self.autor_combo[1]
        self.editora_field = self.editora_combo[1]
        self.isbn_field = self.isbn_input[1]
        self.paginas_field = self.paginas_input[1]
        self.genero_field = self.genero_combo[1]

        # Botões
        self.limpar_button = QPushButton("Limpar", self)
        self.cadastrar_button = QPushButton("Cadastrar", self)
        self.exibir_button = QPushButton("Exibir Cadastros", self)

        # Definir políticas de tamanho para os botões
        for button in [self.limpar_button, self.cadastrar_button, self.exibir_button]:
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # Conectar o botão de exibir cadastros à função de mudança de tela
        self.exibir_button.clicked.connect(self.exibir_cadastros)

        # Layout para os botões
        botoes_layout = QHBoxLayout()
        botoes_layout.addWidget(self.limpar_button)
        botoes_layout.addStretch()  # Espaço para empurrar os botões para o centro
        botoes_layout.addWidget(self.cadastrar_button)
        botoes_layout.addStretch()  # Espaço entre o botão cadastrar e exibir
        botoes_layout.addWidget(self.exibir_button)

        # Adiciona um espaço maior acima dos botões
        layout.addItem(QSpacerItem(0, 30, QSizePolicy.Minimum, QSizePolicy.Expanding))  # Espaço de 30px acima dos botões

        # Adiciona os botões ao layout
        layout.addLayout(botoes_layout)

        # Cria um widget para a tela de cadastro e define seu layout
        cadastro_widget = QWidget()
        cadastro_widget.setLayout(layout)

        # Carregar os dados no QComboBox ao iniciar
        self.carregar_dados_combo()

        return cadastro_widget

    def criar_campo(self, placeholder):
        """Cria um campo de entrada com rótulo ao lado esquerdo."""
        layout = QHBoxLayout()  # Usar layout horizontal para colocar rótulo e campo lado a lado

        rotulo = QLabel(placeholder, self)
        rotulo.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)

        campo = QLineEdit(self)
        campo.setPlaceholderText(f"Digite {placeholder.lower()}")
        campo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # Ajusta o campo para ser expansível verticalmente também

        layout.addWidget(rotulo)  # Adiciona o rótulo
        layout.addWidget(campo)  # Adiciona o campo ao lado do rótulo

        # Ajustar o espaçamento entre o rótulo e o campo
        layout.setContentsMargins(0, 15, 0, 15)  # Margens: superior com 15px para afastar do título
        layout.setSpacing(5)  # Ajusta o espaço entre o rótulo e o campo

        return layout, campo  # Retorna o layout e o campo

    def criar_combo(self, placeholder):
        """Cria um ComboBox com rótulo ao lado esquerdo."""
        layout = QHBoxLayout()  # Usar layout horizontal para colocar rótulo e combo lado a lado

        rotulo = QLabel(placeholder, self)
        rotulo.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)

        combo = QComboBox(self)
        combo.setEditable(True)
        combo.lineEdit().setPlaceholderText(f"Selecione ou digite {placeholder.lower()}")
        combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # Ajusta o combo para ser expansível verticalmente também

        layout.addWidget(rotulo)  # Adiciona o rótulo
        layout.addWidget(combo)  # Adiciona o combo ao lado do rótulo

        # Ajustar o espaçamento entre o rótulo e o combo
        layout.setContentsMargins(0, 15, 0, 15)  # Margens: superior com 15px para afastar do título
        layout.setSpacing(5)  # Ajusta o espaço entre o rótulo e o combo

        return layout, combo  # Retorna o layout e o combo

    def carregar_dados_combo(self):
        """Carrega os autores, editoras e gêneros já cadastrados no banco de dados."""
        try:
            conn = sqlite3.connect('biblioteca.db')
            cursor = conn.cursor()

            # Carregar autores
            autores = cursor.execute("SELECT DISTINCT autor FROM livros").fetchall()
            self.autor_field.clear()  # Limpa itens antes de recarregar (acessando o combo)
            self.autor_field.addItem("")  # Adiciona item vazio para mostrar o placeholder
            for autor in autores:
                self.autor_field.addItem(autor[0])

            # Carregar editoras
            editoras = cursor.execute("SELECT DISTINCT editora FROM livros").fetchall()
            self.editora_field.clear()  # Limpa itens antes de recarregar
            self.editora_field.addItem("")  # Adiciona item vazio para mostrar o placeholder
            for editora in editoras:
                self.editora_field.addItem(editora[0])

            # Carregar gêneros
            generos = cursor.execute("SELECT DISTINCT genero FROM livros").fetchall()
            self.genero_field.clear()  # Limpa itens antes de recarregar
            self.genero_field.addItem("")  # Adiciona item vazio para mostrar o placeholder
            for genero in generos:
                self.genero_field.addItem(genero[0])

            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Erro", str(e))

    def exibir_cadastros(self):
        """Exibe a tela de lista de cadastros."""
        self.stacked_widget.setCurrentWidget(self.lista_widget)

# Executar a aplicação
if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    janela = JanelaCadastro()
    janela.show()
    sys.exit(app.exec_())