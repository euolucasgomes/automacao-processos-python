import os
import sqlite3

class BancoDeDados:
    def __init__(self, db_name="email_pastas.db"):
        """
        Inicializa a conexão com o banco de dados.
        """
        # Define o caminho do banco na pasta 'data'
        db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", db_name)
        self.conn = sqlite3.connect(db_path)
        self.criar_tabela()

    def criar_tabela(self):
        """
        Cria a tabela 'pastas' se não existir.
        """
        with self.conn:
            self.conn.execute("""
            CREATE TABLE IF NOT EXISTS pastas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome_pasta TEXT UNIQUE NOT NULL,
                status TEXT DEFAULT 'pendente'
            )
            """)
        print("Tabela 'pastas' garantida no banco de dados.")

    def inserir_pastas(self, pastas):
        """
        Insere uma lista de pastas na tabela.
        :param pastas: Lista de nomes de pastas (ex: ["Pasta 1", "Pasta 2"])
        """
        with self.conn:
            for pasta in pastas:
                try:
                    self.conn.execute("INSERT INTO pastas (nome_pasta) VALUES (?)", (pasta,))
                    print(f"Pasta '{pasta}' inserida com sucesso.")
                except sqlite3.IntegrityError:
                    print(f"Pasta '{pasta}' já existe no banco de dados.")
        print("Todas as pastas foram processadas para inserção.")

