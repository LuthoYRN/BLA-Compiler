import ply.yacc as yacc
from lex_bla import tokens,lexer
import sys

#Parsing rules
def p_program(p):
    '''
    program : program statement
            | statement
    '''
    if len(p) == 3:
        if p[2] is not None:  # Ignore None values from WHITESPACE/COMMENT
            p[0] = p[1] + [p[2]]
        else:
            p[0] = p[1]
    else:
        p[0] = [p[1]] if p[1] is not None else []  # Skip None entries


def p_statement(p):
    '''
    statement : ID EQUALS expression
    '''
    p[0] = (p[2], p[1], p[3])

def p_expression(p):
    '''
    expression : expression A term
               | expression S term 
               | term
    '''
    if len(p) == 4:
        p[0] = (p[2], p[1], p[3])
    else:
        p[0] = p[1]

def p_term(p):
    '''
    term : term M factor
         | term D factor
         | factor
    '''
    if len(p) == 4:
        p[0] = (p[2], p[1], p[3])
    else:
        p[0] = p[1]

def p_factor(p):
    '''
    factor : LPAREN expression RPAREN
           | BINARY_LITERAL
           | ID 
    '''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 4:
        p[0] = p[2]
        
def p_ignore_whitespace_comment(p):
    '''
    statement : WHITESPACE
              | COMMENT
    '''
    p[0] = None  

def p_error(p):
    print("Syntax error found!")

# Building the parser
parser = yacc.yacc()

def process_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        data = f.read()
    
    lexer.input(data) 
    result = parser.parse(lexer=lexer)  # Parse tokens

    # Output AST
    print("AST:", result)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        process_file(sys.argv[1])
    else:
        print("Usage: python parse_bla.py my_program.bla")