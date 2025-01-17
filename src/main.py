from banco_dados import BancoDeDados
from email_automation.EmailAutomation import EmailAutomation
from email_automation.WebDriver import WebDriver
from email_automation.Login import Login
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()
email = os.getenv("EMAIL")
password = os.getenv("PASSWORD")

def main():
    # Inicializa o WebDriver
    webdriver_instance = WebDriver()
    driver = webdriver_instance.iniciar_webdriver()

    # Inicializa as classes
    login = Login(driver)
    email_automation = EmailAutomation(driver)
    banco = BancoDeDados()

    try:
        # Realiza login
        login.realizar_login(email, password)

        # Processa as pastas do banco de dados
        while True:
            pasta = banco.buscar_proxima_pasta()
            if not pasta:
                print("Todas as pastas foram processadas!")
                break

            pasta_id, nome_pasta = pasta
            print(f"Processando pasta: {nome_pasta}")

            try:
                email_automation.clicar_na_pasta(nome_pasta)
                email_automation.clicar_email_e_baixar_anexo()
                banco.marcar_pasta_concluida(pasta_id)
            except Exception as e:
                print(f"Erro ao processar a pasta '{nome_pasta}': {e}")

    except Exception as e:
        print(f"Erro inesperado durante o processamento: {e}")
    finally:
        banco.fechar_conexao()
        print("Conexão com o banco de dados fechada.")
        print("Feche o navegador manualmente.")

if __name__ == "__main__":
    main()