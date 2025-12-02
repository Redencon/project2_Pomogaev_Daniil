"""Tables and data processing"""
# from .utils import load_metadata, save_metadata


def create_table(metadata, table_name, columns):
    if table_name in metadata:
        raise ValueError(f"Table {table_name} already exists")
    if columns[0][0] != "ID":
        columns = [("ID", "int")] + columns
    for column in columns:
        if column[1] not in ("int", "str", "bool"):
            raise ValueError(f"Invalid column type {column[1]}")
    metadata[table_name] = columns
    return metadata

def drop_table(metadata, table_name):
    if table_name not in metadata:
        raise ValueError(f"Table {table_name} does not exist")
    del metadata[table_name]
    return metadata

