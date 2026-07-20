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
    BY_METHODS = {
        "name": By.NAME,
        "classname": By.CLASS_NAME,
        "class_name": By.CLASS_NAME,
        "xpath": By.XPATH,
        "id": By.ID,
        "css_selector": By.CSS_SELECTOR,
        "tag_name": By.TAG_NAME,
        "link_text": By.LINK_TEXT,
        "partial_link_text": By.PARTIAL_LINK_TEXT,
    }

    def __init__(self, process_id: str = None, process_type: str = None, process_machine: str = None) -> None:
        super().__init__(process_id=process_id, process_type=process_type, process_machine=process_machine)
        self.subprocessprograms = SubprocessPrograms()
        self.pathmanager = PathManager()
        self.driver = None
        self.by_methods = dict(self.BY_METHODS)

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

    def keyboard(self, element, word: str, key_down: bool, just_numbers: bool, verify: bool = True, clean: bool = True, word_to_remove: str = None) -> None:
        """Função para interagir com campos de texto editáveis.
        element: elemento web campo de texto editável para interagir.
        word: palavra ou frase para enviar ao elemento.
        key_down: método para "teclar a direita", alguns campos voltam o cursor como se "teclassem a esquerda".
        just_number: método para enviar apenas números ao elemento.
        verify: método para verificar se o elemento recebeu o valor correto.
        clean: método para limpar o elemento antes de enviar o valor a ele.
        word_to_remove: palavra para remover de word ao enviar para o elemento"""
        if clean and element:
            element.clear()
        for caract in word:
            sleep(uniform(0.5, 1.5))
            element.send_keys(caract)
            if key_down is True:
                keyDown('right')
                element.click()
        if verify:
            if just_numbers:
                if sub(r"\D", "", element.get_attribute('value')) != word:
                    self.keyboard(element, word, key_down, verify)
            elif not just_numbers and word_to_remove is None:
                if element.get_attribute('value') != word:
                    self.keyboard(element, word, key_down, verify)
            elif word_to_remove is not None:
                if element.get_attribute('value').replace(word_to_remove, "") != word.replace(word_to_remove, ""):
                    self.keyboard(element, word, key_down, verify)
            return

    def element_response(self, method: By, element_id: str, message_success: str, message_error: str, repetitions: int=100000, element: any = None, click: bool = False, update: bool = False):
        """Função para tentar n vezes encontrar um elemento web e retorna-lo.
        method: método usado para identificar o elemento [By.NAME, By.CLASSNAME, By.XPATH, etc...].
        element_id: identificador do elemento, exemplo: password, table, name_id_1, etc...
        message_success: mensagem de sucesso confirmando a captura do elemento.
        message_error: mensagem de erro mostrando que o elemento não foi capturado e o motivo.
        repetitons: número de tentativas para capturar o elemento.
        element: elemento que origina a captura de outro, exemplo element.find_element(...). -> janela_login.find_element(...).
        click: método para clicar no elemento assim que capturado.
        update: método para atualizar a página a cada 20 tentativas, as vezes um elemento quebrado se conserta apenas atualizando a página.
        """
        if element is None:
            for _ in range(repetitions):
                if update and (_ + 1) % 20 == 0:
                    self.driver.refresh()
                    logger.info('Atualizou a página')
                logger.info(f'TENTATIVA {_ + 1} de {repetitions}')
                try:
                    if click:
                        self.driver.find_element(method, element_id).click()
                        logger.info(message_success)
                        return True
                    else:
                        logger.info(message_success)
                        return self.driver.find_element(method, element_id)
                except Exception as error_x:
                    logger.error(f'{message_error}: {error_x}')
                sleep(1)
        else:
            for _ in range(repetitions):
                logger.info(f'TENTATIVA {_ + 1} de {repetitions}')
                try:
                    element.find_element(method, element_id)
                    logger.info(message_success)
                    return element.find_element(method, element_id)
                except Exception as error_x:
                    logger.error(f'{message_error}: {error_x}')
                sleep(1)
        return False
    
    def elements_response(self, method: By, element_id: str, message_success: str, message_error: str, repetitions: int=100000, element: any = None):
        """Função para tentar n vezes encontrar um elemento ou mais elementos web e retorna-los em forma de lista.
        method: método usado para identificar o(s) elemento(s) [By.NAME, By.CLASSNAME, By.XPATH, etc...].
        element_id: identificador do(s) elemento(s), exemplo: password, table, name_id_1, etc...
        message_success: mensagem de sucesso confirmando a captura do elemento.
        message_error: mensagem de erro mostrando que o elemento não foi capturado e o motivo.
        repetitons: número de tentativas para capturar o elemento.
        element: elemento que origina a captura de outro, exemplo element.find_element(...). -> janela_login.find_element(...).
        update: método para atualizar a página a cada 20 tentativas, as vezes um elemento quebrado se conserta apenas atualizando a página.
        """
        if element is None:
            for _ in range(repetitions):
                logger.info(f'TENTATIVA {_ + 1} de {repetitions}')
                try:
                    self.driver.find_elements(method, element_id)
                    logger.info(message_success)
                    return self.driver.find_elements(method, element_id)
                except Exception as error_x:
                    logger.error(f'{message_error}: {error_x}')
                sleep(1)
        else:
            for _ in range(repetitions):
                logger.info(f'TENTATIVA {_ + 1} de {repetitions}')
                try:
                    element.find_elements(method, element_id)
                    logger.info(message_success)
                    return element.find_elements(method, element_id)
                except Exception as error_x:
                    logger.error(f'{message_error}: {error_x}')
                sleep(1)
        return False
    
    def try_click(self, element, repetitions: int = 100000) -> bool:
        """Função para tentar n vezes clicar em um elemento web.
        element: elemento web para clicar.
        repetitions: número de tentativas para clicar no elemento."""
        for _ in range(repetitions):
            logger.info(f'TENTATIVA {_ + 1} de {repetitions}')
            try:
                element.click()
                logger.info('Clique realizado com sucesso')
                return True
            except Exception as error_x:
                logger.error(f'Erro ao tentar clicar no elemento: {error_x}')
            sleep(1)
        return False
