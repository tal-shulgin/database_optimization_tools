import re
import csv


def calculate_storage_size(data_type):
    # Function to calculate size for decimal types
    def decimal_size(precision, scale):
        if precision is None:
            precision = 10  # Default precision
        return (precision + 2) // 9 * 4 + (precision + 2) % 9

    # Mapping data types to their size calculation
    type_mapping = {
        'tinyint': lambda _: 1,
        'smallint': lambda _: 2,
        'mediumint': lambda _: 3,
        'int': lambda _: 4,
        'bigint': lambda _: 8,
        'decimal': decimal_size,
        'varchar': lambda length: length if length is not None else 255,  # Default length for varchar
        'text': lambda length: length if length is not None else 65535,  # Default length for text
        # Add other data types and their logic as needed
    }

    parts = data_type.split('(')
    base_type = parts[0].strip().lower()

    if base_type not in type_mapping:
        return 0  # Unknown or unhandled type

    if len(parts) == 2:
        size_info = parts[1].rstrip(')')
        if ',' in size_info:
            precision, scale = map(int, size_info.split(','))
            return type_mapping[base_type](precision, scale)
        else:
            size = int(size_info)
            return type_mapping[base_type](size)
    else:
        return type_mapping[base_type](None)  # Call with None for types without additional size info


def parse_data_type_changes(data):
    changes = {}
    for table, info in data.items():
        column_changes = info.get('column_changes', {})
        changes[table] = column_changes
    return changes


# Function to generate the Markdown report
def markdown_report(changes):
    report = ["# Database Optimization Report\n"]
    for table, cols in changes.items():
        report.append(f"## Table: {table}\n")
        report.append(
            "| Column Name | Original Data Type | Original Size (Bytes) | Optimized Data Type | Optimized Size (Bytes) | Reduction per Value (Bytes) |")
        report.append(
            "|-------------|--------------------|-----------------------|---------------------|------------------------|----------------------------|")

        total_reduction = 0
        for col, (original, optimized) in cols.items():
            original_size = calculate_storage_size(original)
            optimized_size = calculate_storage_size(optimized)
            reduction = original_size - optimized_size
            total_reduction += reduction
            report.append(f"| {col} | {original} | {original_size} | {optimized} | {optimized_size} | {reduction} |")

        report.append(f"\n**Total Capacity Reduction for {table}: {total_reduction} Bytes**\n")
        report.append("---\n")
    return '\n'.join(report)


# def markdown_report(changes):
#     report = ["# Database Optimization Report\n"]
#     for table, cols in changes.items():
#         report.append(f"## Table: {table}\n")
#         report.append(
#             "| Column Name | Original Data Type | Original Size (Bytes) | Optimized Data Type | Optimized Size (Bytes) | Reduction per Value (Bytes) |")
#         report.append(
#             "|-------------|--------------------|-----------------------|---------------------|------------------------|----------------------------|")
#
#         total_reduction = 0
#         for col, (original, optimized) in cols.items():
#             original_size = calculate_storage_size(original)
#             optimized_size = calculate_storage_size(optimized)
#             reduction = original_size - optimized_size
#             total_reduction += reduction
#             report.append(f"| {col} | {original} | {original_size} | {optimized} | {optimized_size} | {reduction} |")
#
#         report.append(f"\n**Total Capacity Reduction for {table}: {total_reduction} Bytes**\n")
#         report.append("---\n")
#     return '\n'.join(report)

# Function to parse SQL dump and extract table structures
def parse_sql_dump(file_path):
    with open(file_path, 'r') as file:
        dump = file.read()

    table_creations = re.findall(r'CREATE TABLE.*?;', dump, re.S)
    tables = {}

    for creation in table_creations:
        table_name = re.search(r'CREATE TABLE `(.*?)`', creation).group(1)
        columns = re.findall(r'`(.*?)` (.*?)\s', creation)
        tables[table_name] = {col[0]: col[1] for col in columns}

    return tables


# Function to compare original and optimized structures
def compare_dumps(original, optimized):
    changes = {}
    for table, cols in original.items():
        if table in optimized:
            for col, dtype in cols.items():
                if col in optimized[table] and dtype != optimized[table][col]:
                    if table not in changes:
                        changes[table] = {}
                    changes[table][col] = (dtype, optimized[table][col])
    return changes


def generate_report(changes):
    report = []
    for table, cols in changes.items():
        total_reduction = 0
        for col, (original, optimized) in cols.items():
            original_size = calculate_storage_size(original)
            optimized_size = calculate_storage_size(optimized)
            reduction = original_size - optimized_size
            total_reduction += reduction
            report.append([table, col, original, original_size, optimized, optimized_size, reduction])
        report.append([table, 'Total Reduction', '', '', '', '', total_reduction])
    return report


def calculate_storage_reduction_and_improvement(changes):
    results = {}
    for table, cols in changes.items():
        total_original_size = sum(calculate_storage_size(col[0]) for col in cols.values())
        total_optimized_size = sum(calculate_storage_size(col[1]) for col in cols.values())
        total_reduction = total_original_size - total_optimized_size
        improvement_percentage = (total_reduction / total_original_size) * 100 if total_original_size > 0 else 0
        results[table] = {
            'total_reduction': total_reduction,
            'improvement_percentage': improvement_percentage
        }
    return results


def write_to_csv(results, file_name):
    with open(file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Table Name', 'Total Capacity Reduction (Bytes)', 'Percentage Improvement (%)'])
        for table, data in results.items():
            writer.writerow([table, data['total_reduction'], data['improvement_percentage']])


# Main execution
sql_dir_path = "./sql/"
output_dir_path = "./output/"
original_dump = sql_dir_path + 'original.sql'
optimized_dump = sql_dir_path + 'optimized.sql'

original_structure = parse_sql_dump(original_dump)
optimized_structure = parse_sql_dump(optimized_dump)

changes = compare_dumps(original_structure, optimized_structure)

# Assuming 'changes' is obtained from compare_dumps(original_structure, optimized_structure)
results = calculate_storage_reduction_and_improvement(changes)
write_to_csv(results, output_dir_path + 'database_optimization_report.csv')

# md_report = markdown_report(changes)
# print(md_report)
