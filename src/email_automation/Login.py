from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
# import datetime
# import time


class Login():

    def __init__(self, driver):
        """
        Inicializa a classe com o WebDriver
        """
        self.driver = driver

    def realizar_login(self, email, password):
        """
        Realiza o login no Hostinger Mail.
        """
        try:
            print("Abrindo a página de login...")
            self.driver.get("https://mail.hostinger.com/")

            email_field = WebDriverWait(self.driver, 20).until(
                EC.visibility_of_element_located((By.NAME, "_user"))
            )
            email_field.send_keys(email)

            password_field = WebDriverWait(self.driver, 20).until(
                EC.visibility_of_element_located((By.NAME, "_pass"))
            )
            password_field.send_keys(password)

            login_button = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[@type='submit']"))
            )
            login_button.click()

            WebDriverWait(self.driver, 20).until(
                EC.url_changes("https://mail.hostinger.com")
            )
            print("Login realizado com sucesso!")

        except Exception as e:
            print(f"Erro ao realizar login: {e}")


email = os.getenv("EMAIL")
password = os.getenv("PASSWORD")