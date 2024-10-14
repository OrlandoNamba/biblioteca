import customtkinter as ctk
import sqlite3
from tkinter import messagebox

class JanelaCadastro:
    def __init__(self, janela, mostrar_lista_callback):
        self.janela = janela
        self.mostrar_lista_callback = mostrar_lista_callback  
        self.criar_interface_principal()

    def carregar_generos(self):
        conn = sqlite3.connect("cadastros.db")
        cursor = conn.cursor()
        cursor.execute("SELECT genero FROM generos")
        generos = [row[0] for row in cursor.fetchall()]
        conn.close()
        return generos

    def cadastrar(self):
        nomeLivro = self.entrada_nomeLivro.get()
        autor = self.entrada_autor.get()
        editora = self.entrada_editora.get()
        numeroPaginas = self.entrada_numeroPaginas.get()
        isbn = self.entrada_isbn.get()
        genero = self.combobox_genero.get()

        if nomeLivro == "" or autor == "" or editora == "" or numeroPaginas == "" or isbn == "" or genero == "":
            messagebox.showwarning("Atenção", "Todos os campos devem ser preenchidos!")
        else:
            conn = sqlite3.connect("cadastros.db")
            cursor = conn.cursor()
            cursor.execute("INSERT OR IGNORE INTO generos (genero) VALUES (?)", (genero,))
            cursor.execute("INSERT INTO livros (nomeLivro, autor, editora, numeroPaginas, isbn, genero) VALUES (?, ?, ?, ?, ?, ?)",
                           (nomeLivro, autor, editora, numeroPaginas, isbn, genero))
            conn.commit()
            conn.close()

            self.atualizar_generos_combobox()
            messagebox.showinfo("Sucesso", "Cadastro realizado com sucesso!")
            self.limpar_campos()

    def limpar_campos(self):
        self.entrada_nomeLivro.delete(0, ctk.END)
        self.entrada_autor.delete(0, ctk.END)
        self.entrada_editora.delete(0, ctk.END)
        self.entrada_numeroPaginas.delete(0, ctk.END)
        self.entrada_isbn.delete(0, ctk.END)
        self.combobox_genero.set("Selecione o gênero")

    def atualizar_generos_combobox(self):
        generos = self.carregar_generos()
        self.combobox_genero.configure(values=generos)

    def add_placeholder(self, entry, placeholder):
        entry.insert(0, placeholder)
        entry.bind("<FocusIn>", lambda e: self.clear_placeholder(entry, placeholder))
        entry.bind("<FocusOut>", lambda e: self.set_placeholder(entry, placeholder))

    def clear_placeholder(self, entry, placeholder):
        if entry.get() == placeholder:
            entry.delete(0, ctk.END)

    def set_placeholder(self, entry, placeholder):
        if entry.get() == "":
            entry.insert(0, placeholder)

    def set_placeholder_combobox(self, event=None):
        if self.combobox_genero.get() == "":
            self.combobox_genero.set("Selecione o gênero")

    def clear_placeholder_combobox(self, event):
        if self.combobox_genero.get() == "Selecione o gênero":
            self.combobox_genero.set("")

    def limpar_tela(self):
        """Função para limpar a tela atual"""
        for widget in self.janela.winfo_children():
            widget.destroy()

    def criar_interface_principal(self):
        # Limpar a tela anterior antes de recriar a interface de cadastro
        self.limpar_tela()

        # Configurando a janela para redimensionar
        self.janela.grid_rowconfigure(0, weight=1)  # Para o título
        self.janela.grid_rowconfigure(1, weight=1)  # Para Nome do Livro
        self.janela.grid_rowconfigure(2, weight=1)  # Para Autor
        self.janela.grid_rowconfigure(3, weight=1)  # Para Editora
        self.janela.grid_rowconfigure(4, weight=1)  # Para Número de Páginas
        self.janela.grid_rowconfigure(5, weight=1)  # Para ISBN
        self.janela.grid_rowconfigure(6, weight=1)  # Para Gênero
        self.janela.grid_rowconfigure(7, weight=1)  # Para Botões
        self.janela.grid_columnconfigure(0, weight=1)
        self.janela.grid_columnconfigure(1, weight=1)

        # Criando título (Centralizado)
        titulo = ctk.CTkLabel(self.janela, text="Cadastro de Livros", font=ctk.CTkFont(size=18, weight="bold"))
        titulo.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")  # Centralizado em todos os lados

        # Campo Nome do Livro (Centralizado)
        label_nomeLivro = ctk.CTkLabel(self.janela, text="Nome Livro:", font=ctk.CTkFont(size=14))
        label_nomeLivro.grid(row=1, column=0, padx=5, pady=2, sticky="nsew")
        self.entrada_nomeLivro = ctk.CTkEntry(self.janela, width=300, justify="center")
        self.entrada_nomeLivro.grid(row=1, column=1, padx=5, pady=2, sticky="nsew")
        self.add_placeholder(self.entrada_nomeLivro, "Digite o nome do livro")

        # Campo Autor (Centralizado)
        label_autor = ctk.CTkLabel(self.janela, text="Autor:", font=ctk.CTkFont(size=14))
        label_autor.grid(row=2, column=0, padx=5, pady=2, sticky="nsew")
        self.entrada_autor = ctk.CTkEntry(self.janela, width=300, justify="center")
        self.entrada_autor.grid(row=2, column=1, padx=5, pady=2, sticky="nsew")
        self.add_placeholder(self.entrada_autor, "Digite o nome do autor")

        # Campo Editora (Centralizado)
        label_editora = ctk.CTkLabel(self.janela, text="Editora:", font=ctk.CTkFont(size=14))
        label_editora.grid(row=3, column=0, padx=5, pady=2, sticky="nsew")
        self.entrada_editora = ctk.CTkEntry(self.janela, width=300, justify="center")
        self.entrada_editora.grid(row=3, column=1, padx=5, pady=2, sticky="nsew")
        self.add_placeholder(self.entrada_editora, "Digite a editora")

        # Campo Número de Páginas (Centralizado)
        label_numeroPaginas = ctk.CTkLabel(self.janela, text="Número de Páginas:", font=ctk.CTkFont(size=14))
        label_numeroPaginas.grid(row=4, column=0, padx=5, pady=2, sticky="nsew")
        self.entrada_numeroPaginas = ctk.CTkEntry(self.janela, width=300, justify="center")
        self.entrada_numeroPaginas.grid(row=4, column=1, padx=5, pady=2, sticky="nsew")
        self.add_placeholder(self.entrada_numeroPaginas, "Digite o número de páginas")

        # Campo ISBN (Centralizado)
        label_isbn = ctk.CTkLabel(self.janela, text="ISBN:", font=ctk.CTkFont(size=14))
        label_isbn.grid(row=5, column=0, padx=5, pady=2, sticky="nsew")
        self.entrada_isbn = ctk.CTkEntry(self.janela, width=300, justify="center")
        self.entrada_isbn.grid(row=5, column=1, padx=5, pady=2, sticky="nsew")
        self.add_placeholder(self.entrada_isbn, "Digite o ISBN")

        # Combobox para Gênero (Centralizado)
        label_genero = ctk.CTkLabel(self.janela, text="Gênero:", font=ctk.CTkFont(size=14))
        label_genero.grid(row=6, column=0, padx=5, pady=2, sticky="nsew")
        self.combobox_genero = ctk.CTkComboBox(self.janela, values=self.carregar_generos(), width=295, justify="center")
        self.combobox_genero.grid(row=6, column=1, padx=5, pady=2, sticky="nsew")
        self.combobox_genero.bind("<FocusIn>", self.clear_placeholder_combobox)
        self.combobox_genero.bind("<FocusOut>", self.set_placeholder_combobox)
        self.combobox_genero.set("Selecione o gênero")

        # Botão Cadastrar (Centralizado)
        self.botao_cadastrar = ctk.CTkButton(self.janela, text="Cadastrar", command=self.cadastrar)
        self.botao_cadastrar.grid(row=7, column=0, padx=10, pady=10, sticky="nsew")

        # Botão Exibir Cadastros (Centralizado)
        self.botao_exibir = ctk.CTkButton(self.janela, text="Exibir Cadastros", command=self.mostrar_lista_callback)
        self.botao_exibir.grid(row=7, column=1, padx=10, pady=10, sticky="nsew")

# Exemplo de uso:
if __name__ == "__main__":
    root = ctk.CTk()
    JanelaCadastro(root, mostrar_lista_callback=lambda: print("Mostrar lista de cadastros aqui."))
    root.mainloop()
