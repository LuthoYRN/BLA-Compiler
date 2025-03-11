import ply.yacc as yacc
from lex_bla import tokens, lexer
import sys

# Parsing rules
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

def generate_ast_string(node, indent=1):
    """
    Recursively generate AST string representation with proper indentation
    """
    if not isinstance(node, tuple):
        # Terminal node
        if isinstance(node, str) and node.startswith(('0', '1', '+', '-')) or node.isdigit() or (node.startswith(('+', '-')) and node[1:].isdigit()):
            return '\t' * indent + f"BINARY_LITERAL,{node}"
        elif isinstance(node, str):
            return '\t' * indent + f"ID,{node}"
        return '\t' * indent + str(node)
    
    # Non-terminal node
    op, left, right = node
    result = '\t' * indent + op + '\n'
    
    # left child
    result += generate_ast_string(left, indent + 1) + '\n'
    
    # right child
    result += generate_ast_string(right, indent + 1)
    
    return result

def write_ast_file(ast, filename):
    output_filename = filename.replace(".bla", ".ast")
    
    with open(output_filename, 'w', encoding='utf-8') as f:
        f.write("Program\n")
        
        for i, statement in enumerate(ast):
            stmt_str = generate_ast_string(statement)
            f.write(stmt_str)
            f.write('\n')
    
    print(f"AST saved to {output_filename}")

def process_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        data = f.read()
    
    lexer.input(data) 
    result = parser.parse(lexer=lexer)  # Parse tokens

    print("AST:", result)
    
    write_ast_file(result, filename)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        process_file(sys.argv[1])
    else:
        print("Usage: python parse_bla.py my_program.bla")