class EmailNavigator:
    def __init__(self, driver):
        self.driver = driver

    def voltar_pagina(self):
        try:
            print("Tentando voltar para a lista de emails...")
            voltar_botao = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//div[@class='mail selected' and @role='button']"))
            )
            self.driver.execute_script(
                "arguments[0].scrollIntoView(true);", voltar_botao)
            voltar_botao.click()
            print("Retornou à lista de emails com sucesso.")
        except Exception as e:
            print(f"Erro ao tentar voltar para a lista de emails: {e}")
