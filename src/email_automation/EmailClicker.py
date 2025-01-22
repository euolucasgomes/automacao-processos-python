from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class EmailClicker:
    def __init__(self, driver):
        """
        Inicializa a classe com o WebDriver.
        """
        self.driver = driver

    def clicar_no_email(self):
        """
        Localiza e clica no primeiro email na lista de mensagens.
        """
        try:
            print("Procurando o primeiro email clicável...")

            # Aguarda que o elemento esteja clicável
            tr_element = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//tr[contains(@class, 'message')]"))
            )

            # Role até o elemento e clique nele
            self.driver.execute_script("arguments[0].scrollIntoView(true);", tr_element)
            tr_element.click()

            print("Email clicado com sucesso!")
        except Exception as e:
            print(f"Erro ao clicar no email: {e}")