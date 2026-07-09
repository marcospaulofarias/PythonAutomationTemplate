from use_cases.UiAutomationClass import UiAutomationClass

class Calculadora(UiAutomationClass):
    def __init__(self):
        super().__init__()

    def sum_1_1(self) -> bool | None:
        """Faz uma simples soma de 1 + 1 na calculador já aberta no Windows para "testar" o módulo"""
        self.window_calculadora = self.find_element(element_type="Window", params={"name": "Calculadora"})
        if self.window_calculadora:
            input(f"WINDOW_CALCULADORA: {self.window_calculadora}")
            button_1 = self.find_element(element_type="Button", params={})

        
