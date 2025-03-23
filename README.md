# BLA Compiler

This project implements a **lexical analyzer**, **syntactic analyzer**, **semantic analyzer**, and **evaluator** for the **BLA (Binary Language)** programming language using Python and **PLY (Python Lex-Yacc)**.

---

## **Features**

- **Lexer (`lex_bla.py`)**:  
  Converts a `.bla` source file into a sequence of tokens and outputs them to the screen and a `.tkn` file.

- **Parser (`parse_bla.py`)**:  
  Validates that the tokens conform to BLA's grammar, constructs an Abstract Syntax Tree (AST), and outputs it to a `.ast` file.

- **Semantic Analyzer (`errors_bla.py`)**:  
  Performs semantic checks on the AST:

  - Checks if a variable is used before being defined.
  - Checks if a variable is redefined (assigned multiple times).
    Reports the **first error (lexical, syntactic, or semantic)** to the screen and a `.err` file.

- **Evaluator (`eval_bla.py`)**:  
  Evaluates valid BLA programs, computing and outputting variable values in binary format to a `.eva` file.

---

## **Usage**

### **Run the Lexer:**

```bash
python lex_bla.py my_program.bla
```

- Outputs tokens to `my_program.tkn`.

---

### **Run the Parser:**

```bash
python parse_bla.py my_program.bla
```

- Outputs AST to `my_program.ast`.

---

### **Run Semantic Analysis:**

```bash
python errors_bla.py my_program.bla
```

- Outputs any error to `my_program.err` (lexical, parse, or semantic error).
- Stops at the first detected error.

---

### **Run the Evaluator:**

```bash
python eval_bla.py my_program.bla
```

- Evaluates the program and outputs each assigned variable with its binary value to `my_program.eva`.

---

## Token Definitions

- Identifiers: Lowercase letters, digits, and underscores starting with a lowercase letter or underscore.
- Numeric Literals: Binary numbers with optional + or - prefix.
- Operators: A (Addition), S (Subtraction), M (Multiplication), D (Integer Division), =, (, ).
- Whitespace: Spaces, tabs, newlines, and carriage returns.
- Comments: /_ block comments _/ and // line comments.

## Grammar

- Program → Statement\*
- Statement → identifier = Expression
- Expression → Expression A Term | Expression S Term | Term
- Term → Term M Factor | Term D Factor | Factor
- Factor → ( Expression ) | binary | identifier

## Dependencies

- Python 3.x
- PLY (Python Lex-Yacc)
