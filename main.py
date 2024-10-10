import customtkinter as ctk
import sqlite3
from tkinter import messagebox

# Função para conectar ao banco de dados SQLite e criar tabela se não existir
def conectar_banco():
    conn = sqlite3.connect("cadastros.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS livros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nomeLivro TEXT NOT NULL,
            autor TEXT NOT NULL,
            editora TEXT NOT NULL,
            numeroPaginas INT NOT NULL,
            isbn INT NOT NULL,
            genero TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Função para cadastrar os dados no banco de dados
def cadastrar():
    nomeLivro = entrada_nomeLivro.get()
    autor = entrada_autor.get()
    editora = entrada_editora.get()
    numeroPaginas = entrada_numeroPaginas.get()
    isbn = entrada_isbn.get()
    genero = entrada_genero.get()

    if nomeLivro == "" or autor == "" or editora == "" or numeroPaginas == "" or isbn == "" or genero == "" :
        messagebox.showwarning("Atenção", "Todos os campos devem ser preenchidos!")
    else:
        conn = sqlite3.connect("cadastros.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO livros (nomeLivro, autor, editora, numeroPaginas, isbn, genero) VALUES (?, ?, ?, ?, ?, ?)", (nomeLivro, autor, editora, numeroPaginas, isbn, genero))
        conn.commit()
        conn.close()
        messagebox.showinfo("Sucesso", "Cadastro realizado com sucesso!")
        limpar_campos()

# Função para exibir os dados cadastrados
def exibir_cadastros():
    conn = sqlite3.connect("cadastros.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM livros")
    registros = cursor.fetchall()
    conn.close()

    if not registros:
        messagebox.showinfo("Sem Cadastros", "Nenhum cadastro foi realizado ainda.")
        return

    janela_cadastros = ctk.CTkToplevel(janela)
    janela_cadastros.title("Cadastros Realizados")
    janela_cadastros.geometry("800x400")

    # Título da janela centralizado
    titulo = ctk.CTkLabel(janela_cadastros, text="Cadastros Realizados", font=ctk.CTkFont(size=18, weight="bold"))
    titulo.grid(row=0, column=0, columnspan=2, padx=20, pady=10)

    # Cabeçalhos da tabela
    cabecalho = ctk.CTkLabel(janela_cadastros, text="ID | Nome do Livro                | Autor                     | Editora                     | Número de Páginas                     | ISBN                     | Genêro", font=ctk.CTkFont(size=12, weight="bold"))
    cabecalho.grid(row=1, column=0, columnspan=2, padx=20)

    # Linha de separação
    separator = ctk.CTkLabel(janela_cadastros, text="---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
    separator.grid(row=2, column=0, columnspan=2, padx=20)

    # Adicionando registros
    for idx, cadastro in enumerate(registros, start=3):
        linha = f"{cadastro[0]:<3} | {cadastro[1]:<20}                | {cadastro[2]:<25}                     | {cadastro[3]}                     | {cadastro[4]}                     | {cadastro[5]}                     | {cadastro[6]}"
        label_cadastro = ctk.CTkLabel(janela_cadastros, text=linha, font=ctk.CTkFont(size=12))
        label_cadastro.grid(row=idx, column=0, sticky="w", padx=20)

    # Botão para fechar a janela
    btn_fechar = ctk.CTkButton(janela_cadastros, text="Fechar", command=janela_cadastros.destroy)
    btn_fechar.grid(row=idx + 1, column=0, columnspan=2, pady=10)

# Função para limpar os campos de entrada
def limpar_campos():
    entrada_nomeLivro.delete(0, ctk.END)
    entrada_autor.delete(0, ctk.END)
    entrada_editora.delete(0, ctk.END)
    entrada_numeroPaginas.delete(0, ctk.END)
    entrada_isbn.delete(0, ctk.END)
    entrada_genero.delete(0, ctk.END)

# Função para adicionar placeholders nas entradas
def add_placeholder(entry, placeholder):
    entry.insert(0, placeholder)
    entry.bind("<FocusIn>", lambda e: clear_placeholder(entry, placeholder))
    entry.bind("<FocusOut>", lambda e: set_placeholder(entry, placeholder))

def clear_placeholder(entry, placeholder):
    if entry.get() == placeholder:
        entry.delete(0, ctk.END)

def set_placeholder(entry, placeholder):
    if entry.get() == "":
        entry.insert(0, placeholder)

# Configurando o tema do CustomTkinter
ctk.set_appearance_mode("dark")  # "dark", "light", or "system"
ctk.set_default_color_theme("dark-blue")  # "blue", "green", "dark-blue"

# Criando a janela principal
janela = ctk.CTk()
janela.title("Sistema de Cadastro")
janela.geometry("800x600")

# Conectando ao banco de dados e criando a tabela
conectar_banco()

# Criando título
titulo = ctk.CTkLabel(janela, text="Cadastro de Livros", font=ctk.CTkFont(size=18, weight="bold"))
titulo.grid(row=0, column=0, padx=20, pady=20, columnspan=2)

# Campo Nome do Livro
label_nomeLivro = ctk.CTkLabel(janela, text="Nome Livro:", font=ctk.CTkFont(size=14))
label_nomeLivro.grid(row=1, column=0, sticky="w", padx=5)
entrada_nomeLivro = ctk.CTkEntry(janela, width=300)
entrada_nomeLivro.grid(row=1, column=1, padx=5, pady=2)
add_placeholder(entrada_nomeLivro, "Digite o nome do livro")

# Campo Autor
label_autor = ctk.CTkLabel(janela, text="Autor:", font=ctk.CTkFont(size=14))
label_autor.grid(row=2, column=0, sticky="w", padx=5)
entrada_autor = ctk.CTkEntry(janela, width=300)
entrada_autor.grid(row=2, column=1, padx=5, pady=2)
add_placeholder(entrada_autor, "Digite o nome do autor")

# Campo editora
label_editora = ctk.CTkLabel(janela, text="Editora:", font=ctk.CTkFont(size=14))
label_editora.grid(row=3, column=0, sticky="w", padx=5)
entrada_editora = ctk.CTkEntry(janela, width=300)
entrada_editora.grid(row=3, column=1, padx=5, pady=2)
add_placeholder(entrada_editora, "Digite seu editora")

# Campo numeroPaginas
label_numeroPaginas = ctk.CTkLabel(janela, text="Número de Páginas:", font=ctk.CTkFont(size=14))
label_numeroPaginas.grid(row=4, column=0, sticky="w", padx=5)
entrada_numeroPaginas = ctk.CTkEntry(janela, width=300)
entrada_numeroPaginas.grid(row=4, column=1, padx=5, pady=2)
add_placeholder(entrada_numeroPaginas, "Digite o número de páginas")

# Campo isbn
label_isbn = ctk.CTkLabel(janela, text="ISBN:", font=ctk.CTkFont(size=14))
label_isbn.grid(row=5, column=0, sticky="w", padx=5)
entrada_isbn = ctk.CTkEntry(janela, width=300)
entrada_isbn.grid(row=5, column=1, padx=5, pady=2)
add_placeholder(entrada_isbn, "Digite o ISBN do livro")

# Campo genero
label_genero = ctk.CTkLabel(janela, text="Gênero:", font=ctk.CTkFont(size=14))
label_genero.grid(row=6, column=0, sticky="w", padx=5)
entrada_genero = ctk.CTkEntry(janela, width=300)
entrada_genero.grid(row=6, column=1, padx=5, pady=2)
add_placeholder(entrada_genero, "Digite o gênero do livro")

# Botões de Cadastro e Exibir Cadastros
botao_cadastrar = ctk.CTkButton(janela, text="Cadastrar", command=cadastrar)
botao_cadastrar.grid(row=7, column=0, padx=20, pady=10)

botao_exibir = ctk.CTkButton(janela, text="Exibir Cadastros", command=exibir_cadastros)
botao_exibir.grid(row=7, column=1, padx=20, pady=10)

# Executando a janela
janela.mainloop()