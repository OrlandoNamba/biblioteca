import sqlite3
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QPushButton, QMessageBox, QHBoxLayout

class ListaCadastros(QWidget):
    def __init__(self):
        super().__init__()

        # Configurações da janela
        self.setWindowTitle("Lista de Cadastros")
        self.setGeometry(100, 100, 600, 400)

        # Layout
        self.layout = QVBoxLayout()

        # Tabela para exibir os livros
        self.tabela = QTableWidget(self)
        self.layout.addWidget(self.tabela)

        # Botões de navegação
        self.botoes_layout = QHBoxLayout()
        
        self.anterior_button = QPushButton("Anterior", self)
        self.anterior_button.clicked.connect(self.mostrar_anterior)
        self.botoes_layout.addWidget(self.anterior_button)

        self.proxima_button = QPushButton("Próxima", self)
        self.proxima_button.clicked.connect(self.mostrar_proxima)
        self.botoes_layout.addWidget(self.proxima_button)

        self.layout.addLayout(self.botoes_layout)

        # Adiciona o layout à janela
        self.setLayout(self.layout)

        # Atributos para controle de página
        self.pagina_atual = 0
        self.livros_por_pagina = 10  # Número de livros a serem exibidos por página

        # Carrega os dados iniciais
        self.carregar_dados()

    def carregar_dados(self):
        """Carrega os livros do banco de dados e exibe na tabela."""
        try:
            conn = sqlite3.connect('biblioteca.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM livros")
            self.livros = cursor.fetchall()  # Armazena todos os livros
            conn.close()

            # Define o número de colunas na tabela
            if self.livros:
                self.tabela.setColumnCount(len(self.livros[0]))  # Define o número de colunas com base no primeiro livro

            # Exibe a primeira página
            self.exibir_pagina()

        except sqlite3.Error as e:
            QMessageBox.critical(self, "Erro", f"Ocorreu um erro ao carregar os dados: {e}")

    def exibir_pagina(self):
        """Exibe os livros da página atual."""
        self.tabela.setRowCount(0)  # Limpa a tabela

        # Checa se há livros a exibir
        if not self.livros:
            QMessageBox.information(self, "Informação", "Nenhum livro encontrado.")
            return

        for i in range(self.pagina_atual * self.livros_por_pagina, 
                       min((self.pagina_atual + 1) * self.livros_por_pagina, len(self.livros))):
            livro = self.livros[i]
            row_position = self.tabela.rowCount()
            self.tabela.insertRow(row_position)

            # Preenche a tabela com os dados do livro
            for j, dado in enumerate(livro):
                self.tabela.setItem(row_position, j, QTableWidgetItem(str(dado)))

        self.atualizar_botoes()

    def atualizar_botoes(self):
        """Atualiza o estado dos botões de navegação."""
        self.anterior_button.setEnabled(self.pagina_atual > 0)
        self.proxima_button.setEnabled((self.pagina_atual + 1) * self.livros_por_pagina < len(self.livros))

    def mostrar_anterior(self):
        """Mostra a página anterior."""        
        if self.pagina_atual > 0:
            self.pagina_atual -= 1
            self.exibir_pagina()

    def mostrar_proxima(self):
        """Mostra a próxima página."""        
        if (self.pagina_atual + 1) * self.livros_por_pagina < len(self.livros):
            self.pagina_atual += 1
            self.exibir_pagina()
