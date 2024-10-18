import sqlite3
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton, QLabel, QLineEdit, QHBoxLayout, QMessageBox

class JanelaEdicao(QDialog):
    def __init__(self, id_livro, atualizar_callback):
        super().__init__()
        self.id_livro = id_livro
        self.atualizar_callback = atualizar_callback
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Editar Livro")
        self.setFixedSize(400, 300)

        layout = QVBoxLayout()

        self.campos = {}
        labels = ["Nome", "Autor", "Editora", "Páginas", "ISBN", "Gênero"]

        conn = sqlite3.connect("cadastros.db")
        cursor = conn.cursor()
        cursor.execute("SELECT nomeLivro, autor, editora, numeroPaginas, isbn, genero FROM livros WHERE id = ?", (self.id_livro,))
        dados_livro = cursor.fetchone()
        conn.close()

        for i, label in enumerate(labels):
            label_widget = QLabel(label)
            input_widget = QLineEdit(dados_livro[i] if dados_livro else "")
            layout.addWidget(label_widget)
            layout.addWidget(input_widget)
            self.campos[label] = input_widget

        botoes_layout = QHBoxLayout()

        botao_salvar = QPushButton("Salvar", self)
        botao_salvar.clicked.connect(self.salvar_alteracoes)
        botoes_layout.addWidget(botao_salvar)

        botao_excluir = QPushButton("Excluir", self)
        botao_excluir.clicked.connect(self.excluir_livro)
        botoes_layout.addWidget(botao_excluir)

        botao_cancelar = QPushButton("Cancelar", self)
        botao_cancelar.clicked.connect(self.reject)
        botoes_layout.addWidget(botao_cancelar)

        layout.addLayout(botoes_layout)
        self.setLayout(layout)

    def salvar_alteracoes(self):
        conn = sqlite3.connect("cadastros.db")
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE livros
            SET nomeLivro = ?, autor = ?, editora = ?, numeroPaginas = ?, isbn = ?, genero = ?
            WHERE id = ?
        """, (
            self.campos["Nome"].text(),
            self.campos["Autor"].text(),
            self.campos["Editora"].text(),
            self.campos["Páginas"].text(),
            self.campos["ISBN"].text(),
            self.campos["Gênero"].text(),
            self.id_livro
        ))
        conn.commit()
        conn.close()

        QMessageBox.information(self, "Sucesso", "Alterações salvas com sucesso!")
        self.atualizar_callback()
        self.accept()

    def excluir_livro(self):
        conn = sqlite3.connect("cadastros.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM livros WHERE id = ?", (self.id_livro,))
        conn.commit()
        conn.close()

        QMessageBox.information(self, "Sucesso", "Livro excluído com sucesso!")
        self.atualizar_callback()
        self.accept()
