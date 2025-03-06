# main.py
from sql_parser import parse_sql

sample_query = """
SELECT name, email FROM users
LEFT JOIN orders ON users.id = orders.user_id
WHERE age > 18
ORDER BY name ASC
LIMIT 10;
"""

stmt_type, data, errors = parse_sql(sample_query)

if errors:
    print("Errors:")
    for error in errors:
        print(f"- {error}")
else:
    print(f"Statement Type: {stmt_type}")
    print("Parsed Data:")
    print(f"- Tables: {data['tables']}")
    print(f"- Columns: {data['columns']}")
    print(f"- Conditions: {data['conditions']}")
    print(f"- Joins: {data['joins']}")