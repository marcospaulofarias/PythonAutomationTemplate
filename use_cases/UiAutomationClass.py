import time
from loguru import logger
import uiautomation as auto
from use_cases.PrintAutomation import PrintAutomation

class UiAutomationClass:
    def __init__(self, process_id: str = "", process_type: str = "", process_machine: str = "") -> None:
        self.printautomation = PrintAutomation(process_id=process_id,
                                               process_type=process_type,
                                               process_machine=process_machine)
                                               
        self.controls = {
            "Button": auto.ButtonControl,
            "Edit": auto.EditControl,
            "Window": auto.WindowControl
        }

        self.interactions = {
            "EditControl": lambda element, value=None: element.SendKeys(value),
            "ButtonControl": lambda element, value=None: element.GetInvokePattern().Invoke(),
        }

    def find_element(self, element_type: str, params: dict, screen: auto.WindowControl = None) -> auto.Control:
        """Captura um elemento. params: {automationid, classname, name, depth, type}"""
        if not self._verify_dict_params(dict_params=params):
            raise ValueError("É necessário passar no mínimo parâmetro")
        return self._try_element(element_type=element_type, params=params, screen=screen)

    def interact_element(self, element: auto.Control, value: str = None,
                         max_interact_seconds: float = 20, interval: float = 1.0) -> bool:
        """Tenta interagir com o elemento por max_interact_segundos, caso não consiga, erro"""
        method_element = self.interactions.get(element.ControlTypeName)
        if not method_element:
            logger.warning(f"Nenhuma interação definida para o tipo: {element.ControlTypeName}")
            return False

        deadline = time.monotonic() + max_interact_seconds
        last_error = None
        while time.monotonic() < deadline:
            try:
                if method_element(element, value) is not False:
                    return True
                last_error = "a interação retornou False"
            except Exception as error_x:
                last_error = error_x
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                break
            time.sleep(min(interval, remaining))
        logger.error(f"Não foi possível interagir com o elemento após {max_interact_seconds}s: {last_error}")
        self.printautomation.print_error(element_to_print=element)
        return False

    def _verify_dict_params(self, dict_params) -> bool:
        """Verifica se no mínimo 1 parâmetro foi passado"""
        if all(k is None or v is None for k, v in dict_params.items()):
            return False
        return True
    
    def _try_element(self, element_type: str, params: dict, max_search_seconds: float = 20, search_interval: float = 1.0, screen: auto.WindowControl = None) -> auto.Control:
        """Busca a janela, tentando por até max_search_seconds segundos, a cada search_interval segundos
        screen: Faz a busca a do elemento a partir da tela informada em screen"""
        if not element_type or element_type not in self.controls:
            raise ValueError("Obrigatório informar o tipo do elemento")
        control_cls = self.controls.get(element_type)
        element = control_cls(searchFromControl=screen,
                              ClassName=params.get("classname"),
                              Name=params.get("name"),
                              AutomationId=params.get("automationid"),
                              Depth=params.get("depth"))
        try:
            if element.Exists(maxSearchSeconds=max_search_seconds, searchIntervalSeconds=search_interval):
                return element
        except Exception as error_x:
            logger.warning(f"Erro ao buscar a janela: {error_x}")
        self.printautomation.print_error(element_to_print=screen)
        raise LookupError(f"{element_type} não encontrada após {max_search_seconds}s: {params}")
