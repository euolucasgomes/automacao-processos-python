from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime

class EmailSearcher:
    def __init__(self, driver):
        self.driver = driver

    def localizar_email(self, prefixo_pasta):
        print("Procurando pelo email com as condições especificadas...")
        emails = WebDriverWait(self.driver, 30).until(
            EC.presence_of_all_elements_located((By.XPATH, "//tr[contains(@class, 'message')]")
        ))

        for email in emails:
            if "selected focused" in email.get_attribute("class"):
                td_subject = email.find_element(By.CLASS_NAME, "subject")
                span_subject = td_subject.find_element(By.CLASS_NAME, "subject")
                link = span_subject.find_element(By.TAG_NAME, "a")
                href = link.get_attribute("href")

                if prefixo_pasta in href:
                    return link
        return None