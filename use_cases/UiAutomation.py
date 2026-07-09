import uiautomation as auto

class UiAutomation:
    def __init__(self) -> None:
        self.controls = {
            "Button": auto.ButtonControl,
            "Edit": auto.EditControl,
        }

    def find_element(self, screen: auto.Control, params: dict) -> auto.Control:
        """Captura um elemento. params: {automationid, classname, name, depth, type}"""
        if not params:
            raise ValueError("É obrigatória a passagem de no mínimo 1 parâmetro")

        control_class = self.controls.get(params.get("type"), auto.Control)
        if params.get("type") and control_class is auto.Control:
            raise ValueError(f"Tipo desconhecido: {params['type']}. "
                             f"Tipos válidos: {list(self.controls)}")

        kwargs = {"searchFromControl": screen}
        mapping = {
            "automationid": "AutomationId",
            "classname": "ClassName",
            "name": "Name",
            "depth": "searchDepth",
        }
        for key, uia_key in mapping.items():
            if params.get(key) is not None:
                kwargs[uia_key] = params[key]

        return control_class(**kwargs)
    
    def find_window(self, )
