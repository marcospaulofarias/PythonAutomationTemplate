from os import getenv
from dotenv import load_dotenv
load_dotenv()

class EnvManager:
    """Gerencia as variáveis de ambiente necessárias para o funcionamento do sistema.
    A classe carrega as variáveis de ambiente do arquivo .env e verifica se todas as variáveis necessárias estão presentes.
    Caso alguma variável esteja ausente, uma exceção é levantada.
    """
    def __init__(self) -> None:
        self.workbooks_path = getenv("PATH_WORKBOOKS")
        env_vars = (self.workbooks_path,)
        if any(var is None for var in env_vars):
            raise EnvironmentError("Algumas variáveis de ambiente não foram definidas. "
                                   "Certifique-se de que todas as variáveis necessárias estão presentes no arquivo .env."
                                   )
        self.paths = {
            "workbooks": self.workbooks_path
        }
