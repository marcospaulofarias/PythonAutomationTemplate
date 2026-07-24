from resources.BancoCentral import BancoCentral
from resources.Calculadora import Calculadora

class TesteAutomacao:
    def __init__(self):
        self.banco_central = BancoCentral()
        self.calculadora = Calculadora()

    def get_data_bc(self):
        """Obtém a cotação do dólar do site do Banco Central e realiza uma multiplicação usando a calculadora."""
        dolar_value = self.banco_central.get_dolar()
        print(f"Valor do dólar: {dolar_value}")
        value_multiplication = self.calculadora.multiply_dolar_value(multiply_valor="3,50", dolar_value=dolar_value)
        print(f"Resultado da multiplicação: {value_multiplication}")
        value_multiplication = self.calculadora.multiply_dolar_value(multiply_valor="7", dolar_value=dolar_value)
        print(f"Resultado da multiplicação: {value_multiplication}")

if __name__ == "__main__":
    teste_automacao = TesteAutomacao()
    teste_automacao.get_data_bc()
