import subprocess
import time
import psutil
from loguru import logger
from use_cases.PrintAutomation import PrintAutomation

class SubprocessPrograms:
    def __init__(self) -> None:
        self.program_in_execute = None
        self.name_of_program = None
        self.name_of_process = None
        self.printautomation = PrintAutomation()

    def run_program(self, name_of_program: str, name_of_process: str = None,
                    close_existing: bool = False, wait_existing: float = 0) -> bool:
        """Função para executar um programa no Windows
        :name_of_program: Nome do programa a ser executado (ex: 'calc.exe')
        :name_of_process: Nome do processo real quando difere do executado — apps UWP/stub
            materializam outro processo (ex: abrir 'calc.exe' resulta em 'CalculatorApp.exe').
            Quando informado, é usado para finalizar em close_existing e em kill_program.
        :close_existing: Se True, finaliza instâncias já em execução antes de abrir
            (usa name_of_process quando informado, senão name_of_program).
        :wait_existing: Tempo máximo (s) a aguardar o processo alvo aparecer antes de finalizá-lo.
            0 (padrão) não espera. Útil ao reabrir em sequência rápida um app stub/UWP que
            demora a materializar o processo real (evita matar 'antes do tempo')."""
        self.name_of_program = name_of_program
        self.name_of_process = name_of_process
        if close_existing:
            process_name = name_of_process or name_of_program
            if wait_existing:
                self._wait_for_process(process_name, timeout=wait_existing)
            self.kill_program_by_name(process_name=process_name)
        try:
            self.program_in_execute = subprocess.Popen(name_of_program)
            return True
        except Exception as error_x:
            logger.critical(f'O programa "{name_of_program}" não pôde ser executado\nError: {error_x}')
            self.printautomation.print_error()
            return False

    def kill_program(self, timeout: float = 5, force: bool = True) -> bool:
        """Finaliza o programa aberto por run_program.
        Se name_of_process foi informado (app UWP/stub cujo processo real difere do
        executado), finaliza por nome; caso contrário, finaliza pelo handle do Popen.
        :timeout: Tempo (s) a aguardar o processo encerrar (só aplicável ao encerrar por nome)
        :force: Se True, força o encerramento dos processos que não fecharem no timeout"""
        if self.name_of_process:
            return self.kill_program_by_name(self.name_of_process, timeout=timeout, force=force)
        if self.program_in_execute is None:
            logger.warning('Nenhum programa em execução para finalizar')
            return False
        try:
            self.program_in_execute.terminate()
            return True
        except Exception as error_x:
            logger.critical(f'O programa "{self.name_of_program}" não pôde ser finalizado\nError: {error_x}')
            self.printautomation.print_error()
            return False

    def kill_program_by_name(self, process_name: str, timeout: float = 5, force: bool = True) -> bool:
        """Função para finalizar um programa pelo nome do processo (útil para apps UWP/stub como CalculatorApp.exe)
        :process_name: Nome do processo a ser finalizado (ex: 'CalculatorApp.exe')
        :timeout: Tempo (s) a aguardar o processo encerrar após o terminate/kill
        :force: Se True, força o encerramento (.kill()) dos processos que não fecharem no timeout"""
        try:
            procs = [p for p in psutil.process_iter(['name']) if p.info['name'] == process_name]
            if not procs:
                logger.warning(f'Nenhum processo "{process_name}" encontrado em execução')
                return False
            for proc in procs:
                proc.terminate()
            _, alive = psutil.wait_procs(procs, timeout=timeout)
            if alive and force:
                for proc in alive:
                    proc.kill()
                psutil.wait_procs(alive, timeout=timeout)
            return True
        except Exception as error_x:
            logger.critical(f'O processo "{process_name}" não pôde ser finalizado\nError: {error_x}')
            return False

    def _wait_for_process(self, process_name: str, timeout: float = 5, interval: float = 0.2) -> bool:
        """Aguarda um processo aparecer em execução, com timeout (poll — evita sleep cego)
        :process_name: Nome do processo a aguardar (ex: 'CalculatorApp.exe')
        :timeout: Tempo máximo (s) de espera
        :interval: Intervalo (s) entre as verificações
        Retorna True se o processo apareceu dentro do timeout, False caso contrário."""
        fim = time.monotonic() + timeout
        while time.monotonic() < fim:
            if any(p.info['name'] == process_name for p in psutil.process_iter(['name'])):
                return True
            time.sleep(interval)
        self.printautomation.print_error()
        return False
    
    
