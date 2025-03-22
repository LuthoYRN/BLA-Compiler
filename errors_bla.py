from lex_bla import lexer,error_messages
from parse_bla import parser
import sys

def process_file(input_filename):
    output_filename = input_filename.replace(".bla", ".err")
    try:
        with open(input_filename, 'r', encoding='utf-8') as file_in, open(output_filename, 'w', encoding='utf-8') as file_out:
            data = file_in.read()
            # Lexical + Syntax Parsing
            ast = parser.parse(data, lexer=lexer)
            if len(error_messages)>0:
                file_out.write(error_messages[0] + "\n")
                return
    except FileNotFoundError:
        print(f"Error: File '{input_filename}' not found!")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        process_file(sys.argv[1])
    else:
        print('Usage: python errors_bla.py <filename>.bla')