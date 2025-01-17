from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import datetime
# import time


class WebDriver():

    def __init__(self):
        # Atributo para armazenar a instância do driver
        self.driver = None

    def iniciar_webdriver(self):
        """
        Inicializa o WebDriver com as configurações especificadas

        """

        options = Options()
        # Abre o navegador maximizado
        options.add_argument("--start-maximized")

        # Configura o serviço do WebDriver
        service = Service(ChromeDriverManager().install())

        # Cria a instância do WebDriver
        self.driver = webdriver.Chrome(service=service, options=options)
        print("WebDriver inicializado com sucesso!")
