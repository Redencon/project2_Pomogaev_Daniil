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
    curmax_id = max([v['ID'] for v in metadata[table_name]['values']])
    dict_to_add =  {'ID': curmax_id+1}
    for value, col in zip(values, metadata[table_name]['columns'][1:]):
        if type(value) is not value_type_mapping[col[1]]:
            raise ValueError(f"Invalid value type {type(value)}")
        dict_to_add[col[0]] = value
    metadata[table_name]['values'].append(dict_to_add)
    return metadata

def clause_parser(clause):
    if clause is None:
        return None, None
    a, b = clause.split(" = ")
    b = ast.literal_eval(b)
    return (a, b)

def select(metadata, table_name, where=None):
    if table_name not in metadata:
        raise ValueError(f"Table {table_name} does not exist")
    col_to_check, val_to_check = clause_parser(where)
    values = metadata[table_name]['values']
    return [
        row for row in values if where is None or row[col_to_check] == val_to_check
    ]

def update(metadata, table_name, set_value, where=None):
    if table_name not in metadata:
        raise ValueError(f"Table {table_name} does not exist")
    a, b = clause_parser(where)
    x, y = clause_parser(set_value)
    for row in metadata[table_name]['values']:
        if where is None or row[a] == b:
            row[x] = y
    return metadata


def delete(metadata, where):
    a, b = clause_parser(where)
    metadata["values"] = [row for row in metadata["values"] if row[a] != b]
    return metadata
    
    

