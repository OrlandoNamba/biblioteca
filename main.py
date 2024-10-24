import os
import shutil
import sys
from PyQt5.QtWidgets import QApplication
from janela_cadastro import JanelaCadastro  # Assegure-se de que a classe esteja definida corretamente

def check_db():
    db_path = 'biblioteca.db'
    if not os.path.exists(db_path):
        shutil.copy('db_template.db', db_path)

def main():
    check_db()
    app = QApplication(sys.argv)
    janela = JanelaCadastro()  # Inicia a janela de cadastro
    janela.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
