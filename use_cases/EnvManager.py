from os import getenv
from dotenv import load_dotenv
load_dotenv()

class EnvManager:
    """Gerencia as variáveis de ambiente necessárias para o funcionamento do sistema."""
    def __init__(self) -> None:
        workbooks_path = getenv("PATH_WORKBOOKS")
        if not workbooks_path:
            raise EnvironmentError(
                "Variável de ambiente PATH_WORKBOOKS não definida. "
                "Defina PATH_WORKBOOKS no arquivo .env ou no ambiente do sistema."
            )

        self.paths = {
            "workbooks": workbooks_path
        }
