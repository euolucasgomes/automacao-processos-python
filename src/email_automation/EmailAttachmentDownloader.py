from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime

class EmailAttachmentDownloader:
    def __init__(self, driver):
        self.driver = driver

    def baixar_anexo(self):
        try:
            anexo = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, "//span[@class='attachment-name']"))
            )
            self.driver.execute_script("arguments[0].scrollIntoView(true);", anexo)
            self.driver.execute_script("arguments[0].click();", anexo)
            print("Anexo encontrado e clicado com sucesso!")
        except Exception as e:
            print(f"Erro ao baixar o anexo: {e}")
