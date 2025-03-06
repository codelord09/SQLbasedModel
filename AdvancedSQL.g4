grammar AdvancedSQL;

// =================== SQL STATEMENTS ===================
sqlStatement: (selectStatement | insertStatement | updateStatement | deleteStatement) SEMI? EOF;

// =================== SELECT ===================
selectStatement: 
    SELECT distinctClause? columnList FROM tableSource 
    (whereClause)? (groupByClause)? (havingClause)? (orderByClause)? (limitClause)?;

distinctClause: DISTINCT;

columnList: '*' | qualifiedColumn (COMMA qualifiedColumn)*;

qualifiedColumn: (IDENTIFIER DOT)? IDENTIFIER;

tableSource: tableName alias? (joinClause)*;

alias: AS? IDENTIFIER;

joinClause: joinType JOIN tableName alias? ON condition;

joinType: (INNER | (LEFT | RIGHT | FULL) OUTER? | CROSS | NATURAL)?;

whereClause: WHERE condition;

groupByClause: GROUP BY groupByItem (COMMA groupByItem)*;
groupByItem: qualifiedColumn | NUMBER;

havingClause: HAVING condition;

orderByClause: ORDER BY orderByItem (COMMA orderByItem)*;
orderByItem: qualifiedColumn (ASC | DESC)?;

limitClause: LIMIT NUMBER (OFFSET NUMBER)?;

// =================== INSERT ===================
insertStatement: INSERT INTO tableName (LPAREN columnList RPAREN)? VALUES valueList;
valueList: LPAREN literalValue (COMMA literalValue)* RPAREN;

// =================== UPDATE ===================
updateStatement: UPDATE tableName SET assignmentList (whereClause)?;
assignmentList: assignment (COMMA assignment)*;
assignment: IDENTIFIER EQUALS expression;

// =================== DELETE ===================
deleteStatement: DELETE FROM tableName (whereClause)?;

// =================== EXPRESSIONS & CONDITIONS ===================
condition: expression;
expression: 
    LPAREN expression RPAREN
    | expression AND expression
    | expression OR expression
    | NOT expression
    | predicate;

predicate: 
    qualifiedColumn operator value
    | qualifiedColumn (IN | BETWEEN) valueList
    | qualifiedColumn LIKE STRING
    | qualifiedColumn IS NULL
    | EXISTS LPAREN selectStatement RPAREN;

value: literalValue | qualifiedColumn;
operator: 
    EQUALS | NOT_EQUALS 
    | GREATER_THAN | LESS_THAN 
    | GREATER_EQUALS | LESS_EQUALS;

literalValue: STRING | NUMBER | NULL;

// =================== TOKEN DEFINITIONS ===================
// Keywords
SELECT: 'SELECT';
INSERT: 'INSERT';
INTO: 'INTO';
VALUES: 'VALUES';
UPDATE: 'UPDATE';
SET: 'SET';
DELETE: 'DELETE';
FROM: 'FROM';
WHERE: 'WHERE';
JOIN: 'JOIN';
ON: 'ON';
GROUP: 'GROUP';
BY: 'BY';
ORDER: 'ORDER';
HAVING: 'HAVING';
LIMIT: 'LIMIT';
OFFSET: 'OFFSET';
UNION: 'UNION';
DISTINCT: 'DISTINCT';
AS: 'AS';
IN: 'IN';
BETWEEN: 'BETWEEN';
LIKE: 'LIKE';
IS: 'IS';
NULL: 'NULL';
EXISTS: 'EXISTS';
ASC: 'ASC';
DESC: 'DESC';
LEFT: 'LEFT';
RIGHT: 'RIGHT';
FULL: 'FULL';
INNER: 'INNER';
OUTER: 'OUTER';
CROSS: 'CROSS';
NATURAL: 'NATURAL';
AND: 'AND';
OR: 'OR';
NOT: 'NOT';
ALL: 'ALL';

// Symbols
DOT: '.';
COMMA: ',';
SEMI: ';';
EQUALS: '=';
NOT_EQUALS: '!=' | '<>';
GREATER_THAN: '>';
LESS_THAN: '<';
GREATER_EQUALS: '>=';
LESS_EQUALS: '<=';
LPAREN: '(';
RPAREN: ')';

// Literals
IDENTIFIER: [a-zA-Z_][a-zA-Z0-9_]*;
NUMBER: [0-9]+;
STRING: '\'' .*? '\'';

// Whitespace
WS: [ \t\r\n]+ -> skip;

// Table name rule (added)
tableName: IDENTIFIER;