import re
import pandas as pd
sql_dir_path = "./sql/"

def read_sql_dump(file_path):
    with open(sql_dir_path + file_path, 'r') as file:
        return file.read()


def parse_sql_structure(sql_dump):
    table_pattern = re.compile(
        r'CREATE TABLE `?(?P<table_name>[\w_]+)`?\s*\((?P<columns_and_indexes>[\s\S]+?)\)\s*(ENGINE|;)',
        re.IGNORECASE
    )
    # Updated regex to correctly capture the full DECIMAL type
    column_pattern = re.compile(
        r'`(?P<column_name>[\w_]+)`\s+(?P<column_type>\w+\(\d+(,\d+)?\)|\w+)',
        re.IGNORECASE
    )
    index_pattern = re.compile(
        r'(PRIMARY KEY|UNIQUE KEY|KEY) `[\w_]+` \(`(?P<index_columns>[\w_, ]+)`\)',
        re.IGNORECASE
    )

    structure = {}
    for table_match in table_pattern.finditer(sql_dump):
        table_name = table_match.group('table_name')
        columns_and_indexes = table_match.group('columns_and_indexes')

        columns = {col.group('column_name'): col.group('column_type')
                   for col in column_pattern.finditer(columns_and_indexes)}
        indexes = [idx.group('index_columns')
                   for idx in index_pattern.finditer(columns_and_indexes)]

        structure[table_name] = {'columns': columns, 'indexes': indexes}

    return structure


def compare_structures(original_struct, optimized_struct):
    changes = {}
    all_tables = set(original_struct.keys()) | set(optimized_struct.keys())

    for table in all_tables:
        original_columns = original_struct.get(table, {}).get('columns', {})
        optimized_columns = optimized_struct.get(table, {}).get('columns', {})
        original_indexes = original_struct.get(table, {}).get('indexes', [])
        optimized_indexes = optimized_struct.get(table, {}).get('indexes', [])

        column_changes = {col: [original_columns.get(col), optimized_columns.get(col)]
                          for col in set(original_columns.keys()) | set(optimized_columns.keys())
                          if original_columns.get(col) != optimized_columns.get(col)}

        index_changes = {
            'removed': [idx for idx in original_indexes if idx not in optimized_indexes],
            'added': [idx for idx in optimized_indexes if idx not in original_indexes]
        }

        if column_changes or index_changes['removed'] or index_changes['added']:
            changes[table] = {'column_changes': column_changes, 'index_changes': index_changes}

    return changes


# Paths to your SQL dump files
original_dump_path = 'original.sql'  # Replace with the path to your original SQL dump file
optimized_dump_path = 'optimized.sql'  # Replace with the path to your optimized SQL dump file

# Reading and parsing the SQL dumps
original_sql_dump = read_sql_dump(original_dump_path)
optimized_sql_dump = read_sql_dump(optimized_dump_path)

original_structure = parse_sql_structure(original_sql_dump)
optimized_structure = parse_sql_structure(optimized_sql_dump)

# Comparing the structures and outputting the differences
structure_changes = compare_structures(original_structure, optimized_structure)
print(structure_changes)
