from os import getenv
from dotenv import load_dotenv
load_dotenv()

class EnvManager:
    def __init__(self) -> None:
        self.paths = {
            "workbooks": getenv("PATH_WORKBOOKS")
        }
