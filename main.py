import customtkinter as ctk
import sqlite3
from tkinter import messagebox
from lista_cadastros import ListaCadastros
from janela_cadastro import JanelaCadastro

# Função para conectar ao banco de dados SQLite e criar tabelas se não existirem
def conectar_banco():
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

# Função para criar a interface principal
def criar_interface_principal():
    JanelaCadastro(janela, mostrar_lista_cadastros)  # Passa a função mostrar_lista_cadastros como callback

# Configurando o tema do CustomTkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Criando a janela principal
janela = ctk.CTk()

# Obtendo as dimensões da tela
largura_tela = janela.winfo_screenwidth()
altura_tela = janela.winfo_screenheight()

# Definindo o tamanho mínimo e máximo da janela
min_largura = 900
min_altura = 600

# Ajustando o tamanho da janela para o máximo permitido
janela.minsize(min_largura, min_altura)  # Define o tamanho mínimo

janela.title("Sistema de Cadastro de Livros")

# Conectar ao banco e criar a interface inicial
conectar_banco()
criar_interface_principal()

# Iniciar o loop da interface
janela.mainloop()
