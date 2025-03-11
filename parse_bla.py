import ply.yacc as yacc

def p_program(p):
    '''
    program : program statement
            | statement
    '''
    if len(p) == 3:  # Multiple statements
        p[0] = p[1] + [p[2]]
    else:  # Single statement
        p[0] = [p[1]]

def p_statement(p):
    '''
    statement : ID '=' expression
    '''
    p[0] = ('ID', p[1], p[3])

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
    factor : '(' expression ')'
           | BINARY_LITERAL
           | ID 
    '''
    if len(p) == 2:
        p[0] = p[1]
    elif p[1] == '(':
        p[0] = p[2]

def p_empty(p):
    'empty :'
    pass
