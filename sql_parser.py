# sql_parser.py
import antlr4
from antlr4 import InputStream, CommonTokenStream, ParseTreeWalker

# Import your SQL grammar components
from AdvancedSQLLexer import AdvancedSQLLexer
from AdvancedSQLParser import AdvancedSQLParser
from AdvancedSQLListener import AdvancedSQLListener
from CaseInsensitiveStringStream import CaseInsensitiveStringStream

# Custom error handling
class SQLErrorReporter:
    def __init__(self):
        self.errors = []
    
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        self.errors.append({
            'line': line,
            'column': column,
            'msg': msg,
            'offendingSymbol': offendingSymbol.text
        })

def get_full_text(context):
    """Get original text from parser context"""
    if context.start is None or context.stop is None:
        return context.getText()
    return context.start.getInputStream().getText(
        context.start.start, context.stop.stop
    )

# Add custom method to parser context
antlr4.ParserRuleContext.GetFullText = get_full_text

class SQLTreeGenerator:
    def __init__(self):
        self.tree = None
        self.errors = []
    
    def parse(self, sql):
        # Setup parsing components
        input_stream = CaseInsensitiveStringStream(sql)
        lexer = AdvancedSQLLexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = AdvancedSQLParser(stream)
        
        # Configure error handling
        error_reporter = SQLErrorReporter()
        parser.removeErrorListeners()
        parser.addErrorListener(error_reporter)
        
        try:
            # Generate parse tree
            self.tree = parser.sqlStatement()
            self.errors = error_reporter.errors
            
            if self.errors:
                return None, self.errors
                
            return self.tree, None
            
        except Exception as e:
            return None, [{'msg': f"Parser error: {str(e)}"}]

    def get_tree_structure(self):
        """Get formatted tree structure"""
        if not self.tree:
            return ""
            
        return self._format_tree(self.tree, 0)

    def _format_tree(self, node, indent):
        """Recursive tree formatting"""
        result = "  " * indent + type(node).__name__
        if isinstance(node, antlr4.TerminalNode):
            result += f" ({node.getText()})"
        else:
            for child in node.getChildren():
                result += "\n" + self._format_tree(child, indent + 1)
        return result

# Example usage
if __name__ == "__main__":
    sample_query = """
    SELECT name, email FROM users
    LEFT JOIN orders ON users.id = orders.user_id
    WHERE age > 18
    ORDER BY name ASC
    LIMIT 10;
    """
    
    generator = SQLTreeGenerator()
    tree, errors = generator.parse(sample_query)
    
    if errors:
        print("Errors:")
        for error in errors:
            print(f"Line {error['line']}:{error['column']} - {error['msg']}")
    else:
        print("Parse Tree Structure:")
        print(generator.get_tree_structure())