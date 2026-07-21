from use_cases.FilesManager import FilesManager

class Clean:
    def __init__(self) -> None:
        self.filesmanager = FilesManager()

    def clean_paths(self, paths_to_clean: list) -> None:
        """Limpa os diretórios especificados, removendo todos os arquivos dentro deles.
        
        :param paths_to_clean: Lista de caminhos completos dos diretórios a serem limpos."""
        self.filesmanager.clean_paths(paths_to_clean)

if __name__ == "__main__":
    # Exemplo de uso
    paths_to_clean = [
        "C:\\Zallpy\\PythonAutomationTemplate\\workbooks\\teste1",
        "C:\\Zallpy\\PythonAutomationTemplate\\workbooks\\teste2",
        "C:\\Zallpy\\PythonAutomationTemplate\\workbooks\\teste3",
        "C:\\Zallpy\\PythonAutomationTemplate\\workbooks\\teste4"
    ]
    cleaner = Clean()
    cleaner.clean_paths(paths_to_clean)