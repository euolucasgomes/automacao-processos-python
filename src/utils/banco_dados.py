import os
import sqlite3

class BancoDeDados:
    def __init__(self, db_name="email_pastas.db"):
        """
        Inicializa a conexão com o banco de dados e garante que o diretório 'data' exista.
        """
        # Caminho base do projeto
        base_dir = os.path.dirname(os.path.dirname(__file__))  # Diretório principal do projeto
        data_dir = os.path.join(base_dir, "data")  # Diretório 'data'

        # Garante que o diretório 'data' exista
        os.makedirs(data_dir, exist_ok=True)

        # Caminho completo do banco de dados
        db_path = os.path.join(data_dir, db_name)
        print(f"Conectando ao banco de dados em: {db_path}")

        # Inicializa a conexão
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
        :param pastas: Lista de nomes de pastas (ex: ["Pasta 1", "Pasta 2"]).
        """
        with self.conn:
            for pasta in pastas:
                try:
                    self.conn.execute("INSERT INTO pastas (nome_pasta) VALUES (?)", (pasta,))
                    print(f"Pasta '{pasta}' inserida com sucesso.")
                except sqlite3.IntegrityError:
                    print(f"Pasta '{pasta}' já existe no banco de dados.")
        print("Todas as pastas foram processadas para inserção.")

    def buscar_proxima_pasta(self):
        """
        Busca a próxima pasta com status 'pendente'.
        :return: Tupla (id, nome_pasta) ou None se não houver pastas pendentes.
        """
        with self.conn:
            cursor = self.conn.execute("SELECT id, nome_pasta FROM pastas WHERE status = 'pendente' LIMIT 1")
            return cursor.fetchone()  # Retorna a próxima pasta pendente ou None

    def marcar_pasta_concluida(self, pasta_id):
        """
        Marca uma pasta como concluída no banco de dados.
        :param pasta_id: ID da pasta a ser marcada como concluída.
        """
        with self.conn:
            self.conn.execute("UPDATE pastas SET status = 'concluida' WHERE id = ?", (pasta_id,))
            print(f"Pasta ID {pasta_id} marcada como concluída.")

    def listar_todas_pastas(self):
        """
        Lista todas as pastas no banco de dados.
        :return: Lista de tuplas contendo (id, nome_pasta, status).
        """
        with self.conn:
            cursor = self.conn.execute("SELECT * FROM pastas")
            pastas = cursor.fetchall()
            return pastas

    def fechar_conexao(self):
        """
        Fecha a conexão com o banco de dados.
        """
        self.conn.close()
        print("Conexão com o banco de dados fechada.")
