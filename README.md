# HIT137 Assessment 2 – Sydney Group 5

This project contains the source code, tests, and documentation for a two-part software now program: a custom two-key substitution cipher and a recursive-descent mathematical expression evaluator. 

## Group Members

| Member Name      | Student ID |
| ---------------- | ---------- |
| Ashim Koirala    | S407089    |
| Hemanta Adhikari | S403355    |
| John Karki       | S403518    |
| Rupesh Ghimire   | S403354    |

## Project Architecture & Logic

### Task 1: Two-Key Substitution Cipher

The `cipher_text` module implements a custom cryptographic pipeline that reads raw text, applies character transformations, and writes the encrypted output to a file. It also supports decrypting the ciphered text and verifying the integrity of the round-trip transformation against the original file.

The core algorithm relies on two non-negative integer keys (`shift1` and `shift2`) and dynamically applies different wrapping and shifting rules based on character classification:

* **Lowercase `a`–`n`**: Shifted forward by `shift1 × shift2`.
* **Lowercase `o`–`z`**: Shifted backward by `shift1 + shift2`.
* **Uppercase `A`–`M`**: Shifted backward by `shift1`.
* **Uppercase `N`–`Z`**: Shifted forward by `shift2²`.
* **Digits `0`–`9`**: Shifted forward by `shift1 − shift2`.
* **Special Characters**: Spaces, tabs, newlines, and punctuation remain strictly unchanged.

The main execution script (`cipher.py`) chains these operations, automatically handling missing files by creating fallback directories and sample text to ensure the pipeline runs seamlessly.

### Task 2: Mathematical Expression Evaluator

The `math_evaluator` module is a text-parsing engine that processes string-based mathematical expressions and computes their results using a recursive-descent parser. 

Built entirely with functional programming principles (no classes), the parser breaks down strings into manageable tokens and evaluates them based on strict mathematical precedence (from lowest to highest):
1. Addition (`+`) and Subtraction (`-`)
2. Multiplication (`*`), Division (`/`), Modulo (`%`), and Implicit Multiplication
3. Unary Negation (e.g., `-5`)
4. Exponentiation (`^`)

The logic correctly processes nested parentheses and flags unsupported operations (like unary `+`) or syntax errors. For each parsed expression, the evaluator generates a structured four-line output block containing the original input, the abstract syntax tree (formatted functionally, e.g., `(+ 3 5)`), the token breakdown, and the final computed result (rounded to 4 decimal places, with whole numbers displayed as integers).

## Folder Structure

```text
.
├── .github/workflows # contains workflow
│   └── ci.yml
├── docs # contains documentations of assignment
│   ├── HIT137_assignment2.md
│   ├── HIT137 Assignment 2 S2 2026.pdf
│   ├── raw_text.txt
│   ├── sample_input.txt
│   └── sample_output.txt
├── github_link.txt 
├── README.md
├── requirements.txt
├── src
│   ├── cipher_text # codes and txt files for question 1
│   │   ├── cipher.py
│   │   ├── decryption.py
│   │   ├── encryption.py
│   │   ├── __init__.py
│   │   ├── text_files
│   │   │   ├── decrypted_text.txt
│   │   │   ├── encrypted_text.txt
│   │   │   └── raw_text.txt
│   │   └── verify.py
│   └── math_evaluator # codes and txt files for question 1
│       ├── evaluator.py
│       ├── __init__.py
│       └── text_files
│           ├── input.txt
│           └── output.txt
└── tests 
    ├── conftest.py
    ├── test_cipher_text
    │   ├── test_cipher.py
    │   ├── test_decryption.py
    │   ├── test_encryption.py
    │   └── test_verify.py
    └── test_math_evaluator
        └── test_math_evaluator.py
```

## Setup, Usage, and Testing

All commands should be executed from the root directory of the project. 

### 1. Virtual Environment Setup

**Linux / macOS**
```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
```

**Windows (PowerShell / Command Prompt)**
```powershell
py -3 -m venv .venv
# PowerShell:
.\.venv\Scripts\Activate.ps1
# Command Prompt:
.venv\Scripts\activate

python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 2. Running the Programs

**Task 1: Cipher Pipeline**
To run the complete encryption, decryption, and verification workflow:
```bash
python3 src/cipher_text/cipher.py
```
*Note: You will be prompted in the terminal to enter the integer values for `shift1` and `shift2`.*

The individual components can also be executed standalone:
```bash
python3 src/cipher_text/encryption.py
python3 src/cipher_text/decryption.py
python3 src/cipher_text/verify.py
```

**Task 2: Math Evaluator**
To evaluate the mathematical expressions in the default input file:
```bash
python3 src/math_evaluator/evaluator.py
```
To evaluate a specific target file, pass the file path as an argument. The program will generate an `output.txt` in the exact same directory as the input file:
```bash
python3 src/math_evaluator/evaluator.py path/to/your/input.txt
```

### 3. Running the Tests

The project uses `pytest` to validate cipher wrapping logic, mathematical parsing precedence, tree generation, and edge-case error handling.

**Run the full test suite:**
```bash
python3 -m pytest tests
```

**Run with verbose output:**
```bash
python3 -m pytest -v tests
```

**Run specific test modules:**
```bash
python3 -m pytest tests/test_cipher_text/test_encryption.py
python3 -m pytest tests/test_math_evaluator/test_math_evaluator.py
```

## Automated Workflow

The github workflow contains testing with pytest and coverage test that will run automated flow of tests when code is pushed into `main` branch or if a pull request is made to `main` branch.