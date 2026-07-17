from time import sleep
from re import sub
from random import uniform
from pyautogui import keyDown
from use_cases.UiAutomationClass import UiAutomationClass
from use_cases.SubprocessPrograms import SubprocessPrograms
from use_cases.PathManager import PathManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from loguru import logger

class Browser(UiAutomationClass):
    """Esta classe serve para trabalha com automação web usando tanto UiAutomation como selenium.
    Usando ela é possível superar algumas limitações do selenium e vice e versa"""
    def __init__(self, process_id: str = None, process_type: str = None, process_machine: str = None) -> None:
        super().__init__(process_id=process_id, process_type=process_type, process_machine=process_machine)
        self.subprocessprograms = SubprocessPrograms()
        self.pathmanager = PathManager()
        self.driver = None

    def _open_browser(self) -> None:
        """Função privada para iniciar o browser edge.
        Nesta função já está incluída a verificação para evitar duplicidade de navegadores."""
        try:
            self.close_browser()
            options = webdriver.EdgeOptions()
            options.add_argument("--no-sandbox")
            options.add_argument("--start-maximized")
            self.driver = webdriver.Edge(options=options)
        except Exception as error_x:
            self.printautomation.print_error()
            logger.critical(f'Erro ao abrir o navegador\nERROR: {error_x}')
            raise RuntimeError("Erro ao abrir o navegador") from error_x

    def get_site(self, url_site: str = 'https://www.google.com') -> None:
        """Função para acessar uma página web por meio de uma url completa url completa.
        certo: https://www.google.com
        errado: www.google.com (url incompleta)
        url_site: url completa para ser acessada"""
        self._open_browser()
        if self.driver:
            self.driver.get(url=url_site)

    def close_browser(self) -> None:
        """Função para fechar o navegador, mesmo que houve um erro ao fechar através do self.driver, é feita tentativa de encerramento pelo subprocess.
        Foi decido não manter como privado, pois assim o encerramento pode ser feito a qualquer momento com mais flexibilidade e controle"""
        if self.driver:
            try:
                self.driver.quit()
            except Exception as error_x:
                self.printautomation.print_error()
                logger.critical(f'Erro ao fechar o navegador\nError: {error_x}')
                raise RuntimeError('Erro ao fechar o navegador') from error_x
        else:
            try:
                self.subprocessprograms.kill_program_by_name(process_name="msedge.exe")
            except Exception as error_x:
                self.printautomation.print_error()
                logger.critical(f'Erro ao fechar o navegador pelo subprocesso\nError: {error_x}')

    def keyboard(self, element, word: str, key_down: bool, mask: bool, verify: bool = True, clean: bool = True, rem: str = None) -> None:
        if clean and element:
            element.clear()
        for caract in word:
            sleep(uniform(0.5, 1.5))
            element.send_keys(caract)
            if key_down is True:
                keyDown('right')
                element.click()
        if verify:
            if mask:
                if sub(r"\D", "", element.get_attribute('value')) != word:
                    self.keyboard(element, word, key_down, verify)
            elif not mask and rem is None:
                if element.get_attribute('value') != word:
                    self.keyboard(element, word, key_down, verify)
            elif rem is not None:
                if element.get_attribute('value').replace(rem, "") != word.replace(rem, ""):
                    self.keyboard(element, word, key_down, verify)
            return

    def element_response(self, metodo: By, identificador_elemento: str, message_success: str, message_error: str, repeticoes: int=100000, elemento: any = None, click: bool = False, update: bool = False):
        if elemento is None:
            for _ in range(repeticoes):
                if update and (_ + 1) % 20 == 0:
                    self.driver.refresh()
                    logger.info('Atualizou a página')
                logger.info(f'TENTATIVA {_ + 1} de {repeticoes}')
                try:
                    if click:
                        self.driver.find_element(metodo, identificador_elemento).click()
                        logger.info(message_success)
                        return True
                    else:
                        logger.info(message_success)
                        return self.driver.find_element(metodo, identificador_elemento)
                except Exception as error_x:
                    logger.error(f'{message_error}: {error_x}')
                sleep(1)
        else:
            for _ in range(repeticoes):
                logger.info(f'TENTATIVA {_ + 1} de {repeticoes}')
                try:
                    elemento.find_element(metodo, identificador_elemento)
                    logger.info(message_success)
                    return elemento.find_element(metodo, identificador_elemento)
                except Exception as error_x:
                    logger.error(f'{message_error}: {error_x}')
                sleep(1)
        return False
    
    def elements_response(self, metodo: By, identificador_elemento: str, message_success: str, message_error: str, repeticoes: int=100000, elemento: any = None):
        if elemento is None:
            for _ in range(repeticoes):
                logger.info(f'TENTATIVA {_ + 1} de {repeticoes}')
                try:
                    self.driver.find_elements(metodo, identificador_elemento)
                    logger.info(message_success)
                    return self.driver.find_elements(metodo, identificador_elemento)
                except Exception as error_x:
                    logger.error(f'{message_error}: {error_x}')
                sleep(1)
        else:
            for _ in range(repeticoes):
                logger.info(f'TENTATIVA {_ + 1} de {repeticoes}')
                try:
                    elemento.find_elements(metodo, identificador_elemento)
                    logger.info(message_success)
                    return elemento.find_elements(metodo, identificador_elemento)
                except Exception as error_x:
                    logger.error(f'{message_error}: {error_x}')
                sleep(1)
        return False
