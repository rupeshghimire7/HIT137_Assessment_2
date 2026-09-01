# HIT137 Assessment 2 – Sydney Group 5

This is our group submission for **HIT137 Software Now, Assessment 2**. The project contains the source code, tests, input/output text files, and documentation for both assignment questions.

## Group Members

| Member Name      | Student ID |
| ---------------- | ---------- |
| Ashim Koirala    | S407089    |
| Hemanta Adhikari | S403355    |
| John Karki       | S403518    |
| Rupesh Ghimire   | S403354    |

## Project / Task Overview

### Question 1 – Cipher

Write a program in `cipher.py` that reads `raw_text.txt`, encrypts its contents using the required two-key substitution scheme, writes the encrypted result to `encrypted_text.txt`, then decrypts it and verifies that the decrypted text matches the original.

The encryption uses two non-negative integer inputs, `shift1` and `shift2`. Lowercase letters, uppercase letters, digits, and other characters are handled according to the assignment rules. The complete encrypt → decrypt → verify workflow is available through `cipher.py`.

### Question 2 – Mathematical Expression Evaluator

Write a program in `evaluator.py` that reads mathematical expressions from an input text file, one expression per line, evaluates them using recursive-descent parsing, and writes the required tree, tokens, and result information to `output.txt`.

The evaluator handles `+`, `-`, `*`, `/`, `%`, exponentiation `^`, parentheses, unary negation, and the required implicit multiplication rules. It uses plain functions and separate parser functions for the precedence levels, as required by the assignment.

## Folder Structure

```text
.
├── docs
│   ├── HIT137_assignment2.md
│   ├── HIT137 Assignment 2 S2 2026.pdf
│   ├── raw_text.txt
│   ├── sample_input.txt
│   └── sample_output.txt
├── github_link.txt
├── README.md
├── requirements.txt
├── src
│   ├── cipher_text
│   │   ├── __init__.py
│   │   ├── decryption.py
│   │   ├── cipher.py
│   │   ├── encryption.py
│   │   ├── text_files
│   │   │   ├── raw_text.txt
│   │   │   ├── encrypted_text.txt
│   │   │   └── decrypted_text.txt
│   │   └── verify.py
│   └── math_evaluator
│       ├── evaluator.py
│       ├── __init__.py
│       └── text_files
│           ├── sample_input.txt
│           ├── sample_output.txt
│           └── output.txt
└── tests
    ├── conftest.py
    ├── test_cipher.py
    ├── test_decryption.py
    ├── test_encryption.py
    ├── test_math_evaluator.py
    └── test_verify.py
```

## Question 1 – Cipher

### Cipher Rules

| Character | What happens |
|---|---|
| Lowercase `a`–`n` | shifted forward by `shift1 × shift2` |
| Lowercase `o`–`z` | shifted backward by `shift1 + shift2` |
| Uppercase `A`–`M` | shifted backward by `shift1` |
| Uppercase `N`–`Z` | shifted forward by `shift2²` |
| Digits `0`–`9` | shifted forward by `shift1 − shift2` |
| Spaces, tabs, newlines, punctuation, symbols | left unchanged |

Each character range wraps around within its own range.

### Input / Output File Handling

The programs use the expected text-file paths when those files exist.

If the expected bundled input file is missing, a small built-in fallback input is stored in the corresponding Python file. The program uses that fallback, prints a message in the terminal, and creates the missing input file so the program can still be demonstrated.

Output directories are created automatically when needed. Generated output is written to the expected output file and the generated content is also displayed in the terminal.

This fallback behaviour is limited to the program's expected bundled paths. Tests that deliberately pass an unrelated missing path still exercise the normal missing-file error behaviour.

### How to Run

From the project root:

```bash
cd HIT137-Assessment-2
```

The complete Question 1 workflow can be run with:

```bash
python3 src/cipher_text/cipher.py
```

Enter the same `shift1` and `shift2` values for encryption and decryption.

Run encryption only:

```bash
python3 src/cipher_text/encryption.py
```

Run decryption only:

```bash
python3 src/cipher_text/decryption.py
```

Run verification only:

```bash
python3 src/cipher_text/verify.py
```

## Question 2 – Mathematical Evaluator

### Supported Features

The evaluator supports:

- `+`, `-`, `*`, `/`, `%`
- exponentiation `^`
- nested parentheses
- unary negation such as `-5`, `--5`, and `-(3 + 4)`
- implicit multiplication where permitted by the assignment
- errors for unsupported unary `+`
- errors for invalid characters and invalid expressions
- division-by-zero and modulo-by-zero errors
- formatted results with whole numbers shown without `.0` and other results rounded to four decimal places

The output contains four lines per expression:

```text
Input: ...
Tree: ...
Tokens: ...
Result: ...
```

### How to Run

Run the evaluator with its bundled sample input:

```bash
python3 src/math_evaluator/evaluator.py
```

Or provide another input file:

```bash
python3 src/math_evaluator/evaluator.py path/to/input.txt
```

The evaluator writes `output.txt` into the same directory as the input file. It also prints each generated four-line result block to the terminal.

If the expected bundled sample input is missing, `evaluator.py` uses its built-in list of sample expressions, creates the missing input file, and continues.

## Virtual Environment and Requirements

### Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
```

### macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
```

### Windows PowerShell

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

If `python3` is available on Windows, the test commands below can also be used exactly as written. Otherwise, use `python -m pytest ...`.

### Windows Command Prompt

```cmd
py -3 -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Tests

Run each test file separately from the project root using `python3 -m pytest path`:

```bash
python3 -m pytest tests/test_cipher.py
python3 -m pytest tests/test_decryption.py
python3 -m pytest tests/test_encryption.py
python3 -m pytest tests/test_math_evaluator.py
python3 -m pytest tests/test_verify.py
```

Run all tests together:

```bash
python3 -m pytest tests
```

Run all tests with verbose output:

```bash
python3 -m pytest -v tests
```

The tests cover the cipher character transformations, wrapping, encryption/decryption round trips, invalid shifts, missing and empty files, evaluator tokenization, parsing, tree generation, calculation errors, output-file generation, and verification.

## Main Files

- `src/cipher_text/cipher.py` — runs the complete Question 1 pipeline.
- `src/cipher_text/encryption.py` — implements encryption.
- `src/cipher_text/decryption.py` — implements decryption.
- `src/cipher_text/verify.py` — compares the original and decrypted files.
- `src/math_evaluator/evaluator.py` — tokenizes, parses, evaluates, formats, and writes Question 2 results.
- `tests/` — pytest test suite for both questions.
- `docs/HIT137_assignment2.md` — assignment requirements supplied for this submission.
- `github_link.txt` — location for the public GitHub repository link.


