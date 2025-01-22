import sys
import os
import time
from email_automation.WebDriver import WebDriver
from email_automation.Login import Login
from email_automation.PastaAutomator import PastaAutomator  # Atualizado para usar a nova classe
from email_automation.EmailClicker import EmailClicker  # Importa a nova classe
from email_automation.EmailAttachmentDownloader import EmailAttachmentDownloader  # Importa a nova classe
from dotenv import load_dotenv
import logging

# Configuração do logging para ignorar mensagens de erro
logging.basicConfig(level=logging.ERROR)

# Adiciona o diretório principal ao PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Carrega variáveis de ambiente
load_dotenv()
email = os.getenv("EMAIL")
password = os.getenv("PASSWORD")

if __name__ == "__main__":
    # Inicializa o WebDriver
    webdriver_instance = WebDriver()
    driver = webdriver_instance.iniciar_webdriver()

    if driver:
        print("WebDriver inicializado com sucesso!")

        # Realiza login
        login_instance = Login(driver)
        if email and password:
            print("Iniciando o login...")
            login_instance.realizar_login(email, password)
            time.sleep(5)  # Aguarda após o login
        else:
            print("Erro: Variáveis de ambiente EMAIL e PASSWORD não configuradas.")
            driver.quit()
            sys.exit()

        # Caminho do banco de dados
        db_path = os.path.join(
            os.path.dirname(__file__), "data", "email_pastas.db"
        )

        # Instancia as classes PastaAutomator, EmailClicker e EmailAttachmentDownloader
        pasta_automator = PastaAutomator(driver, db_path)
        email_clicker = EmailClicker(driver)
        attachment_downloader = EmailAttachmentDownloader(driver)

        # Processa todas as pastas e clica no email em cada uma
        try:
            print("Iniciando o processamento de pastas e emails...")
            conn = pasta_automator.conectar_banco()
            if conn:
                pastas = pasta_automator.buscar_pastas(conn)
                if pastas:
                    for nome_pasta in pastas:
                        prefixo_pasta = nome_pasta.split(' - ')[0]  # Obtém o prefixo da pasta
                        pasta_automator.clicar_na_pasta(nome_pasta)
                        try:
                            email_clicker.clicar_no_email()
                            attachment_downloader.clicar_email_e_baixar_anexo(prefixo_pasta)
                        except Exception as e:
                            logging.error(f"Erro ao processar email na pasta '{nome_pasta}': {e}")
                        print("Aguardando 10 segundos antes de processar a próxima pasta...")
                        time.sleep(10)
                else:
                    print("Nenhuma pasta encontrada no banco de dados.")
                conn.close()
            else:
                print("Erro ao conectar ao banco de dados.")
        except Exception as e:
            logging.error(f"Erro durante o processamento: {e}")
        finally:
            # Encerramento seguro
            print("Processo concluído. O navegador permanecerá aberto por 30 segundos.")
            time.sleep(30)  # Permite inspeção manual
            driver.quit()
            print("Navegador encerrado.")
    else:
        print("Falha ao iniciar o WebDriver.")