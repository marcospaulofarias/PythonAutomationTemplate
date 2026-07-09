from loguru import logger
import uiautomation as auto

class UiAutomationClass:
    def __init__(self) -> None:
        self.controls = {
            "Button": auto.ButtonControl,
            "Edit": auto.EditControl,
            "Window": auto.WindowControl
        }
    
    def find_element(self, element_type: str, params: dict, screen: auto.WindowControl = None) -> auto.Control | None:
        """Captura um elemento. params: {automationid, classname, name, depth, type}"""
        if not self._verify_dict_params(dict_params=params):
            raise ValueError("É necessário passar no mínimo parâmetro")
        return self._try_element(element_type=element_type, params=params, screen=screen)

    def _verify_dict_params(self, dict_params) -> bool:
        """Verifica se no mínimo 1 parâmetro foi passado"""
        if all(k is None or v is None for k, v in dict_params.items()):
            return False
        return True
    
    def _try_element(self, element_type: str, params: dict, max_search_seconds: float = 20, search_interval: float = 1.0, screen: auto.WindowControl = None) -> auto.WindowControl | None:
        """Busca a janela, tentando por até max_search_seconds segundos, a cada search_interval segundos"""
        if not element_type or element_type not in self.controls:
            raise ValueError("Obrigatório informar o tipo do elemento")
        if not screen:
            element = self.controls.get(element_type)(ClassName=params.get("classname"),
                                                Name=params.get("name"),
                                                AutomationId=params.get("automationid"),
                                                Depth=params.get("depth"))
        else:
            element = screen.self.controls.get(element_type)(ClassName=params.get("classname"),
                                                Name=params.get("name"),
                                                AutomationId=params.get("automationid"),
                                                Depth=params.get("depth"))
        try:
            if element.Exists(maxSearchSeconds=max_search_seconds, searchIntervalSeconds=search_interval):
                return element
        except Exception as error_x:
            logger.warning(f"Erro ao buscar a janela: {error_x}")
        logger.error(f"Janela não encontrada após {max_search_seconds}s")
        return None
