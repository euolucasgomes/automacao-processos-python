from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import sqlite3

class EmailAutomation:
    def __init__(self, driver):
        """
        Inicializa a classe com o WebDriver.
        """
        self.driver = driver

    def clicar_em_todas_as_pastas(self, driver, db_path):
        """
        Clica em todas as pastas especificadas no banco de dados, com uma pausa de 10 segundos entre os cliques.
        """
        try:
            # Conecta ao banco de dados
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            # Busca todas as pastas da coluna `nome_pasta`
            cursor.execute("SELECT nome_pasta FROM pastas")
            pastas = cursor.fetchall()

            if not pastas:
                print("Nenhuma pasta encontrada no banco de dados.")
                return

            print(f"{len(pastas)} pastas encontradas no banco de dados. Iniciando o processo...")

            for (nome_pasta,) in pastas:
                print(f"Procurando pela pasta com o título: {nome_pasta} ...")
                try:
                    # XPath atualizado para localizar pelo título ou texto visível
                    xpath = f"//a[@title='{nome_pasta}' or text()='{nome_pasta}']"

                    # Aguarda o carregamento da página e a presença do elemento
                    pasta_elemento = WebDriverWait(driver, 20).until(
                        EC.presence_of_element_located((By.XPATH, xpath))
                    )

                    # Aguarda até que o elemento seja clicável
                    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath)))

                    # Role até o elemento e clique
                    driver.execute_script("arguments[0].scrollIntoView(true);", pasta_elemento)
                    driver.execute_script("arguments[0].click();", pasta_elemento)

                    # Aguarda o carregamento da nova página/pasta
                    WebDriverWait(driver, 20).until(
                        EC.presence_of_element_located((By.XPATH, "//tr[contains(@class,'message')]"))
                    )

                    print(f"Pasta com o título '{nome_pasta}' acessada com sucesso.")

                except Exception as e:
                    print(f"Erro ao acessar a pasta '{nome_pasta}': {e}")

                # Pausa de 10 segundos entre os cliques
                print("Aguardando 10 segundos antes de clicar na próxima pasta...")
                time.sleep(10)

            print("Processo concluído. Todas as pastas foram acessadas.")
        except Exception as e:
            print(f"Erro ao processar as pastas: {e}")
        finally:
            if 'conn' in locals():
                conn.close()