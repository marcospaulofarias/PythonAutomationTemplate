from use_cases.UiAutomationClass import UiAutomationClass
from use_cases.SubprocessPrograms import SubprocessPrograms

class Calculadora(UiAutomationClass):
    def __init__(self, name_of_program: str, name_of_process: str = None):
        super().__init__()
        self.name_of_program = name_of_program
        self.name_of_process = name_of_process
        self.subprocessprograms = SubprocessPrograms()
        program_in_execution = self.subprocessprograms.run_program(name_of_program=self.name_of_program, name_of_process=self.name_of_process)
        if not program_in_execution:
            raise RuntimeError(f'Programa "{self.name_of_program}" não executado')

    def sum_1_1(self) -> None:
        """Faz uma simples soma de 1 + 1 na calculadora já aberta no Windows para "testar" o módulo"""
        self.window_calculadora = self.find_element(element_type="Window", params={"name": "Calculadora"})
        button_1 = self.find_element(element_type="Button", params={"name": "Um"})
        self.interact_element(button_1)
        button_plus = self.find_element(screen=self.window_calculadora, element_type="Button", params={"name": "Mais"})
        self.interact_element(button_plus)
        button_1 = self.find_element(screen=self.window_calculadora, element_type="Button", params={"name": "Um"})
        self.interact_element(button_1)
        equal_to = self.find_element(screen=self.window_calculadora, element_type="Button", params={"name": "Igual a"})
        self.interact_element(equal_to)

    def close(self) -> bool:
        """Finaliza o programa aberto na construção."""
        return self.subprocessprograms.kill_program()

    def __enter__(self) -> "Calculadora":
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.close()
