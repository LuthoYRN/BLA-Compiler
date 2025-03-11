import ply.yacc as yacc
from lex_bla import tokens,lexer
import sys

def filter_tokens(lexer, data):
    lexer.input(data)
    filtered_tokens = []
    for token in lexer:
        if token.type not in ['WHITESPACE', 'COMMENT']:
            filtered_tokens.append(token)
    return filtered_tokens

# Parsing rules
def p_program(p):
    '''
    program : statements
    '''
    p[0] = ('Program', p[1])

def p_statements(p):
    '''
    statements : statements statement
               | statement
               |
    '''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    elif len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = []

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

def p_error(p):
    print("Syntax error found!")

# Building the parser
parser = yacc.yacc()

def generate_ast(node, file=None, indent=0):
    if isinstance(node, tuple):
        # Non-terminal node
        output = "\t" * indent + str(node[0])
        if file:
            file.write(output + "\n")
        
        if node[0] == 'Program':
            for stmt in node[1]:
                generate_ast(stmt, file, indent + 1)
        else:
            generate_ast(node[1], file, indent + 1)
            generate_ast(node[2], file, indent + 1)
    else:
        # Terminal node
        if isinstance(node, str):
            if node.startswith(('0', '1', '+', '-')):
                output = "\t" * indent + f"BINARY_LITERAL,{node}"
            else:
                output = "\t" * indent + f"ID,{node}"
            if file:
                file.write(output + "\n")

def process_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = f.read()  
        # A custom filtered lexer to skip whitespace and comments
        class FilteredLexer:
            def __init__(self, tokens):
                self.tokens = tokens
                self.pos = 0
            
            def token(self):
                if self.pos < len(self.tokens):
                    tok = self.tokens[self.pos]
                    self.pos += 1
                    return tok
                return None
        
        filtered_tokens = filter_tokens(lexer, data) #using old lexer to get all tokens except whitespaces and comments
        filtered_lexer = FilteredLexer(filtered_tokens) #dummy lexer to return filtered tokens 
        ast = parser.parse(lexer=filtered_lexer)  # Parse with filtered tokens
        output_filename = filename.replace(".bla", ".ast")
        
        with open(output_filename, 'w', encoding='utf-8') as f:
            generate_ast(ast, f)
        
        print(f"AST saved to {output_filename}")
    
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found!")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        process_file(sys.argv[1])
    else:
        print("Usage: python parse_bla.py my_program.bla")