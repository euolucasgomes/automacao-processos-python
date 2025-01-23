from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime

class EmailDateVerifier:
    def __init__(self, driver):
        self.driver = driver

    def verificar_data_email(self):
        try:
            data_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//span[contains(@class, 'text-nowrap')]")
            ))
            data_texto = data_element.text.strip()

            mes_corrente = datetime.now().strftime("%m")
            ano_corrente = datetime.now().strftime("%Y")

            data_email = datetime.strptime(data_texto.split(" ")[0], "%Y-%m-%d")

            return data_email.strftime("%m") == mes_corrente and data_email.strftime("%Y") == ano_corrente
        except Exception as e:
            print(f"Erro ao verificar a data do email: {e}")
            return False