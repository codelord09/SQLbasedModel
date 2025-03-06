# sql_tree_builder.py
import sys
import json
from antlr4 import *
from AdvancedSQLLexer import AdvancedSQLLexer
from AdvancedSQLParser import AdvancedSQLParser
from antlr4.tree.Tree import TerminalNodeImpl
from anytree import Node, RenderTree
from CaseInsensitiveStringStream import CaseInsensitiveStringStream
from sql_parser import SQLTreeGenerator  # Assuming your previous SQL parser module

def main():
    query = input("Enter your SQL query: ")
    
    # Generate parse tree
    input_stream = CaseInsensitiveStringStream(query)
    lexer = AdvancedSQLLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = AdvancedSQLParser(stream)
    tree = parser.sqlStatement()
    root = to_anytree(tree, parser.ruleNames)

    # Process with SQL analyzer
    generator = SQLTreeGenerator()
    parsed_tree, errors = generator.parse(query)
    rule, data, plugin = analyze_sql(query)  # Implement your SQL analyzer

    # Write results to file
    with open("sql_analysis.txt", "w", encoding="utf-8") as f:
        f.write("=== SQL QUERY ===\n")
        f.write(query + "\n\n")
        
        f.write("=== PARSE TREE ===\n")
        for pre, _, node in RenderTree(root):
            f.write(f"{pre}{node.name}\n")
        
        f.write("\n=== SEMANTIC ANALYSIS ===\n")
        if errors:
            f.write("\nERRORS:\n" + "\n".join(errors) + "\n")
        else:
            f.write("\nQUERY STRUCTURE:\n")
            f.write(json.dumps(rule, indent=2, ensure_ascii=False) + "\n")
            
            f.write("\nDATA COMPONENTS:\n")
            f.write(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
            
            f.write("\nOPERATIONS INFO:\n")
            f.write(json.dumps(plugin, indent=2, ensure_ascii=False) + "\n")

    print("Analysis complete. Results saved to sql_analysis.txt")

def to_anytree(tree, rule_names, parent=None):
    """Convert SQL parse tree to anytree structure"""
    if isinstance(tree, TerminalNodeImpl):
        return Node(f"TOKEN: {tree.getText()}", parent=parent)
    node_name = f"RULE: {rule_names[tree.getRuleIndex()]}" if tree.getRuleIndex() >= 0 else "ROOT"
    node = Node(node_name, parent=parent)
    for child in tree.children:
        to_anytree(child, rule_names, parent=node)
    return node

def analyze_sql(query):
    """Sample SQL analyzer - implement your actual analysis logic here"""
    # This should be replaced with your actual SQL analysis implementation
    return {
        "query_type": "SELECT",
        "tables": ["users", "orders"],
        "columns": ["name", "email", "id", "user_id"],
        "joins": ["LEFT JOIN orders ON users.id = orders.user_id"],
        "filters": ["age > 18"]
    }, {}, {}

if __name__ == '__main__':
    main()