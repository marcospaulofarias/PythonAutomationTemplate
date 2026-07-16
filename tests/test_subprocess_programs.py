from use_cases.SubprocessPrograms import SubprocessPrograms
from time import sleep

if __name__ == '__main__':
    subprocessprograms = SubprocessPrograms()

    subprocessprograms.run_program(name_of_program='calc.exe', name_of_process='CalculatorApp.exe')
    sleep(5)
    subprocessprograms.kill_program()
