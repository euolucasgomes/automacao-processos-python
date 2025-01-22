import sqlite3
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class PastaAutomator:
    def __init__(self, driver, db_path):
        """
        Inicializa a classe com o WebDriver e o caminho para o banco de dados.
        """
        self.driver = driver
        self.db_path = db_path

    def conectar_banco(self):
        """
        Conecta ao banco de dados SQLite e retorna a conexão.
        """
        try:
            conn = sqlite3.connect(self.db_path)
            return conn
        except sqlite3.Error as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
            return None

    def buscar_pastas(self, conn):
        """
        Busca todas as pastas no banco de dados.
        """
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT nome_pasta FROM pastas")
            return [row[0] for row in cursor.fetchall()]
        except sqlite3.Error as e:
            print(f"Erro ao buscar pastas no banco de dados: {e}")
            return []

    def clicar_na_pasta(self, nome_pasta):
        """
        Clica na pasta especificada pelo título ou texto visível.
        """
        try:
            print(f"Procurando pela pasta com o título: {nome_pasta} ...")

            xpath = f"//a[@title='{nome_pasta}' or text()='{nome_pasta}']"
            pasta_elemento = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath)))

            self.driver.execute_script("arguments[0].scrollIntoView(true);", pasta_elemento)
            self.driver.execute_script("arguments[0].click();", pasta_elemento)

            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//tr[contains(@class,'message')]"))
            )

            print(f"Pasta com o título '{nome_pasta}' acessada com sucesso.")
        except Exception as e:
            print(f"Erro ao acessar a pasta com o título '{nome_pasta}': {e}")

    def clicar_em_todas_as_pastas(self):
        """
        Clica em todas as pastas listadas no banco de dados, com uma pausa de 10 segundos entre os cliques.
        """
        conn = self.conectar_banco()
        if not conn:
            return

        pastas = self.buscar_pastas(conn)
        if not pastas:
            print("Nenhuma pasta encontrada no banco de dados.")
            conn.close()
            return

        print(f"{len(pastas)} pastas encontradas no banco de dados. Iniciando o processo...")

        for nome_pasta in pastas:
            self.clicar_na_pasta(nome_pasta)
            print("Aguardando 10 segundos antes de clicar na próxima pasta...")
            time.sleep(10)

        print("Processo concluído. Todas as pastas foram acessadas.")
        conn.close()

# Exemplo de uso
# driver = WebDriver inicializado anteriormente
# db_path = "caminho/para/email_pastas.db"
# automator = PastaAutomator(driver, db_path)
# automator.clicar_em_todas_as_pastas()
