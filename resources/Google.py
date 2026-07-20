from use_cases.Browser import Browser
from time import sleep

class Google:
    def __init__(self) -> None:
        self.browser = Browser(process_id="0000003", process_type="generate_report", process_machine="COOP_MACHINE_02")
        self._start_google()

    def _start_google(self) -> None:
        self.browser.get_site(url_site='https://www.google.com')

    def search_car(self) -> None:
        search_bar = self.browser.element_response(method=self.browser.by_methods["name"], element_id="q", message_success="Barra de pesquisa capturada com sucesso", message_error="Erro ao capturar a barra de pesquisa")
        search_button = self.browser.element_response(method=self.browser.by_methods["name"], element_id="btnK", message_success="Botão de pesquisa capturado com sucesso", message_error="Erro ao capturar o botão de pesquisa")
        search_bar.send_keys("car")
        self.browser.try_click(element=search_button)
        sleep(10)

if __name__ == '__main__':
    google = Google()
    google.search_car()
