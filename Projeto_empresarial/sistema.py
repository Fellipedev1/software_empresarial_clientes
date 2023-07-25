import tkinter as tk
from tkinter import ttk
import re
import locale
from tkinter import messagebox
import mysql.connector

class Cliente:
    def __init__(self, nome, endereco, contato, detalhes_contrato, valor_pago):
        self.nome = nome
        self.endereco = endereco
        self.contato = contato
        self.detalhes_contrato = detalhes_contrato
        self.valor_pago = valor_pago

class CadastroClientesApp:
    def __init__(self, root):
        self.clientes = []
        self.root = root
        self.root.title("FRM Tecnologia - Cadastro de Clientes")
        self.root.configure(bg='green')

        self.frame = ttk.Frame(self.root)
        self.frame.pack(padx=10, pady=10, expand=True, fill='both')

        ttk.Label(self.frame, text="FRM Tecnologia", font=("Helvetica", 16, "bold")).grid(row=0, column=0, columnspan=3, padx=500, pady=5, sticky="ew")

        ttk.Label(self.frame, text="Nome:").grid(row=1, column=0, padx=5, pady=5)
        self.nome_entry = ttk.Entry(self.frame)
        self.nome_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.frame, text="Detalhes do Contrato:").grid(row=4, column=0, padx=5, pady=5)
        self.detalhes_contrato_entry = ttk.Entry(self.frame)
        self.detalhes_contrato_entry.grid(row=4, column=1, padx=5, pady=5)

        ttk.Label(self.frame, text="Contato:").grid(row=3, column=0, padx=5, pady=5)
        self.contato_entry = ttk.Entry(self.frame)
        self.contato_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(self.frame, text="Endereço:").grid(row=2, column=0, padx=5, pady=5)
        self.endereco_entry = ttk.Entry(self.frame)
        self.endereco_entry.grid(row=2, column=1, padx=5, pady=5)

        self.aviso_nome = ttk.Label(self.frame, text="", foreground="red")
        self.aviso_nome.grid(row=1, column=2, padx=5, pady=5)

        self.aviso_detalhes = ttk.Label(self.frame, text="", foreground="red")
        self.aviso_detalhes.grid(row=4, column=2, padx=5, pady=5)

        ttk.Label(self.frame, text="Valor Pago (R$):").grid(row=5, column=0, padx=5, pady=5)
        self.valor_pago_entry = ttk.Entry(self.frame)
        self.valor_pago_entry.grid(row=5, column=1, padx=5, pady=5)

        ttk.Button(self.frame, text="Cadastrar", command=self.cadastrar_cliente).grid(row=6, column=0, columnspan=3, padx=5, pady=5)

        self.tree = ttk.Treeview(self.frame, columns=("nome", "endereco", "contato", "detalhes_contrato", "valor_pago"), show="headings")
        self.tree.heading("#1", text="Nome")
        self.tree.heading("#2", text="Endereço")
        self.tree.heading("#3", text="Contato")
        self.tree.heading("#4", text="Detalhes do Contrato")
        self.tree.heading("#5", text="Valor Pago (R$)")

        self.tree.column("#1", anchor="center", width=150)
        self.tree.column("#2", anchor="center", width=200)
        self.tree.column("#3", anchor="center", width=150)
        self.tree.column("#4", anchor="center", width=300)
        self.tree.column("#5", anchor="center", width=150)

        self.tree_scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=self.tree.yview)
        self.tree_scrollbar.grid(row=7, column=5, sticky="ns")
        self.tree.configure(yscrollcommand=self.tree_scrollbar.set)

        self.tree.grid(row=7, column=0, columnspan=5, padx=5, pady=5)

        ttk.Button(self.frame, text="Calcular Faturamento", command=self.calcular_faturamento).grid(row=8, column=0, columnspan=5, padx=5, pady=5)

        self.faturamento_label = ttk.Label(self.frame, text="Valor Faturado: R$ 0.00")
        self.faturamento_label.grid(row=9, column=0, columnspan=5, padx=5, pady=5)

        root.bind('<Return>', lambda event: self.cadastrar_cliente())
        self.criar_interface_pesquisa()

        # Database connection
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="acesso123",
                database="sistema"
            )
            self.cursor = self.conn.cursor()

            create_table_query = """
            CREATE TABLE IF NOT EXISTS clientes (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(255) NOT NULL,
                endereco VARCHAR(255) NOT NULL,
                contato VARCHAR(255) NOT NULL,
                detalhes_contrato VARCHAR(255) NOT NULL,
                valor_pago DECIMAL(10, 2) NOT NULL
            )
            """
            self.cursor.execute(create_table_query)

            self.cursor.execute("SELECT * FROM clientes")
            rows = self.cursor.fetchall()
            for row in rows:
                nome, endereco, contato, detalhes_contrato, valor_pago = row
                cliente = Cliente(nome, endereco, contato, detalhes_contrato, valor_pago)
                self.clientes.append(cliente)

            self.atualizar_tabela()

        except mysql.connector.Error as e:
            messagebox.showerror("Erro de Conexão", f"Ocorreu um erro ao conectar ao banco de dados: {e}")

    def formatar_valor(self, valor):
        try:
            valor_formatado = locale.currency(float(valor), grouping=True)
            return valor_formatado
        except ValueError:
            return ""

    def validar_nome(self, nome):
        if not re.match("^[A-Za-z ]+$", nome):
            self.aviso_nome.config(text="Somente letras e caracteres são permitidos.")
            return False
        else:
            self.aviso_nome.config(text="")
            return True

    def validar_detalhes(self, detalhes):
        if not re.match("^[A-Za-z ]+$", detalhes):
            self.aviso_detalhes.config(text="Somente letras e caracteres são permitidos.")
            return False
        else:
            self.aviso_detalhes.config(text="")
            return True

    def cadastrar_cliente(self):
        nome = self.nome_entry.get()
        endereco = self.endereco_entry.get()
        contato = self.contato_entry.get()
        detalhes_contrato = self.detalhes_contrato_entry.get()
        valor_pago = self.valor_pago_entry.get()

        if not self.validar_nome(nome) or not self.validar_detalhes(detalhes_contrato):
            return

        if not valor_pago:
            messagebox.showerror("Erro", "Digite um valor para 'Valor Pago (R$)'.")
            return

        try:
            valor_pago = float(valor_pago)
        except ValueError:
            messagebox.showerror("Erro", "Digite um valor numérico para 'Valor Pago (R$)'.")
            return

        cliente = Cliente(nome, endereco, contato, detalhes_contrato, valor_pago)
        self.clientes.append(cliente)

        self.nome_entry.delete(0, tk.END)
        self.endereco_entry.delete(0, tk.END)
        self.contato_entry.delete(0, tk.END)
        self.detalhes_contrato_entry.delete(0, tk.END)
        self.valor_pago_entry.delete(0, tk.END)

        try:
            insert_query = "INSERT INTO clientes (nome, endereco, contato, detalhes_contrato, valor_pago) VALUES (%s, %s, %s, %s, %s)"
            values = (nome, endereco, contato, detalhes_contrato, valor_pago)
            self.cursor.execute(insert_query, values)
            self.conn.commit()

            self.cursor.execute("SELECT LAST_INSERT_ID()")
            last_id = self.cursor.fetchone()[0]
            cliente.id = last_id

        except mysql.connector.Error as e:
            messagebox.showerror("Erro de Inserção", f"Ocorreu um erro ao inserir os dados no banco de dados: {e}")

        self.atualizar_tabela()
        self.nome_entry.focus_set()

    def atualizar_tabela(self, resultados=None):
        self.tree.delete(*self.tree.get_children())

        if resultados is None:
            resultados = self.clientes

        for cliente in resultados:
            valor_formatado = self.formatar_valor(cliente.valor_pago)
            self.tree.insert("", "end", values=(cliente.nome, cliente.endereco, cliente.contato, cliente.detalhes_contrato, valor_formatado))

    def calcular_faturamento(self):
        faturamento_total = sum(cliente.valor_pago for cliente in self.clientes)
        valor_formatado = self.formatar_valor(faturamento_total)
        self.faturamento_label.config(text=f"Valor Faturado: {valor_formatado}")

    def criar_interface_pesquisa(self):
        ttk.Label(self.frame, text="Pesquisar Cliente por Nome:").grid(row=10, column=0, padx=5, pady=5)
        self.pesquisa_entry = ttk.Entry(self.frame)
        self.pesquisa_entry.grid(row=10, column=1, padx=5, pady=5)

        ttk.Button(self.frame, text="Pesquisar", command=self.pesquisar_cliente).grid(row=10, column=2, padx=5, pady=5)

    def pesquisar_cliente(self):
        nome_pesquisado = self.pesquisa_entry.get().strip().lower()
        resultados = []

        for cliente in self.clientes:
            if nome_pesquisado in cliente.nome.lower():
                resultados.append(cliente)

        if not resultados:
            messagebox.showinfo("Pesquisa", f"Nenhum cliente encontrado com o nome '{self.pesquisa_entry.get()}'")
            return

        self.atualizar_tabela(resultados)

if __name__ == "__main__":
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

    root = tk.Tk()
    app = CadastroClientesApp(root)
    root.mainloop()
