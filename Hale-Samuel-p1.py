from sly import Lexer

class DLangLexer(Lexer):
    # Set of token names
    # nothing, int, double, bool, string, class, interface, null, this, extends, implements, for, while, if, else, return, break, new, ArrayInstance, Output, InputInt, InputLine
    tokens = { NOTHING, INT, DOUBLE_KEYWORD, BOOL, STRING_KEYWORD, CLASS, INTERFACE, NULL, THIS, EXTENDS, IMPLEMENTS, FOR, WHILE, IF, ELSE, RETURN, BREAK, NEW, ARRAYINSTANCE, OUTPUT, INPUTINT, INPUTLINE, ID, BOOLEAN, INTEGER, DOUBLE, STRING, COMMENT, PLUS, MINUS, TIMES, DIVIDE, MOD, LT, LE, GT, GE, EQ, EQEQ, NE, AND, OR, NOT, SEMI, COMMA, DOT, LBRACK, RBRACK, LPAREN, RPAREN, LBRACE, RBRACE }

    # String containing ignored characters
    ignore = ' \t'

    # Regular expression rules for tokens
    NOTHING = r'nothing'
    INT = r'int'
    DOUBLE_KEYWORD = r'double'
    BOOL = r'bool'
    STRING_KEYWORD = r'string'
    CLASS = r'class'
    INTERFACE = r'interface'
    NULL = r'null'
    THIS = r'this'
    EXTENDS = r'extends'
    IMPLEMENTS = r'implements'
    FOR = r'for'
    WHILE = r'while'
    IF = r'if'
    ELSE = r'else'
    RETURN = r'return'
    BREAK = r'break'
    NEW = r'new'
    ARRAYINSTANCE = r'ArrayInstance'
    OUTPUT = r'Output'
    INPUTINT = r'InputInt'
    INPUTLINE = r'InputLine'
    ID = r'[a-zA-Z_][a-zA-Z_0-9]{0,49}'
    BOOLEAN = r'True|False'
    INTEGER = r'\d+'
    DOUBLE = r'\d+\.\d*([Ee][+-]?\d+)?'
    STRING = r'\".*?\"'
    COMMENT = r'//.*|/\*(.|\n)*?\*/'

    # Special characters
    PLUS = r'\+'
    MINUS = r'-'
    TIMES = r'\*'
    DIVIDE = r'/'
    MOD = r'%'
    LT = r'<'
    LE = r'<='
    GT = r'>'
    GE = r'>='
    EQ = r'='
    EQEQ = r'=='
    NE = r'!='
    AND = r'&&'
    OR = r'\|\|'
    NOT = r'!'
    SEMI = r';'
    COMMA = r','
    DOT = r'\.'
    LBRACK = r'\['
    RBRACK = r'\]'
    LPAREN = r'\('
    RPAREN = r'\)'
    LBRACE = r'\{'
    RBRACE = r'\}'

    # Ignored pattern
    ignore_newline = r'\n+'

    # Extra action for newlines
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    # Error handling rule
    def error(self, t):
        print("Illegal character '%s'" % t.value[0])
        self.index += 1
        
if __name__ == '__main__':
    lexer = DLangLexer()
    env = {}
    while True:
        try:
            text = input('dlang > ')
        except EOFError:
            break
        if text:
            lex = lexer.tokenize(text)
            for token in lex:
                print(token)
        else:
            continue