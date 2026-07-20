from use_cases.Browser import Browser
from time import sleep

class BancoCentral:
    def __init__(self) -> None:
        self.browser = Browser(process_id="0000003", process_type="generate_report", process_machine="COOP_MACHINE_02")
        self._start_google()

    def _start_google(self) -> None:
        self.browser.get_site(url_site='https://www.bcb.gov.br/')

    def statistics(self) -> None:
        statistics_button = self.browser.element_response(method=self.browser.by_methods["id"], element_id="navbarDropdown3", message_success="Botão de estatísticas capturado com sucesso", message_error="Erro ao capturar o botão de estatísticas")
        self.browser.try_click(element=statistics_button)
        sleep(10)

if __name__ == '__main__':
    bancocentral = BancoCentral()
    bancocentral.statistics()
