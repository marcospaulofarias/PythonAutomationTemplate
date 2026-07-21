from time import sleep
from use_cases.Browser import Browser

class BancoCentral:
    def __init__(self) -> None:
        self.browser = Browser(process_id="0000003", process_type="generate_report", process_machine="COOP_MACHINE_02")
        self._start_google()

    def _start_google(self) -> None:
        self.browser.get_site(url_site='https://www.bcb.gov.br/')

    def get_dolar(self) -> str:
        sleep(10)
        cotacao = self.browser.element_response(
            method=self.browser.by_methods["tag_name"],
            element_id="cotacao",
            message_success="Tag <cotacao> capturada com sucesso",
            message_error="Erro ao capturar a tag <cotacao>"
        )

        tables = self.browser.elements_response(
            method=self.browser.by_methods["css_selector"],
            element_id=".table.light",
            message_success="Tabela .table.light capturada com sucesso",
            message_error="Erro ao capturar a tabela .table.light",
            element=cotacao
        )

        spans = self.browser.elements_response(
            method=self.browser.by_methods["tag_name"],
            element_id="span",
            message_success="Spans capturados com sucesso",
            message_error="Erro ao capturar os spans",
            element=tables[0]
        )

        if len(spans) < 2:
            raise RuntimeError("Não há spans suficientes dentro da tabela")

        return spans[1].text

if __name__ == '__main__':
    bancocentral = BancoCentral()
    print(bancocentral.get_dolar())
