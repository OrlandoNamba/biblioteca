import customtkinter as ctk
import sqlite3
from tkinter import messagebox
from lista_cadastros import ListaCadastros

# Função para conectar ao banco de dados SQLite e criar tabelas se não existirem
def conectar_banco():
    conn = sqlite3.connect("cadastros.db")
    cursor = conn.cursor()
    
    # Criar tabela de livros
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
    
    # Criar tabela de gêneros
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS generos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            genero TEXT NOT NULL UNIQUE
        )
    ''')
    
    # Inserir gêneros iniciais, caso a tabela esteja vazia
    cursor.execute("INSERT OR IGNORE INTO generos (genero) VALUES ('Ficção'), ('Romance'), ('Suspense'), ('Biografia')")
    conn.commit()
    conn.close()

# Função para carregar os gêneros no Combobox
def carregar_generos():
    conn = sqlite3.connect("cadastros.db")
    cursor = conn.cursor()
    cursor.execute("SELECT genero FROM generos")
    generos = [row[0] for row in cursor.fetchall()]
    conn.close()
    return generos

# Função para cadastrar o novo livro e gênero, caso seja necessário
def cadastrar():
    nomeLivro = entrada_nomeLivro.get()
    autor = entrada_autor.get()
    editora = entrada_editora.get()
    numeroPaginas = entrada_numeroPaginas.get()
    isbn = entrada_isbn.get()
    genero = combobox_genero.get()

    if nomeLivro == "" or autor == "" or editora == "" or numeroPaginas == "" or isbn == "" or genero == "":
        messagebox.showwarning("Atenção", "Todos os campos devem ser preenchidos!")
    else:
        conn = sqlite3.connect("cadastros.db")
        cursor = conn.cursor()

        # Cadastrar o gênero se ele ainda não estiver na tabela
        cursor.execute("INSERT OR IGNORE INTO generos (genero) VALUES (?)", (genero,))
        
        # Cadastrar o livro
        cursor.execute("INSERT INTO livros (nomeLivro, autor, editora, numeroPaginas, isbn, genero) VALUES (?, ?, ?, ?, ?, ?)",
                       (nomeLivro, autor, editora, numeroPaginas, isbn, genero))
        conn.commit()
        conn.close()

        # Atualizar a lista de gêneros no combobox
        atualizar_generos_combobox()

        messagebox.showinfo("Sucesso", "Cadastro realizado com sucesso!")
        limpar_campos()

# Função para trocar de tela para a lista de cadastros
def mostrar_lista_cadastros():
    limpar_tela()
    ListaCadastros(janela, voltar_pagina_principal)

# Função para voltar à página principal
def voltar_pagina_principal():
    limpar_tela()
    criar_interface_principal()

# Função para limpar a tela atual
def limpar_tela():
    for widget in janela.winfo_children():
        widget.destroy()

# Função para limpar os campos de entrada
def limpar_campos():
    entrada_nomeLivro.delete(0, ctk.END)
    entrada_autor.delete(0, ctk.END)
    entrada_editora.delete(0, ctk.END)
    entrada_numeroPaginas.delete(0, ctk.END)
    entrada_isbn.delete(0, ctk.END)
    combobox_genero.set("Selecione o gênero")

# Função para atualizar os gêneros no combobox
def atualizar_generos_combobox():
    generos = carregar_generos()
    combobox_genero.configure(values=generos)

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

# Função para configurar o placeholder no combobox
def set_placeholder_combobox(event=None):
    if combobox_genero.get() == "":
        combobox_genero.set("Selecione o gênero")

def clear_placeholder_combobox(event):
    if combobox_genero.get() == "Selecione o gênero":
        combobox_genero.set("")

# Função para criar a interface principal
def criar_interface_principal():
    # Criando título
    titulo = ctk.CTkLabel(janela, text="Cadastro de Livros", font=ctk.CTkFont(size=18, weight="bold"))
    titulo.grid(row=0, column=0, padx=20, pady=20, columnspan=2)

    # Campo Nome do Livro
    global entrada_nomeLivro
    label_nomeLivro = ctk.CTkLabel(janela, text="Nome Livro:", font=ctk.CTkFont(size=14))
    label_nomeLivro.grid(row=1, column=0, sticky="w", padx=5)
    entrada_nomeLivro = ctk.CTkEntry(janela, width=300)
    entrada_nomeLivro.grid(row=1, column=1, padx=5, pady=2)
    add_placeholder(entrada_nomeLivro, "Digite o nome do livro")

    # Campo Autor
    global entrada_autor
    label_autor = ctk.CTkLabel(janela, text="Autor:", font=ctk.CTkFont(size=14))
    label_autor.grid(row=2, column=0, sticky="w", padx=5)
    entrada_autor = ctk.CTkEntry(janela, width=300)
    entrada_autor.grid(row=2, column=1, padx=5, pady=2)
    add_placeholder(entrada_autor, "Digite o nome do autor")

    # Campo Editora
    global entrada_editora
    label_editora = ctk.CTkLabel(janela, text="Editora:", font=ctk.CTkFont(size=14))
    label_editora.grid(row=3, column=0, sticky="w", padx=5)
    entrada_editora = ctk.CTkEntry(janela, width=300)
    entrada_editora.grid(row=3, column=1, padx=5, pady=2)
    add_placeholder(entrada_editora, "Digite a editora")

    # Campo Número de Páginas
    global entrada_numeroPaginas
    label_numeroPaginas = ctk.CTkLabel(janela, text="Número de Páginas:", font=ctk.CTkFont(size=14))
    label_numeroPaginas.grid(row=4, column=0, sticky="w", padx=5)
    entrada_numeroPaginas = ctk.CTkEntry(janela, width=300)
    entrada_numeroPaginas.grid(row=4, column=1, padx=5, pady=2)
    add_placeholder(entrada_numeroPaginas, "Digite o número de páginas")

    # Campo ISBN
    global entrada_isbn
    label_isbn = ctk.CTkLabel(janela, text="ISBN:", font=ctk.CTkFont(size=14))
    label_isbn.grid(row=5, column=0, sticky="w", padx=5)
    entrada_isbn = ctk.CTkEntry(janela, width=300)
    entrada_isbn.grid(row=5, column=1, padx=5, pady=2)
    add_placeholder(entrada_isbn, "Digite o ISBN")

    # Campo Gênero com Combobox
    global combobox_genero
    label_genero = ctk.CTkLabel(janela, text="Gênero:", font=ctk.CTkFont(size=14))
    label_genero.grid(row=6, column=0, sticky="w", padx=5)
    combobox_genero = ctk.CTkComboBox(janela, width=300, values=carregar_generos())
    combobox_genero.grid(row=6, column=1, padx=5, pady=2)
    combobox_genero.set("Selecione o gênero")
    combobox_genero.bind("<FocusIn>", clear_placeholder_combobox)
    combobox_genero.bind("<FocusOut>", set_placeholder_combobox)

    # Botões de Cadastro e Exibir Cadastros
    botao_cadastrar = ctk.CTkButton(janela, text="Cadastrar", command=cadastrar)
    botao_cadastrar.grid(row=7, column=0, padx=20, pady=10)

    botao_exibir = ctk.CTkButton(janela, text="Exibir Cadastros", command=mostrar_lista_cadastros)
    botao_exibir.grid(row=7, column=1, padx=20, pady=10)

# Configurando o tema do CustomTkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Criando a janela principal
janela = ctk.CTk()
janela.geometry("600x500")
janela.title("Sistema de Cadastro de Livros")

# Conectar ao banco e criar a interface inicial
conectar_banco()
criar_interface_principal()

# Iniciar o loop da interface
janela.mainloop()
