from lex_bla import lexer, error_messages
from parse_bla import parser,filter_tokens
import sys

symbol_table = {}

def semantic_analysis(ast, file_out):
    global symbol_table
    
    # Handle the Program node from the parser
    if isinstance(ast, tuple) and ast[0] == 'Program':
        for stmt in ast[1]:
            semantic_analysis(stmt, file_out)
        return

    if isinstance(ast, tuple):
        if ast[0] == '=':
            var_name = ast[1]

            if var_name in symbol_table:  # redefinition error
                error_msg = f"semantic error on line {ast[-1]}"
                print(error_msg)  # Output to screen as well
                file_out.write(error_msg + "\n")
                exit()

            # Check RHS variables
            check_rhs(ast[2], file_out, ast[-1])

            symbol_table[var_name] = True  # Mark variable as defined

def check_rhs(expr, file_out, line_num):
    if isinstance(expr, tuple):
        # This is an operation
        check_rhs(expr[1], file_out, line_num)
        check_rhs(expr[2], file_out, line_num)
    elif isinstance(expr, str):
        # Skip if it's a binary literal
        if not any(c in expr for c in '01+-'):  # Simple check for binary literals
            if expr not in symbol_table:
                error_msg = f"semantic error on line {line_num}"
                print(error_msg)  # Output to screen as well
                file_out.write(error_msg + "\n")
                exit()

def process_file(input_filename):
    output_filename = input_filename.replace(".bla", ".err")
    try:
        with open(input_filename, 'r', encoding='utf-8') as file_in, open(output_filename, 'w', encoding='utf-8') as file_out:
            data = file_in.read()
            
            filtered_tokens = filter_tokens(lexer, data)
            
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
            
            filtered_lexer = FilteredLexer(filtered_tokens)
            
            ast = parser.parse(lexer=filtered_lexer)

            # Handle lex/parse errors
            if len(error_messages) > 0:
                print(error_messages[0])  # Output to screen
                file_out.write(error_messages[0] + "\n")
                return

            # Semantic Analysis
            semantic_analysis(ast, file_out)

            # No errors
            print(f"No errors found. Checked {input_filename}")
            file_out.write("No errors\n")

    except FileNotFoundError:
        print(f"Error: File '{input_filename}' not found!")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        process_file(sys.argv[1])
    else:
        print('Usage: python errors_bla.py <filename>.bla')