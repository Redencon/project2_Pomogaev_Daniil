import prompt

HELP_TEXT = """
<command> exit - выйти из программы
<command> help - справочная информация
"""

def get_command():
    return prompt.string("Введите команду: ")

def execute_command(command):
    if command == "exit":
        return False
    elif command == "help":
        print(HELP_TEXT)
        return True