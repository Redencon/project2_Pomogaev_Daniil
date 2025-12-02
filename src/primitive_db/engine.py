"""Running the app on the command line"""
import shlex

import prompt

from .core import create_table, drop_table
from .utils import DEFAULT_META_FILE, load_metadata, save_metadata

HELP_TEXT = """
<command> create_table <имя_таблицы> <столбец1:тип> <столбец2:тип> .. - создать таблицу
<command> list_tables - показать список всех таблиц
<command> drop_table <имя_таблицы> - удалить таблицу
<command> exit - выйти из программы
<command> help - справочная информация
"""

def run():
    while True:
        metadata = load_metadata(DEFAULT_META_FILE)
        user_inp = get_command()
        if not user_inp:
            continue
        command, *args = shlex.split(user_inp)
        try:
            match command:
                case "exit":
                    break
                case "help":
                    print(HELP_TEXT)
                    continue
                case "create_table":
                    table_name, *columns_inp = args
                    columns = []
                    for column in columns_inp:
                        a, b = column.split(":")
                        columns.append((a, b))
                    create_table(metadata, table_name, columns)
                case "drop_table":
                    table_name = args[0]
                    drop_table(metadata, table_name)
                case "list_tables":
                    print(*metadata.keys())
                case _:
                    print(
                        "Unknown command. "
                        "Используйте help чтобы узнать список комманд."
                    )
        except Exception as e:
            print(e)
            continue

        save_metadata(DEFAULT_META_FILE, metadata)

def get_command():
    return prompt.string("Введите команду: ")
