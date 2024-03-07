# -------------------------------------------------------------------------
# dlang-parser.py: DLang Syntax Analyzer
# Run with source file 
# -------------------------------------------------------------------------
import sys
from sly import Lexer, Parser

class DLangLexer(Lexer):
    # Initialize the lexer with a symbol table
    def __init__(self):
        self.IDENTIFIERs = { }

    # Define names of tokens
    tokens = {LE, GE, EQ, NE, AND, OR, INT, DOUBLE, STRING, IDENTIFIER, NOTHING, INTK, DOUBLEK, BOOL, BOOLK, STRINGK, INTERFACE, NULL, FOR, WHILE, IF, ELSE, RETURN, BREAK, ARRAYINSTANCE, OUTPUT, INPUTINT, INPUTLINE}
    
    # Single-character literals can be recognized without token names
    # If you use separate tokens for each literal, that is fine too
    literals = {'+', '-', '*', '/', '%', '<', '>', '=','!', ';', ',', '.', '[', ']','(',')','{','}'}
    
    # Specify things to ignore
    ignore = ' \t\r' # space, tab, and carriage return
    ignore_comment1= r'\/\*[^"]*\*\/' # c-style multi-line comment (note: test with input from file)
    ignore_comment = r'\/\/.*' # single line comment
    ignore_newline=r'\n+' # end of line

    # Specify REs for each token
    STRING = r'\"(.)*\"'
    DOUBLE = r'[0-9]+\.[0-9]*([E][+-]?\d+)?'
    INT = r'[0-9]+'
    EQ = r'=='
    NE = r'!='
    LE = r'<='
    GE = r'>='
    AND = r'&&' 
    OR =  r'\|\|'
    IDENTIFIER = r'[a-zA-Z_][a-zA-Z0-9_]{0,49}'

    # IDENTIFIER lexemes overlap with keywords.
    # To avoid confusion, we do token remaping.
    # Alternatively, you can specify each keywork before IDENTIFIER
    IDENTIFIER['nothing'] = NOTHING
    IDENTIFIER['int'] = INTK
    IDENTIFIER['double'] = DOUBLEK
    IDENTIFIER['string'] = STRINGK
    IDENTIFIER['bool'] = BOOLK
    IDENTIFIER['True'] = BOOL
    IDENTIFIER['False'] = BOOL
    IDENTIFIER['null'] = NULL
    IDENTIFIER['for'] = FOR
    IDENTIFIER['while'] = WHILE
    IDENTIFIER['if'] = IF
    IDENTIFIER['else'] = ELSE
    IDENTIFIER['return'] = RETURN
    IDENTIFIER['ArrayInstance'] = ARRAYINSTANCE
    IDENTIFIER['Output'] = OUTPUT
    IDENTIFIER['InputInt'] = INPUTINT
    IDENTIFIER['InputLine'] = INPUTLINE


    def error(self,t):
        print ("Invalid character '%s'" % t.value[0])
        self.index+=1

class DLangParser(Parser):

    tokens = DLangLexer.tokens

    def __init__(self):
        self.IDENTIFIERs = { }


    # Program -> Decl+
    @_('Decls')
    def Program(self, p): 
        print('Parsing completed successfully!') # If we get here with no issues, bottom-up parsing is successful!
        return p
    
    @_('Decl Decls ','Decl')
    def Decls(self, p):
        #print(p)
        return p
    

    # Decl -> VariableDecl
    @_('VariableDecl')
    def Decl(self, p):
        return p.VariableDecl

    # VariableDecl -> Variable;
    @_('Variable ";"')
    def VariableDecl(self, p):
        print ('Found VariableDecl')

    # Variable -> Type ident
    @_('Type IDENTIFIER')
    def Variable(self, p):
        return p

    # Type -> int | double | bool | string    
    @_('INTK', 'DOUBLEK', 'BOOLK', 'STRINGK')
    def Type(self, p):
        return p
    
    # FunctionDecl -> Type ident ( Formals ) StmtBlock | nothing ident ( Formals ) StmtBlock
    @_('Type IDENTIFIER "(" Formals ")" StmtBlock',
        'NOTHING IDENTIFIER "(" Formals ")" StmtBlock')
    def FunctionDecl(self, p):
         print('Found FunctionDecl')
         
    # Formals -> Variable+ | ε
    @_('Variable+',
        'ε')
    def Formals(self, p):
         return p
     
    # StmtBlock → { VariableDecl* Stmt* }
    @_(' "{" VariableDecl* Stmt* "}" ')
    def StmtBlock(self, p):
        print('Found StmtBlock')
        
    # Stmt → <Expr> ; | IfStmt | WhileStmt | ForStmt | BreakStmt | ReturnStmt | OutputStmt | StmtBlock
    @_('Expr ";"',
        'IfStmt',
        'WhileStmt',
        'ForStmt',
        'BreakStmt',
        'ReturnStmt',
        'OutputStmt',
        'StmtBlock')
    def Stmt(self, p):
        print('Found Stmt')
        
    # IfStmt → if ( Expr ) Stmt <else Stmt>
    @_('IF "(" Expr ")" Stmt ELSE Stmt',
        'IF "(" Expr ")" Stmt')
    def IfStmt(self, p):
        print('Found IfStmt')
        
    # WhileStmt → while ( Expr ) Stmt
    @_('WHILE "(" Expr ")" Stmt')
    def WhileStmt(self, p):
        print('Found WhileStmt')
        
    # ForStmt → for ( <Expr> ; Expr ; <Expr> ) Stmt
    @_('FOR "(" Expr ";" Expr ";" Expr ")" Stmt')
    def ForStmt(self, p):
        print('Found ForStmt')
        
    # ReturnStmt → return <Expr> ;
    @_('RETURN Expr ";"')
    def ReturnStmt(self, p):
        print('Found ReturnStmt')
        
    # BreakStmt → break ;
    @_('BREAK ";"')
    def BreakStmt(self, p):
        print('Found BreakStmt')
        
    # OutputStmt → Output ( Expr+, ) ;
    @_('OUTPUT "(" Expr+ "," ")" ";"')
    def OutputStmt(self, p):
        print('Found OutputStmt')
        
    # Expr → ident = Expr | Ident | Constant | Call | ( Expr ) | Expr+Expr | Expr -Expr | Expr *Expr | Expr/Expr | Expr % Expr | - Expr | Expr < Expr | Expr <= Expr | Expr > Expr | Expr>= Expr | Expr==Expr | Expr!=Expr | Expr && Expr | Expr || Expr | !Expr | InputInt ( ) | InputLine ( )
    @_('IDENTIFIER "=" Expr',
        'IDENTIFIER',
        'Constant',
        'Call',
        ' "(" Expr ")" ',
        'Expr "+" Expr',
        'Expr "-" Expr',
        'Expr "*" Expr',
        'Expr "/" Expr',
        'Expr "%" Expr',
        '- Expr',
        'Expr "<" Expr',
        'Expr "<=" Expr',
        'Expr ">" Expr',
        'Expr ">=" Expr',
        'Expr "==" Expr',
        'Expr "!=" Expr',
        'Expr "&&" Expr',
        'Expr "||" Expr',
        '! Expr',
        'INPUTINT "(" ")"',
        'INPUTLINE "(" ")"')
    def Expr(self, p):
        print('Found Expr')
        
    # Call → ident ( Actuals )
    @_('IDENTIFIER "(" Actuals ")"')
    def Call(self, p):
        print('Found Call')
        
    # Actuals → Expr+, |ε
    @_('Expr+',
        'ε')
    def Actuals(self, p):
        return p
    
    # Constant → intConstant | doubleConstant | boolConstant | stringConstant | null
    @_('INT',
        'DOUBLE',
        'BOOL',
        'STRING',
        'NULL')
    def Constant(self, p):
        return p

    @_('IDENTIFIER')
    def Decl(self, p):
        try:
            return self.IDENTIFIERs[p.IDENTIFIER]
        except LookupError:
            print("Undefined IDENT '%s'" % p.IDENTIFIER)
            return 0
        
    def error(self, p):
        if p:
            print("Syntax error at '%s'" % p.value)
        else:
            print("Syntax error at EOF")


if __name__ == '__main__':

    # Expects DLang source from file
    if len(sys.argv) == 2:
        lexer = DLangLexer()
        parser = DLangParser()
        with open(sys.argv[1]) as source:
            dlang_code = source.read()
            try:
                parser.parse(lexer.tokenize(dlang_code))
            except EOFError: exit(1)
    else:
        print("[DLang]: Source file missing")
