
# Installation

Offer step-by-step instructions for setting up the project's environment:


macOS/Linux:
```Bash
pip install -r requirements.txt
```

Use code with caution. Learn more
Using a virtual environment: (1) Create a virtual environment (e.g., python -m venv venv) (2) Activate it (e.g., venv\Scripts\activate.bat on Windows) (3) Install requirements: pip install -r requirements.txt


## database_optimization_report_csv.py
This Python code is used to analyze and generate reports on optimizing a database storage capacity.

### Functionality
Parses SQL dump files to extract table and column data types
Compares original and optimized database structures
Calculates storage size of data types
Determines storage reduction for optimized data types
Generates markdown and CSV reports showing:
Storage size changes per column
Total storage reduction per table
Percentage storage improvement per table


### Usage
The main steps to use this are:

Place [original.sql] and [optimized.sql] SQL dump files in ./sql folder


Run script
Parsed SQL dumps and compared structures are processed
Reports are output to ./output folder:
database_optimization_report.csv - CSV format
Markdown format printed to console
The main functions that can be imported and reused are:

- parse_sql_dump() - Extract schema from SQL file
- compare_dumps() - Compare two database structures
- calculate_storage_reduction_and_improvement() - Analyze storage optimizations
- markdown_report() / write_to_csv() - Generate reports

So in summary, it automatizes analyzing database structure changes and quantifying storage optimizations between an original and optimized database schema. The output reports help identify and demonstrate the storage improvements from optimizing data types.


## database_schema_csv.py
 Here is a summary of what this Python code is doing:

### Functionality

- Reads an SQL dump file
- Parses the file to extract details on:
  - Tables
  - Columns
  - Data types
  - Comments
- Saves the extracted details into a Pandas DataFrame
- Converts the DataFrame into a CSV file

So in essence, it processes an SQL dump and generates a CSV summary of the database schema including additional comments. 

### Usage

The key steps to use it are:

1. Update SQL file path:
   ```
   file_path = 'optimized.sql'
   ```
2. Update output CSV file path:
   ```
   csv_file_path = './output/db_summary.csv'
   ```
3. Run script
4. CSV summary file is generated 

The main functions that can be reused:

- `read_sql_dump()` - Reads SQL file 
- `parse_sql_dump()` - Extract schema details
- `create_summary()` - Structure data into DataFrame

So in summary, this parses an SQL dump, extracts useful schema metadata, and outputs it as a CSV report. This can be helpful for quickly reviewing key details on a database without needing to pore through extensive SQL files.

The output CSV can serve as handy reference or documentation on the structure of a database.

## database_schema_diff_json.py
 Here is a summary of what this Python code is doing:

### Functionality

- Reads original and optimized SQL dump files
- Parses the SQL to extract database schema structure including:
  - Tables
  - Columns
    - Names
    - Data types 
  - Indexes
- Compares original vs optimized structures
- Detects differences in:
  - Column data types
  - Added/removed indexes
- Outputs structure differences between original and optimized

### Usage

The key steps to use it are:

1. Update SQL file paths:
   ```
   original_dump_path = 'original.sql'  
   optimized_dump_path = 'optimized.sql'
   ```
2. Run script
3. Structure differences are printed out 

The main functions that can be reused:

- `read_sql_dump()` - Reads SQL file
- `parse_sql_structure()` - Extract schema details 
- `compare_structures()` - Compare two schema structures

So in summary, it parses original and optimized database schemas from SQL dumps, compares them, and detects any structural changes in columns and indexes during optimization.

This can be helpful to analyze and document the specific database optimizations that were performed for performance gains or storage improvements.

The output clearly highlights the before and after structural differences, making it easy to understand the database changes and improvements at a glance.