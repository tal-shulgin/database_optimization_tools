import re
import pandas as pd

sql_dir_path = "./sql/"
output_dir_path = "./output/"

# Function to read the SQL dump file
def read_sql_dump(file_path):
    with open(file_path, 'r') as file:
        return file.read()

# Function to parse the SQL dump and extract table and column information including comments
def parse_sql_dump(sql_dump):
    table_column_pattern = re.compile(
        r'CREATE TABLE `?(?P<table_name>[\w_]+)`?\s*\((?P<column_definitions>[\s\S]+?)\)\s*(ENGINE|;)',
        re.IGNORECASE
    )
    # Updated regex to include capturing column comments
    column_detail_pattern = re.compile(
        r'`(?P<column_name>[\w_]+)`\s+(?P<column_type>\w+\((\d+,\d+|\d+)\)|\w+)(?:\s+COMMENT\s+'r"'(?P<comment>[^']*)')?",
        re.IGNORECASE
    )

    tables_columns_comments = []
    for table_match in table_column_pattern.finditer(sql_dump):
        table_name = table_match.group('table_name')
        column_definitions = table_match.group('column_definitions')

        for column_match in column_detail_pattern.finditer(column_definitions):
            column_name = column_match.group('column_name')
            column_type = column_match.group('column_type')
            comment = column_match.group('comment') or ''  # Default to empty string if no comment
            tables_columns_comments.append((table_name, column_name, column_type, comment))

    return tables_columns_comments

# Function to create a summary DataFrame
def create_summary(tables_columns_comments):
    summary_df = pd.DataFrame(tables_columns_comments, columns=['Table Name', 'Column Name', 'Column Type', 'Comment'])
    return summary_df

# Path to your SQL dump file
file_path = 'optimized.sql'  # Replace with the path to your SQL dump file

# Reading, parsing, and summarizing the SQL dump
sql_dump = read_sql_dump(sql_dir_path + file_path)
tables_columns_comments = parse_sql_dump(sql_dump)
summary_df = create_summary(tables_columns_comments)

# Saving the summary to a CSV file
csv_file_path = output_dir_path + 'database_schema_summary.csv'  # Replace with your desired CSV file path
summary_df.to_csv(csv_file_path, index=False)

print(f"Summary saved to CSV file: {csv_file_path}")
