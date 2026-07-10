from pathlib import Path
from loguru import logger
from use_cases.PathManager import PathManager
from utils.date_time_utils import get_numeric_timestamp
import uiautomation as auto

class PrintAutomation:
    def __init__(self) -> None:
        self.pathmanager = PathManager()

    def _build_save_path(self) -> str:
        return str(Path(self.pathmanager.path_workbooks) / f"{get_numeric_timestamp()}.png")

    def print_error(self, element_to_print: auto.Control = None) -> None:
        try:
            target = element_to_print if element_to_print else auto.GetRootControl()
            target.CaptureToImage(savePath=self._build_save_path())
        except Exception as error:
            logger.warning(f"Falha ao capturar do elemento, tentando tela cheia: {error}")
            try:
                auto.GetRootControl().CaptureToImage(savePath=self._build_save_path())
            except Exception as error_fallback:
                logger.error(f"Falha também no print de tela cheia: {error_fallback}")
