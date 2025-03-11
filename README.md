# BLA Compiler

This project implements a lexical analyzer and a syntactic analyzer for the **BLA** (Binary Language) programming language using Python and PLY (Python Lex-Yacc).

## Features

- **Lexer (`lex_bla.py`)**: Converts a `.bla` source file into a sequence of tokens and outputs them to the screen and a `.tkn` file.
- **Parser (`parse_bla.py`)**: Validates that the tokens conform to BLA's grammar, constructs an Abstract Syntax Tree (AST), and outputs it to the screen and a `.ast` file.

## Usage

Run the lexer:

```sh
python lex_bla.py my_program.bla
```

Run the parser:

```sh
python parse_bla.py my_program.bla
```

## Token Definitions

- Identifiers: Lowercase letters, digits, and underscores starting with a lowercase letter or underscore.
- Numeric Literals: Binary numbers with optional + or - prefix.
- Operators: A (Addition), S (Subtraction), M (Multiplication), D (Integer Division), =, (, ).
- Whitespace: Spaces, tabs, newlines, and carriage returns.
- Comments: /* block comments */ and // line comments.

## Grammar
- Program → Statement*
- Statement → identifier = Expression
- Expression → Expression A Term | Expression S Term | Term
- Term → Term M Factor | Term D Factor | Factor
- Factor → ( Expression ) | binary | identifier

## Dependencies
- Python 3.x
- PLY (Python Lex-Yacc)
