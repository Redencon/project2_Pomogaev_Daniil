"""Tables and data processing"""
# from .utils import load_metadata, save_metadata
import ast

value_type_mapping: dict[str, type] = {
    "int": int,
    "str": str,
    "bool": bool,
}


def create_table(metadata, table_name, columns):
    if table_name in metadata:
        raise ValueError(f"Table {table_name} already exists")
    if len(columns) == 0:
        raise ValueError("No columns specified")
    if columns[0][0] != "ID":
        columns = [("ID", "int")] + columns
    for column in columns:
        if column[1] not in ("int", "str", "bool"):
            raise ValueError(f"Invalid column type {column[1]}")
    metadata[table_name] = {'columns': columns, 'values': []}
    return metadata

def drop_table(metadata, table_name):
    if table_name not in metadata:
        raise ValueError(f"Table {table_name} does not exist")
    del metadata[table_name]
    return metadata

def insert(metadata, table_name, values):
    if table_name not in metadata:
        raise ValueError(f"Table {table_name} does not exist")
    if len(values) != len(metadata[table_name]) - 1:
        raise ValueError("Invalid number of values")
    if metadata[table_name]['values']:
        curmax_id = max([v['ID'] for v in metadata[table_name]['values']])
    else:
        curmax_id = 0
    dict_to_add =  {'ID': curmax_id+1}
    for value, col in zip(values, metadata[table_name]['columns'][1:]):
        # if type(value) is not value_type_mapping[col[1]]:
        #     raise ValueError(f"Invalid value type {type(value)}")
        dict_to_add[col[0]] = value_type_mapping[col[1]](value)
    print(f"Добавлена строка: {dict_to_add}")
    metadata[table_name]['values'].append(dict_to_add)
    return metadata

def clause_parser(clause):
    if clause is None:
        return None, None
    a, b = clause.split(" = ")
    b = ast.literal_eval(b)
    return (a, b)

def get_col_type(metadata, table_name, col_name):
    col_pair = [col for col in metadata[table_name]['columns'] if col[0] == col_name]
    if not col_pair:
        raise ValueError(f"Column {col_name} does not exist")
    return value_type_mapping[col_pair[0][1]]

def select(metadata, table_name, where=None):
    if table_name not in metadata:
        raise ValueError(f"Table {table_name} does not exist")
    col_to_check, val_to_check = clause_parser(where)
    values = metadata[table_name]['values']
    if col_to_check:
        val_to_check = get_col_type(metadata, table_name, col_to_check)(val_to_check)
    return [
        row for row in values if where is None or row[col_to_check] == val_to_check
    ]

def update(metadata, table_name, set_value, where=None):
    if table_name not in metadata:
        raise ValueError(f"Table {table_name} does not exist")
    a, b = clause_parser(where)
    b = get_col_type(metadata, table_name, a)(b)
    x, y = clause_parser(set_value)
    y = get_col_type(metadata, table_name, x)(y)
    update_ids = []
    for row in metadata[table_name]['values']:
        if where is None or row[a] == b:
            row[x] = y
            update_ids.append(row['ID'])
    print("Обновлены строки с ID:", *update_ids)
    return metadata


def delete(metadata, table_name, where):
    a, b = clause_parser(where)
    b = get_col_type(metadata, table_name, a)(b)
    update_ids = [row["ID"] for row in metadata[table_name]["values"] if row[a] == b]
    metadata[table_name]["values"] = [
        row for row in metadata[table_name]["values"] if row[a] != b
    ]
    print("Удалены строки с ID:", *update_ids)
    return metadata


def info(metadata, table_name):
    if table_name not in metadata:
        raise ValueError(f"Table {table_name} does not exist")
    print(f"""
Таблица: {table_name}
Столбцы: {', '.join([col[0]+':'+col[1] for col in metadata[table_name]["columns"]])}
Количество записей: {len(metadata[table_name]["values"])}
""")
    
    

