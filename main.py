#!/usr/bin/env python
# Coding: utf-8
# Author: Samsepi0l

from colorama import init, Fore, Style


def print_title():
    title = Fore.GREEN + r"""

██████╗  ██████╗ ██╗      █████╗ ██████╗ ██████╗ ███████╗ █████╗ ██████╗       ██████╗  ██████╗ ████████╗
██╔══██╗██╔═══██╗██║     ██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗██╔══██╗      ██╔══██╗██╔═══██╗╚══██╔══╝
██████╔╝██║   ██║██║     ███████║██████╔╝██████╔╝█████╗  ███████║██████╔╝█████╗██████╔╝██║   ██║   ██║   
██╔═══╝ ██║   ██║██║     ██╔══██║██╔══██╗██╔══██╗██╔══╝  ██╔══██║██╔══██╗╚════╝██╔══██╗██║   ██║   ██║   
██║     ╚██████╔╝███████╗██║  ██║██║  ██║██████╔╝███████╗██║  ██║██║  ██║      ██████╔╝╚██████╔╝   ██║   
╚═╝      ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝      ╚═════╝  ╚═════╝    ╚═╝   
                                                                                                         
""" + Style.RESET_ALL
    version_info = Style.BRIGHT + Fore.GREEN + """
    [PolarBear-Bot v1.0.1] [Release 1.0]
    Build: [2024-12-15] [linux/amd64] [RELEASE/__unknown__]
    Compiler Version: python version 3.12.4 linux/amd64
    Author: [Samsepi0l]
""" + Style.RESET_ALL 
    print(title)
    print(version_info)


if __name__ == '__main__':
    init(autoreset=True)
    print_title()