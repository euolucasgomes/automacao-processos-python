from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
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
                    # Acessa a pasta
                    self.clicar_na_pasta(nome_pasta)

                    # Processa os emails na pasta
                    self.processar_emails_na_pasta()

                except Exception as e:
                    print(f"Erro ao acessar ou processar a pasta '{nome_pasta}': {e}")

                # Pausa de 10 segundos entre os cliques
                print("Aguardando 10 segundos antes de clicar na próxima pasta...")
                time.sleep(10)

            print("Processo concluído. Todas as pastas foram acessadas.")
        except Exception as e:
            print(f"Erro ao processar as pastas: {e}")
        finally:
            if 'conn' in locals():
                conn.close()

    def clicar_na_pasta(self, nome_pasta):
        """
        Clica na pasta especificada pelo título ou texto visível.
        """
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
        print(f"Pasta '{nome_pasta}' acessada com sucesso.")

    def processar_emails_na_pasta(self):
        """
        Processa os emails dentro da pasta: clica no email, verifica a data e decide continuar ou passar.
        """
        try:
            emails = WebDriverWait(self.driver, 20).until(
                EC.presence_of_all_elements_located((By.XPATH, "//tr[contains(@class, 'message')]"))
            )
            tentativa = 0

            for email in emails:
                try:
                    # Clica no email
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", email)
                    email.click()
                    print("Email clicado com sucesso!")

                    # Verifica a data do email
                    if self.verificar_data_email():
                        print("Email dentro do mês corrente encontrado!")
                        return  # Para o processamento, já que encontrou um email válido
                    else:
                        print("Email fora do mês corrente. Tentando o próximo.")
                        tentativa += 1

                    if tentativa >= 2:
                        print("Nenhum email válido encontrado. Passando para a próxima pasta.")
                        break

                except Exception as e:
                    print(f"Erro ao processar email: {e}")
        except Exception as e:
            print(f"Erro ao processar emails na pasta: {e}")

    def verificar_data_email(self):
        """
        Verifica se a data do email na <span class="text-nowrap"> está dentro do mês corrente.
        """
        try:
            data_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//span[contains(@class, 'text-nowrap')]"))
            )
            data_texto = data_element.text.strip()

            # Obtem o mês e o ano corrente
            mes_corrente = datetime.now().strftime("%m")
            ano_corrente = datetime.now().strftime("%Y")

            # Caso 1: Data completa no formato "aaaa-mm-dd hh:mm"
            if "-" in data_texto and ":" in data_texto:
                try:
                    data_email = datetime.strptime(data_texto.split(" ")[0], "%Y-%m-%d")
                    return data_email.strftime("%m") == mes_corrente and data_email.strftime("%Y") == ano_corrente
                except ValueError as ve:
                    print(f"Erro ao converter data completa: {ve}")
                    return False

            # Caso 2: Data abreviada (exemplo: "Seg.", "Terç.")
            elif data_texto in ["Seg.", "Terç.", "Qua.", "Qui.", "Sex.", "Sáb.", "Dom."]:
                print(f"Data abreviada encontrada: '{data_texto}'. Considerando como mês corrente.")
                return True  # Assume que datas abreviadas pertencem ao mês corrente

            print(f"Formato de data não identificado: '{data_texto}'")
            return False

        except Exception as e:
            print(f"Erro ao verificar a data do email: {e}")
            return False
