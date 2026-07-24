from time import sleep
from use_cases.Browser import Browser

class BancoCentral:
    def __init__(self) -> None:
        self.browser = Browser(process_id="0000003", process_type="generate_report", process_machine="COOP_MACHINE_02", headless=True)
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

    def _open_converter_menu(self) -> None:
        # self.browser.get_site(url_site='https://www.bcb.gov.br/conversao/')
        # sleep(10)
        self.browser.element_response(
            method=self.browser.BY_METHODS["id"],
            element_id="button-converter-para",
            message_success="Menu de conversão aberto",
            message_error="Não foi possível abrir o menu de conversão",
            click=True
        )

    def _get_coin_options(self):
        return self.browser.elements_response(
            method=self.browser.by_methods["css_selector"],
            element_id="#moedaResultado1 a.dropdown-item",
            message_success="Opções de moedas capturadas com sucesso",
            message_error="Erro ao capturar as opções de moedas"
        )

    def get_all_coins(self) -> list:
        self.browser.get_site(url_site='https://www.bcb.gov.br/conversao/')
        self._open_converter_menu()
        coin_options = self._get_coin_options()
        coins = []
        for coin in coin_options:
            inner = coin.get_attribute("innerHTML") or coin.text
            coin_name = inner.strip()
            coins.append({
                "name": coin_name,
                "element": coin
            })
        self._open_converter_menu()
        return coins

    def select_coin_by_inner_html(self, coin_html: str):
        self._open_converter_menu()
        coin_options = self._get_coin_options()
        for coin in coin_options:
            inner = (coin.get_attribute("innerHTML") or coin.text).strip()
            if coin_html in inner:
                coin.click()
                result = self._get_result_convertion()
                return result
        raise RuntimeError(f"Moeda não encontrada com base em innerHTML: {coin_html}")

    def _get_result_convertion(self) -> str:
        resultado = bancocentral.browser.elements_response(method=bancocentral.browser.BY_METHODS["class_name"], 
                                                          element_id="col-12", 
                                                          message_success="ok", 
                                                          message_error="erro")
        return resultado[1].text

if __name__ == '__main__':
    bancocentral = BancoCentral()
    coins = bancocentral.get_all_coins()
    for coin in coins:
        print(coin["name"])
        conversao = bancocentral.select_coin_by_inner_html(coin_html=coin["name"])
        print(f'CONVERSAO: {conversao}')
