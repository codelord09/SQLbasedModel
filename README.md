# SQL-based Model Project

ANTLR4-based SQL parser with code tuning capabilities

## Features
- SQL grammar parsing
- Query analysis
- Parse tree visualization

## Setup
```bash
pip install -r requirements.txt
antlr4 -Dlanguage=Python3 AdvancedSQL.g4
```

## Usage
```python
python sql_tree_builder.py
```

## Grammar
See [AdvancedSQL.g4](AdvancedSQL.g4)