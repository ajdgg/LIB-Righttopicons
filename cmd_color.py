# ! /usr/bin/env python
# coding=utf-8
import time
from colorama import init, Fore, Back, Style

init(autoreset=True)


class CmdColor:
    def __init__(self):
        pass

    def ccolor(self, state: str, text: str, color: str):
        t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        if color == 'red':
            print(Fore.RED + f'[{state}]' + Fore.RESET + " " + Fore.RED + t + Fore.RESET + " " + Fore.RED + text + Fore.RESET)
        elif color == 'green':
            print(Fore.GREEN + f'[{state}]' + Fore.RESET + " " + Fore.GREEN + t + Fore.RESET + " " + Fore.GREEN + text + Fore.RESET)
        elif color == 'blue':
            print(Fore.BLUE + f'[{state}]' + Fore.RESET + " " + Fore.BLUE + t + Fore.RESET + " " + Fore.BLUE + text + Fore.RESET)
        elif color == 'yellow':
            print(Fore.YELLOW + f'[{state}]' + Fore.RESET + " " + Fore.YELLOW + t + Fore.RESET + " " + Fore.YELLOW + text + Fore.RESET)

    def h_time(self, state, text):
        print(Fore.BLUE + f'[{state}]' + Fore.RESET + " " + Fore.BLUE + text + Fore.RESET)
