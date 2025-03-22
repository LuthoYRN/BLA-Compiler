import ply.lex as lex
import sys

# Define token names
tokens = ['COMMENT','A','S','M','D','EQUALS','LPAREN','RPAREN', 'ID', 'BINARY_LITERAL', 'WHITESPACE']

error_messages = []

#Token rules
t_A = r'A'
t_S = r'S'
t_M = r'M'
t_D = r'D'
t_EQUALS = r'='
t_LPAREN = r'\('
t_RPAREN = r'\)'

def t_ID(t):
    r'[a-z_][a-z0-9_]*'
    return t

def t_BINARY_LITERAL(t):
    r'[+-]?[01]+'
    return t

def t_COMMENT(t):
    r'//.*|/\*[\s\S]*?\*/'
    return t

def t_WHITESPACE(t):
    r'\s+'
    return t

def t_error(t):
    #print(f"lexical error on line {t.lexer.lineno}")
    error_messages.append(f"lexical error on line {t.lexer.lineno}")
    t.lexer.skip(1)

#Building lexer
lexer = lex.lex()

#Processing bla file
def process_file(input_filename):
    output_filename = input_filename.replace(".bla", ".tkn")
    try:
        with open(input_filename, 'r', encoding='utf-8') as file_in, open(output_filename, 'w', encoding='utf-8') as file_out:
            content = file_in.read()
            lexer.input(content)
            while True:
                tok = lexer.token()
                if not tok:
                    break
                if tok.type in ['LPAREN','RPAREN','EQUALS']:
                    token_output = f"{tok.value}"
                elif tok.type in ['A','S','M','D',"WHITESPACE","COMMENT"]:
                    token_output = f"{tok.type}"
                else:
                    token_output = f"{tok.type},{tok.value}"          
                file_out.write(token_output + "\n") 
        print(f"Tokens saved to {output_filename}")
    except FileNotFoundError:
        print(f"Error: File '{input_filename}' not found!")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        process_file(sys.argv[1])
    else:
        print('Usage: python lex_bla.py <filename>.bla')