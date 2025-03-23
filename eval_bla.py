from lex_bla import lexer,error_messages
from parse_bla import parser,filter_tokens
import sys

symbol_table = {} 

def convert_to_binary(num):
    if isinstance(num,str):
        return num
    if num < 0:
        return f"-{bin(abs(num))[2:]}" 
    else:
        return bin(num)[2:]  # Remove '0b' prefix

def convert_to_decimal(binary_str):
    if binary_str.startswith('-'):
        return -int(binary_str[1:], 2)
    elif binary_str.startswith('+'):
        return int(binary_str[1:], 2)
    else:
        return int(binary_str, 2)

def evaluate(node):
    if isinstance(node, str):
        # Check if it's a binary literal
        if any(c in node for c in '01+-') and not(node[:1].isalpha()):
            if node[:1]=='0':
                return node
            return convert_to_decimal(node)
        # Otherwise it's a variable
        if node in symbol_table:
            return symbol_table[node]
        else:
            raise ValueError(f"Variable {node} not defined")
    
    # Handle tuple nodes (operations)
    if isinstance(node, tuple):
        if node[0] == '=':
            var_name = node[1]
            value = evaluate(node[2])
            symbol_table[var_name] = value
            return value
        
        # Evaluate binary operations
        left = evaluate(node[1])
        right = evaluate(node[2])
        
        if node[0] == 'A':
            return left + right
        elif node[0] == 'S':
            return left - right
        elif node[0] == 'M':
            return left * right
        elif node[0] == 'D':
            return left // right  # Integer division
    
    return None

def process_file(input_filename):
    output_filename = input_filename.replace(".bla", ".eva")
    try:
        with open(input_filename, 'r', encoding='utf-8') as file_in, open(output_filename, 'w', encoding='utf-8') as file_out:
            data = file_in.read()
            
            global symbol_table
            symbol_table = {}
            
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
            print(ast)
            # Evaluate the program
            results = []
            
            if ast[0] == 'Program':
                for stmt in ast[1]:
                    if stmt[0] == '=':
                        var_name = stmt[1]
                        evaluate(stmt)  
                        binary_value = convert_to_binary(symbol_table[var_name])
                        output = f"{var_name}[{binary_value}]"
                        print(output)
                        results.append(output)
            
            # Write results to file
            for result in results:
                file_out.write(result + "\n")
    except FileNotFoundError:
        print(f"Error: File '{input_filename}' not found!")
    except Exception as e:
        print(f"Error during evaluation: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        process_file(sys.argv[1])
    else:
        print('Usage: python eval_bla.py <filename>.bla')