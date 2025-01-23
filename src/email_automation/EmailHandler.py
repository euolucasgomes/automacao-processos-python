class EmailHandler:
    def __init__(self, driver):
        self.driver = driver
        self.searcher = EmailSearcher(driver)
        self.date_verifier = EmailDateVerifier(driver)
        self.attachment_downloader = EmailAttachmentDownloader(driver)
        self.navigator = EmailNavigator(driver)

    def processar_email(self, prefixo_pasta):
        try:
            link = self.searcher.localizar_email(prefixo_pasta)

            if link:
                self.driver.execute_script(
                    "arguments[0].scrollIntoView(true);", link)
                WebDriverWait(self.driver, 10).until(EC.visibility_of(link))
                WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable(link))
                self.driver.execute_script("arguments[0].click();", link)

                print(f"Email com prefixo '{
                      prefixo_pasta}' encontrado e aberto.")

                WebDriverWait(self.driver, 30).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//span[@class='attachment-name']"))
                )

                if self.date_verifier.verificar_data_email():
                    self.attachment_downloader.baixar_anexo()
                else:
                    print("Email fora do mês corrente. Ignorando.")

                self.navigator.voltar_pagina()
            else:
                print("Nenhum email com as condições especificadas foi encontrado.")
                self.navigator.voltar_pagina()
        except Exception as e:
            print(f"Erro durante o processo: {e}")
            self.navigator.voltar_pagina()
