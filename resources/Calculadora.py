from use_cases.UiAutomationClass import UiAutomationClass

class Calculadora(UiAutomationClass):
    """Automação da calculadora do Windows usando uiautomation."""

    def __init__(self, name_of_process: str = None):
        super().__init__(process_id="0000001", process_type="create_report", process_machine="COOP_MACHINE_01", apps_needed_for_process=["calculadora"])
        self.name_of_process = name_of_process

    def sum_1_1(self) -> None:
        """Realiza a soma 1 + 1 na calculadora do Windows.

        :returns: None.
        """
        self.window_calculadora = self.find_element(element_type="Window", params={"name": "Calculadora"})
        button_1 = self.find_element(element_type="Button", params={"name": "Um"})
        self.interact_element(button_1)
        button_plus = self.find_element(screen=self.window_calculadora, element_type="Button", params={"name": "Mais"})
        self.interact_element(button_plus)
        button_1 = self.find_element(screen=self.window_calculadora, element_type="Button", params={"name": "Um"})
        self.interact_element(button_1)
        equal_to = self.find_element(screen=self.window_calculadora, element_type="Button", params={"name": "Igual a"})
        self.interact_element(equal_to)

    def multiply_dolar_value(self, multiply_valor: str, dolar_value: str) -> str:
        """Multiplica um valor pela cotação do dólar exibida na calculadora.

        :param multiply_valor: Valor a ser multiplicado pelo dólar.
        :param dolar_value: Cotação do dólar a ser usada na operação.
        :returns: Texto exibido no resultado da calculadora após a operação.
        """
        self.window_calculadora = self.find_element(element_type="Window", params={"name": "Calculadora"})
        text_field = self.find_element(screen=self.window_calculadora, element_type="EditText", params={"automationid": "NormalOutput"})
        self.interact_element(text_field, value=dolar_value.replace(".", ","))
        button_multiply = self.find_element(screen=self.window_calculadora, element_type="Button", params={"name": "Multiplicar por"})
        self.interact_element(button_multiply)
        result_field = self.find_element(screen=self.window_calculadora, element_type="EditText", params={"automationid": "CalculatorResults"})
        self.interact_element(result_field, value=multiply_valor.replace(".", ","))
        equal_to = self.find_element(screen=self.window_calculadora, element_type="Button", params={"name": "Igual a"})
        self.interact_element(equal_to)
        result_text = self.find_element(screen=self.window_calculadora, element_type="EditText", params={"automationid": "CalculatorResults"})
        return result_text.Name

    def close(self) -> bool:
        """Finaliza o programa aberto na construção.

        :returns: True se o encerramento foi solicitado com sucesso.
        """
        return self.subprocessprograms.kill_program()

    def __enter__(self) -> "Calculadora":
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.close()

if __name__ == "__main__":
    with Calculadora(name_of_program="calc.exe", name_of_process="CalculatorApp.exe") as calc:
        calc.multiply_dolar_value("5.25", "3.50")
