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

# Função para mostrar o frame de cadastros
def mostrar_cadastro():
    frame_lista.grid_forget()
    frame_cadastro.grid(row=0, column=0, sticky="nsew")
    janela_cadastro.atualizar_generos_combobox()  # Atualiza combobox para evitar problemas com novos gêneros

# Função para mostrar o frame de lista de cadastros
def mostrar_lista_cadastros():
    frame_cadastro.grid_forget()
    frame_lista.grid(row=0, column=0, sticky="nsew")
    janela_lista.exibir_cadastros()

# Configurando o tema do CustomTkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Criando a janela principal
janela = ctk.CTk()
janela.title("Sistema de Cadastro de Livros")

# Frame principal para alternar entre telas
frame_cadastro = ctk.CTkFrame(janela)
frame_lista = ctk.CTkFrame(janela)

# Configurar os frames para ocupar o espaço total da janela
frame_cadastro.grid(row=0, column=0, sticky="nsew")
frame_lista.grid(row=0, column=0, sticky="nsew")

# Permitir que os frames se redimensionem
janela.grid_rowconfigure(0, weight=1)
janela.grid_columnconfigure(0, weight=1)

# Criar instâncias das janelas de cadastro e lista
janela_cadastro = JanelaCadastro(frame_cadastro, mostrar_lista_cadastros)
janela_lista = ListaCadastros(frame_lista, mostrar_cadastro)

# Conectar ao banco e exibir tela inicial
conectar_banco()
mostrar_cadastro()

# Iniciar o loop da interface
janela.mainloop()
