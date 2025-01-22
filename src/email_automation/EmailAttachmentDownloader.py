from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime

class EmailAttachmentDownloader:
    def __init__(self, driver):
        """
        Inicializa a classe com o WebDriver.
        """
        self.driver = driver

    def clicar_email_e_baixar_anexo(self, prefixo_pasta):
        """
        Localiza o email desejado, verifica a data do mês corrente, e baixa o anexo se a condição for atendida.
        Após a execução, tenta voltar para a página anterior.
        """
        try:
            print("Procurando pelo email com as condições especificadas...")

            # Localiza todas as linhas de email
            emails = WebDriverWait(self.driver, 30).until(
                EC.presence_of_all_elements_located((By.XPATH, "//tr[contains(@class, 'message')]")
            ))

            encontrou_email = False

            for email in emails:
                # Verifica se a linha do email possui a classe 'message selected focused'
                if "selected focused" in email.get_attribute("class"):
                    # Verifica se há um 'td' com classe 'subject'
                    td_subject = email.find_element(By.CLASS_NAME, "subject")
                    # Verifica se há um 'span' com classe 'subject' dentro do 'td'
                    span_subject = td_subject.find_element(By.CLASS_NAME, "subject")
                    # Verifica se o 'a' dentro do 'span' contém o prefixo da pasta
                    link = span_subject.find_element(By.TAG_NAME, "a")
                    href = link.get_attribute("href")

                    if prefixo_pasta in href:
                        encontrou_email = True
                        # Role para o elemento e clique nele para abrir o email
                        self.driver.execute_script("arguments[0].scrollIntoView(true);", link)
                        WebDriverWait(self.driver, 10).until(EC.visibility_of(link))
                        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(link))
                        self.driver.execute_script("arguments[0].click();", link)

                        print(f"Email com prefixo '{prefixo_pasta}' encontrado e aberto: {href}")

                        # Aguarda o carregamento do email
                        WebDriverWait(self.driver, 30).until(
                            EC.presence_of_element_located((By.XPATH, "//span[@class='attachment-name']"))
                        )

                        # Verifica a data do email
                        if self.verificar_data_email():
                            # Localiza e clica no anexo
                            anexo = WebDriverWait(self.driver, 30).until(
                                EC.element_to_be_clickable((By.XPATH, "//span[@class='attachment-name']"))
                            )
                            self.driver.execute_script("arguments[0].scrollIntoView(true);", anexo)
                            self.driver.execute_script("arguments[0].click();", anexo)

                            print("Anexo encontrado e clicado com sucesso!")
                        else:
                            print("Email fora do mês corrente. Ignorando.")

                        # Tenta voltar à lista de emails
                        self.voltar_pagina()
                        return  # Encerra após concluir a tarefa

            if not encontrou_email:
                print("Nenhum email com as condições especificadas foi encontrado.")
                # Volta para a lista de emails, caso não encontre o email
                self.voltar_pagina()
        except Exception as e:
            print(f"Erro durante o processo: {e}")
            # Volta para a lista de emails, caso ocorra erro
            self.voltar_pagina()

    def verificar_data_email(self):
        """
        Verifica se a data do email está dentro do mês corrente.
        """
        try:
            # Localiza o elemento que contém a data
            data_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//span[contains(@class, 'text-nowrap')]")
            ))
            data_texto = data_element.text.strip()

            # Obtem o mês e o ano corrente
            mes_corrente = datetime.now().strftime("%m")
            ano_corrente = datetime.now().strftime("%Y")

            # Converte a data do email
            data_email = datetime.strptime(data_texto.split(" ")[0], "%Y-%m-%d")

            # Verifica se a data pertence ao mês e ano corrente
            if data_email.strftime("%m") == mes_corrente and data_email.strftime("%Y") == ano_corrente:
                return True
            else:
                return False
        except Exception as e:
            print(f"Erro ao verificar a data do email: {e}")
            return False

    def voltar_pagina(self):
        """
        Clica no elemento com class="mail selected" e role="button" para retornar à lista de emails.
        """
        try:
            print("Tentando voltar para a lista de emails...")
            voltar_botao = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@class='mail selected' and @role='button']"))
            )
            self.driver.execute_script("arguments[0].scrollIntoView(true);", voltar_botao)
            voltar_botao.click()
            print("Retornou à lista de emails com sucesso.")
        except Exception as e:
            print(f"Erro ao tentar voltar para a lista de emails: {e}")