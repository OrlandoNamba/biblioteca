import sqlite3

# Cria um banco de dados template
conn = sqlite3.connect('db_template.db')
cursor = conn.cursor()

# Cria a tabela sem inserir dados
cursor.execute('''CREATE TABLE IF NOT EXISTS livros (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    autor TEXT NOT NULL,
    editora TEXT NOT NULL,
    isbn TEXT NOT NULL,
    paginas INTEGER NOT NULL,
    genero TEXT NOT NULL)''')

conn.commit()
conn.close()

print("Banco de dados template criado com sucesso!")
