"""Running the app on the command line"""
import shlex
from typing import Any

import prompt

from .core import create_table, delete, drop_table, info, insert, select, update
from .utils import DEFAULT_META_FILE, load_metadata, save_metadata

HELP_TEXT = """
<command> create_table <имя_таблицы> (<столбец1>:<тип1>, <столбец2>:<тип2>, ...) \
- создать таблицу.
<command> drop_table <имя_таблицы> - удалить таблицу.
<command> list_tables - вывести список таблиц.
<command> insert into <имя_таблицы> values (<значение1>, <значение2>, ...) \
- создать запись.
<command> select from <имя_таблицы> where <столбец> = <значение> \
- прочитать записи по условию.
<command> select from <имя_таблицы> - прочитать все записи.
<command> update <имя_таблицы> set <столбец1> = <новое_значение1> \
where <столбец_условия> = <значение_условия> - обновить запись.
<command> delete from <имя_таблицы> where <столбец> = <значение> - удалить запись.
<command> info <имя_таблицы> - вывести информацию о таблице.
<command> exit - выход из программы
<command> help - справочная информация
"""

def print_rows(rows: list[dict[str, Any]]):
    print("\n".join([
        ", ".join([
            f"{k}: {v}" for k, v in row.items()
        ])
        for row in rows
    ]))
    

def run():
    # cacher = create_cacher()
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
                case "insert":
                    if args[0] != "into":
                        raise ValueError("Unknown syntax for INSERT command")
                    table_name = args[1]
                    if args[2] != "values":
                        raise ValueError("Unknown syntax for INSERT command")
                    values = args[3:]
                    metadata = insert(metadata, table_name, values)
                case "select":
                    if args[0] != "from":
                        raise ValueError("Unknown syntax for SELECT command")
                    table_name = args[1]
                    if "where" not in args:
                        rows = select(metadata, table_name)
                        # rows = select(metadata, table_name)
                        print_rows(rows)
                    else:
                        clause = " ".join(args[3:6])
                        rows = select(metadata, table_name, clause)
                        # rows = select(metadata, table_name, clause)
                        print_rows(rows)
                case "update":
                    table_name = args[0]
                    if args[1] != "set":
                        raise ValueError("Unknown syntax for UPDATE command")
                    set_clause = " ".join(args[2:5])
                    if "where" not in args:
                        metadata = update(metadata, table_name, set_clause)
                    else:
                        where_clause = " ".join(args[6:9])
                        metadata = update(
                            metadata, table_name, set_clause, where_clause
                        )
                case "delete":
                    if args[0] != "from":
                        raise ValueError("Unknown syntax for DELETE command")
                    table_name = args[1]
                    clause = " ".join(args[3:6])
                    metadata = delete(metadata, table_name, clause)
                case "info":
                    table_name = args[0]
                    info(metadata, table_name)
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
