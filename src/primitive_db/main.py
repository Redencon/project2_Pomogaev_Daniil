#!/usr/bin/env python3
from .engine import execute_command, get_command


def main():
    print(" Первая попытка запустить проект!")
    s = True
    execute_command('help')
    while s:
        c = get_command()
        s = execute_command(c)




if __name__ == "__main__":
    main()