import ply.lex as lex
import sys

# Define token names
tokens = ['COMMENT','OP','ID', 'BINARY_LITERAL','WHITESPACE']

# Token 
def t_COMMENT(t):
    r'//.*' 
    return t 

def t_WHITESPACE(t):
    r'\s'
    return t 

def t_ID(t):
    r'[a-z_][a-zA-Z0-9_]*' 
    return t

def t_BINARY_LITERAL(t):
    r'[+-]?[01]+'  
    return t

def t_OP(t):
    r'[ASMD=()]'
    return t

def t_error(t): 
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

# Building the lexer
lexer = lex.lex()

def process_file(input_filename):
    output_filename = input_filename.replace(".bla", ".tkn")
    try:
        with open(input_filename, 'r', encoding='utf-8') as file_in, open(output_filename, 'w', encoding='utf-8') as file_out:
            for line in file_in:
                lexer.input(line)
                while True:
                    tok = lexer.token()
                    if not tok:
                        break
                    if tok.type=="OP":
                        token_output = f"{tok.value}"
                    elif tok.type =="WHITESPACE":
                        token_output = f"{tok.type}"
                    elif tok.type == 'COMMENT':
                        token_output = f"{tok.type}"
                    else:
                        token_output = f"{tok.type},{tok.value}"
                    file_out.write(token_output + "\n") 
        print(f"Tokens saved to {output_filename}")
    except FileNotFoundError:
        print(f"Error: File '{input_filename}' not found!")

if len(sys.argv) > 1:
    process_file(sys.argv[1])
else:
    print('Usage: python lex_bla.py <filename>.bla')