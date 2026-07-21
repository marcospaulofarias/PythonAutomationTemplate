import psutil
from loguru import logger
from use_cases.PrintAutomation import PrintAutomation

def kill_program_by_name(process_name: str, timeout: float = 5, force: bool = True, process_id: str = None, process_type: str = None, process_machine: str = None) -> bool:
    """Função para finalizar um programa pelo nome do processo (útil para apps UWP/stub como CalculatorApp.exe)
    :process_name: Nome do processo a ser finalizado (ex: 'CalculatorApp.exe')
    :timeout: Tempo (s) a aguardar o processo encerrar após o terminate/kill
    :force: Se True, força o encerramento (.kill()) dos processos que não fecharem no timeout"""
    printautomation = PrintAutomation(process_id=process_id, process_type=process_type, process_machine=process_machine)
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
        printautomation.print_error()
        logger.critical(f'O processo "{process_name}" não pôde ser finalizado\nError: {error_x}')
        raise RuntimeError(f'O processo "{process_name}" não pôde ser finalizado\nError: {error_x}') from error_x
