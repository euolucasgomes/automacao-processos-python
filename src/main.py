import sys
import os
import time
from email_automation.WebDriver import WebDriver
from email_automation.Login import Login
from email_automation.EmailAutomation import EmailAutomation
from dotenv import load_dotenv

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

        # Instancia a classe EmailAutomation
        email_automation = EmailAutomation(driver)

        # Caminho do banco de dados
        db_path = os.path.join(
            os.path.dirname(__file__), "data", "email_pastas.db"
        )

        # Processa todas as pastas no banco de dados
        try:
            print("Iniciando o processamento de pastas...")
            email_automation.clicar_em_todas_as_pastas(db_path)
        except Exception as e:
            print(f"Erro durante o processamento das pastas: {e}")
        finally:
            # Encerramento seguro
            print("Processo concluído. O navegador permanecerá aberto por 30 segundos.")
            time.sleep(30)  # Permite inspeção manual
            driver.quit()
            print("Navegador encerrado.")
    else:
        print("Falha ao iniciar o WebDriver.")