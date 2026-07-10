from os import makedirs
from loguru import logger
from use_cases.EnvManager import EnvManager

class PathManager:
    def __init__(self) -> None:
        self.envmanager = EnvManager()
        self.erros = {}
        self.verify_paths()
        if self.erros:
            raise OSError(f'Verificar os seguintes erros: {self.erros}')
        self.path_workbooks = self.envmanager.paths["workbooks"]

    def verify_paths(self) -> None:
        for _path in self.envmanager.paths.values():
            try:
                makedirs(_path, exist_ok=True)
            except Exception as error:
                logger.error(f'Diretório "{_path}" não criado | Erro: {error}')
                self.erros[_path] = error
