import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget, QWidget, QVBoxLayout, QLabel, QComboBox, QLineEdit, QPushButton, QMessageBox, QHBoxLayout
from janela_cadastro import JanelaCadastro
from lista_cadastros import ListaCadastros

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Cadastro de Livros - Sinfy")
        self.setMinimumSize(900, 600)

        # Stacked Widget para alternar entre telas
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Inicializar tela de cadastro e lista
        self.cadastro_widget = JanelaCadastro(self.show_lista)
        self.lista_widget = ListaCadastros(self.show_cadastro)

        self.stacked_widget.addWidget(self.cadastro_widget)
        self.stacked_widget.addWidget(self.lista_widget)

        self.conectar_banco()
        self.stacked_widget.setCurrentWidget(self.cadastro_widget)

    def conectar_banco(self):
        conn = sqlite3.connect("cadastros.db")
        cursor = conn.cursor()

        # Criar tabela de livros
        cursor.execute('''CREATE TABLE IF NOT EXISTS livros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nomeLivro TEXT NOT NULL,
            autor TEXT NOT NULL,
            editora TEXT NOT NULL,
            numeroPaginas INT NOT NULL,
            isbn INT NOT NULL,
            genero TEXT NOT NULL)''')

        # Criar tabela de gêneros
        cursor.execute('''CREATE TABLE IF NOT EXISTS generos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            genero TEXT NOT NULL UNIQUE)''')

        # Inserir gêneros iniciais, caso a tabela esteja vazia
        cursor.execute("INSERT OR IGNORE INTO generos (genero) VALUES ('Ficção'), ('Romance'), ('Suspense'), ('Biografia')")
        conn.commit()
        conn.close()

    def show_lista(self):
        self.stacked_widget.setCurrentWidget(self.lista_widget)

    def show_cadastro(self):
        self.stacked_widget.setCurrentWidget(self.cadastro_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
