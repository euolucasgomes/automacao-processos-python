from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class EmailAutomation:
    def __init__(self, driver):
        """
        Inicializa a classe com o WebDriver.
        """
        self.driver = driver

    def clicar_na_pasta(self, nome_pasta):
        """
        Clica na pasta especificada pelo título ou texto visível.
        """
        try:
            print(f"Procurando pela pasta: {nome_pasta} ...")
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
        except Exception as e:
            print(f"Erro ao acessar a pasta '{nome_pasta}': {e}")

    def clicar_no_email(self):
        """
        Clica no primeiro email da lista.
        """
        try:
            tr_element = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//tr[contains(@class, 'message')]"))
            )
            self.driver.execute_script("arguments[0].scrollIntoView(true);", tr_element)
            tr_element.click()
            print("Primeiro email da lista clicado com sucesso!")
        except Exception as e:
            print(f"Erro ao clicar no email: {e}")

    def clicar_email_e_baixar_anexo(self):
        """
        Verifica se o email é do mês corrente, baixa o anexo e vai para o próximo email.
        """
        try:
            print("Procurando emails e verificando condições...")
            emails = WebDriverWait(self.driver, 30).until(
                EC.presence_of_all_elements_located((By.XPATH, "//tr[contains(@class, 'message')]"))
            )
            for email in emails:
                # Verifica se o email está selecionado
                if "selected focused" in email.get_attribute("class"):
                    # Obtém a data do email
                    data_element = email.find_element(By.CLASS_NAME, "date")
                    data_email = data_element.text

                    # Valida se o email pertence ao mês corrente
                    if self.validar_data_mes_corrente(data_email):
                        print(f"Email da data {data_email} encontrado.")

                        # Abre o email
                        email.click()
                        WebDriverWait(self.driver, 20).until(
                            EC.presence_of_element_located((By.XPATH, "//span[@class='attachment-name']"))
                        )

                        # Tenta baixar o anexo
                        anexos = self.driver.find_elements(By.XPATH, "//span[@class='attachment-name']")
                        if anexos:
                            for anexo in anexos:
                                print("Baixando anexo...")
                                self.driver.execute_script("arguments[0].scrollIntoView(true);", anexo)
                                anexo.click()
                            print("Todos os anexos baixados com sucesso!")
                        else:
                            print("Nenhum anexo encontrado neste email.")
                    else:
                        print(f"Email com data {data_email} fora do mês corrente. Pulando...")
        except Exception as e:
            print(f"Erro durante o processo de verificar e baixar anexos: {e}")

    def validar_data_mes_corrente(self, data_email):
        """
        Verifica se a data do email está dentro do mês corrente.
        """
        from datetime import datetime
        # Obtem o mês corrente
        mes_corrente = datetime.now().strftime("%m")
        ano_corrente = datetime.now().strftime("%Y")

        # Supondo que o formato da data seja algo como "01 Jan 2023"
        try:
            data_formatada = datetime.strptime(data_email, "%d %b %Y")
            return data_formatada.strftime("%m") == mes_corrente and data_formatada.strftime("%Y") == ano_corrente
        except Exception as e:
            print(f"Erro ao validar a data: {e}")
            return False