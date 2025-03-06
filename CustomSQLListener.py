# CustomSQLListener.py
from antlr4 import *
from AdvancedSQLParser import AdvancedSQLParser
from AdvancedSQLListener import AdvancedSQLListener

class CustomSQLListener(AdvancedSQLListener):
    class ErrorReporter:
        def __init__(self):
            self.errors = []
            
        def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
            self.errors.append({
                'line': line,
                'column': column,
                'message': msg,
                'symbol': offendingSymbol.text
            })

    class BailErrorStrategy(BailErrorStrategy):
        pass

    def __init__(self):
        self.statement_type = None
        self.parsed_data = {
            'tables': [],
            'columns': [],
            'conditions': [],
            'joins': []
        }
        self.errors = []

    # Implement enter/exit methods for your grammar rules
    def enterSelectStatement(self, ctx: AdvancedSQLParser.SelectStatementContext):
        self.statement_type = 'SELECT'
        # Extract select components
        
    def enterInsertStatement(self, ctx: AdvancedSQLParser.InsertStatementContext):
        self.statement_type = 'INSERT'
        # Extract insert components

    # Add similar methods for update/delete/other statements