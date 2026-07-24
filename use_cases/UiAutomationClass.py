import time
from loguru import logger
import uiautomation as auto
from use_cases.PrintAutomation import PrintAutomation
from use_cases.Initializator import Initializator
from utils.serial_killer import kill_all
from utils.config import load_apps_config

class UiAutomationClass:
    """Classe para automação de interface gráfica RPA usando uiautomation.

    :param process_id: Identificador do processo para logs e rastreamento.
    :param process_type: Tipo do processo para logs e rastreamento.
    :param process_machine: Nome da máquina para logs e rastreamento.
    """
    def __init__(self, process_id: str = "", process_type: str = "", process_machine: str = "", apps_needed_for_process=None) -> None:
        self.printautomation = PrintAutomation(process_id=process_id,
                                               process_type=process_type,
                                               process_machine=process_machine)

        if apps_needed_for_process is None:
            apps_needed_for_process = []

        self.initializator = None
        # Carregar apps a partir de config/apps.json e permitir overrides por .env
        apps_config = load_apps_config()
        self.apps = {}
        for key, cfg in apps_config.items():
            def make_runner(c):
                return lambda c=c: self._run_app(
                    name_of_program=c.get("name_of_program"),
                    name_of_process=c.get("name_of_process"),
                    close_existing=c.get("close_existing", False),
                    wait_existing=c.get("wait_existing", 0),
                    new_cmd=c.get("new_cmd", False)
                )
            self.apps[key] = make_runner(cfg)

        if apps_needed_for_process:
            self.initializator = Initializator(process_id=process_id, process_type=process_type, process_machine=process_machine)
            error_apps = []
            for app in apps_needed_for_process:
                if app in self.apps:
                    self.apps[app]()
                else:
                    logger.warning(f"Aplicativo '{app}' não definido na lista de apps disponíveis.")
                    error_apps.append(app)
            if error_apps:
                logger.error(f"Os seguintes aplicativos não foram encontrados na lista de apps disponíveis: {', '.join(error_apps)}")
                self.printautomation.print_error()
                kill_all()
                raise ValueError(f"Aplicativos não encontrados: {', '.join(error_apps)}")
                                               
        self.controls = {
            "Button": auto.ButtonControl,
            "Edit": auto.EditControl,
            "EditText": auto.TextControl,
            "Window": auto.WindowControl
        }

        self.interactions = {
            "EditControl": lambda element, value=None: element.SendKeys(value),
            "TextControl": lambda element, value=None: element.SendKeys(value),
            "ButtonControl": lambda element, value=None: element.GetInvokePattern().Invoke(),
        }

    def _run_app(self, name_of_program: str, name_of_process: str = None, close_existing: bool = False, wait_existing: float = 0, new_cmd: bool = False) -> bool:
        """Executa um aplicativo necessário para o processo.

        :param name_of_program: Nome do programa a ser executado (ex: 'calc.exe').
        :param name_of_process: Nome do processo real quando difere do executado (ex: 'CalculatorApp.exe').
            Exemplos de apps UWP/stub que materializam outro processo.
        :param close_existing: Se True, finaliza instâncias já em execução antes de abrir.
        :param wait_existing: Tempo máximo (s) a aguardar o processo alvo aparecer antes de finalizá-lo.
            0 não espera.
        :param new_cmd: Se True, abre o cmd.exe em uma nova janela de console (útil para manter o cmd aberto).
        :returns: True se o programa foi iniciado com sucesso, False caso contrário.
        """
        if not name_of_program:
            kill_all()
            raise ValueError("É necessário informar o nome do programa a ser executado.")
        if self.initializator is None:
            logger.critical("Initializator não inicializado. apps_needed_for_process deve ser fornecido para executar apps.")
            kill_all()
            raise RuntimeError("Initializator não inicializado. apps_needed_for_process deve ser fornecido para executar apps.")
        return self.initializator.run_program(
            name_of_program=name_of_program,
            name_of_process=name_of_process,
            close_existing=close_existing,
            wait_existing=wait_existing,
            new_cmd=new_cmd
        )

    def find_element(self, element_type: str, params: dict, screen: auto.WindowControl = None) -> auto.Control:
        """Captura um elemento usando os parâmetros fornecidos.

        :param element_type: Tipo do elemento a ser buscado (ex: 'Button', 'Edit', 'Window').
        :param params: Dicionário de parâmetros para a busca do elemento.
            Exemplos: automationid, classname, name, depth, type.
        :param screen: Elemento de tela a partir do qual a busca deve ser realizada.
        :returns: O controle encontrado.
        """
        if not self._verify_dict_params(dict_params=params):
            kill_all()
            raise ValueError("É necessário passar no mínimo parâmetro")
        return self._try_element(element_type=element_type, params=params, screen=screen)

    def interact_element(self, element: auto.Control, value: str = None,
                         max_interact_seconds: float = 20, interval: float = 1.0) -> bool:
        """Tenta interagir com o elemento até atingir o timeout.

        :param element: Elemento a ser interagido (uiautomation.Control).
        :param value: Valor a ser enviado (para EditControl/TextControl).
        :param max_interact_seconds: Tempo máximo (s) para tentar interagir com o elemento.
        :param interval: Intervalo (s) entre as tentativas de interação.
        :returns: True se a interação for bem-sucedida.
        :raises RuntimeError: se a interação falhar.
        """
        method_element = self.interactions.get(element.ControlTypeName)
        if not method_element:
            kill_all()
            raise ValueError(f"Nenhuma interação definida para o tipo: {element.ControlTypeName}")

        deadline = time.monotonic() + max_interact_seconds
        last_error = None
        while time.monotonic() < deadline:
            try:
                result = method_element(element, value)
                if result is False:
                    raise RuntimeError("A interação retornou False")
                return True
            except Exception as error_x:
                last_error = error_x
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                break
            time.sleep(min(interval, remaining))
        self.printautomation.print_error(element_to_print=element)
        logger.critical(f"Não foi possível interagir com o elemento após {max_interact_seconds}s: {last_error}")
        kill_all()
        raise RuntimeError(f"Não foi possível interagir com o elemento após {max_interact_seconds}s: {last_error}") from last_error

    def _verify_dict_params(self, dict_params) -> bool:
        """Verifica se foi passado ao menos um parâmetro válido.

        :param dict_params: Dicionário de parâmetros a ser verificado.
        :returns: True se existir ao menos um par chave/valor não nulo, False caso contrário.
        """
        if all(k is None or v is None for k, v in dict_params.items()):
            return False
        return True
    
    def _try_element(self, element_type: str, params: dict, max_search_seconds: float = 20, search_interval: float = 1.0, screen: auto.WindowControl = None) -> auto.Control:
        """Busca um elemento repetidamente até encontrá-lo ou estourar o timeout.

        :param element_type: Tipo do elemento a ser buscado (ex: 'Button', 'Edit', 'Window').
        :param params: Dicionário de parâmetros para a busca do elemento.
        :param screen: Elemento de tela a partir do qual a busca deve ser realizada.
        :param max_search_seconds: Tempo máximo (s) para tentar encontrar o elemento.
        :param search_interval: Intervalo (s) entre as tentativas de busca.
        :returns: O controle encontrado.
        """
        if not element_type or element_type not in self.controls:
            kill_all()
            raise ValueError("Obrigatório informar o tipo do elemento")
        control_cls = self.controls.get(element_type)
        element = control_cls(searchFromControl=screen,
                              ClassName=params.get("classname"),
                              Name=params.get("name"),
                              AutomationId=params.get("automationid"),
                              Depth=params.get("depth"))
        try:
            if element.Exists(maxSearchSeconds=max_search_seconds, searchIntervalSeconds=search_interval):
                if element_type == "Window":
                    element.SetActive()
                    element.SetFocus()
                elif screen:
                    screen.SetActive()
                    screen.SetFocus()
                return element
            kill_all()
            raise LookupError(f"{element_type} não encontrado: {params}")
        except Exception as error_x:
            self.printautomation.print_error(element_to_print=screen)
            logger.critical(f"Erro ao buscar {element_type}: {error_x}")
            kill_all()
            raise LookupError(f"Erro ao buscar {element_type}: {error_x}") from error_x
