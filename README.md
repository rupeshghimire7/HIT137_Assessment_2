# HIT137-Assessment-2

Software Now – Assessment 2 (HIT137, Sydney Group 5). This repository is our implementation of the assignment, with source code, test files and outputs.

Task 1 – Cipher ( Hemanta Adhikari (s403355) & John Karki ())

## Repository Structure

```
.
├── github_link.txt
├── Q1_Cipher
│   ├── actions
│   │   ├── encryption.py       # encrypt_character, encrypt_file
│   │   └── decryption.py       # decrypt_character, decrypt_file
│   ├── verification
│   │   └── verify.py           # verify_files
│   ├── cipher.py                # main program: prompts for shift1/shift2, runs the pipeline
│   ├── raw_text.txt             # sample input text
│   ├── encrypted_text.txt       # generated output (encrypted)
│   ├── decrypted_text.txt       # generated output (decrypted)
│   └── tests
│       ├── conftest.py
│       ├── test_encryption.py
│       ├── test_decryption.py
│       ├── test_verify.py
│       └── test_cipher.py
└── README.md
```

Explain the concept of a Cipher, meaning.Give an explanation about the concept of Cipher meaning.

The `Q1_Cipher` module contains a user-defined substitution cipher, which uses two non-negative integer keys, `shift1` and `shift2`.

### Cipher rules

Character range | Shift applied |
|---|---|
| Lowercase `a`–`n` | forward by `shift1 * shift2` |
| Lowercase `o`–`z` | backward by `shift1 + shift2` |
| Uppercase `A`–`M` | backward by `shift1` |
| Uppercase `N`–`Z` | forward by `shift2 ** 2` |
| Digits `0`–`9` | forward by `shift1 - shift2` |
All other characters (spaces, punctuation, symbols, new lines) | keep the same characters |

Each range is wrapped separately (modular arithmetic), which means that the encryption is completely reversible by using the inverse shift in `decryption.py`.

### How to run

From inside `Q1_Cipher/`:

```bash
python cipher.py
```

You will be asked for `shift1` and `shift2`, which are integers and are not negative. The program will then automatically:

1. Encrypt `raw_text.txt` → `encrypted_text.txt`
2. Decrypt `encrypted_text.txt` → `decrypted_text.txt`
3. Check if `decrypted_text.txt` is identical to `raw_text.txt` and print the answer.

### Modules

For each function listed below, create a corresponding function in the file "actions/encryption.py".For each of the following functions, write a function with the same name in the file "actions/encryption.py".
These are found in the actions/decryption.py file: `shift_character_in_range`, `decrypt_character`, `decrypt_file`
This script, `verification/verify.py`, takes two file paths as arguments: the original file path and the decrypted path.This script, verification/verify.py, accepts two file paths as arguments: original_path and decrypted_path.
- **`ask_for_shift.py`** - `ask_for_shift` (asks the user for the shift value)

### Tests

Tests are in the `Q1_Cipher/tests/` directory, and they leverage the `pytest` tools and the `monkeypatch` and `tmp_path` fixtures to isolate the file I/O and simulate user input. The `conftest.py` file adds the root of the project to `sys.path` so that the packages `actions` and `verification` are available for direct import.

Execute all the Q1 tests from the `Q1_Cipher/` (either command will do):

```bash
pytest tests/
```

or, using the module runner (recommended if `pytest` isn't on your PATH, or to make sure the current Python environment's `pytest` is used):

```bash
python -m pytest tests/
```

Use `-v` to get verbose per-test output (e.g. `python -m pytest tests/ -v`).

### Test run output

```
$ pytest tests/
================================= test session starts =================================
platform linux -- Python 3.13.5, pytest-8.3.4, pluggy-1.5.0
rootdir: /home/hemanta/Documents/CDU/Software Now/assessment-2/HIT137-Assessment-2/Q1_Cipher
plugins: anyio-4.7.0
collected 43 items

tests/test_cipher.py ........                                                    [ 18%]
tests/test_decryption.py .............                                          [ 53%]
tests/test_encryption.py .............                                          [ 88%]
tests/test_verify.py ....                                                       [100%]

================================== 43 passed in 0.09s ==================================
```

Coverage includes:
- Proper shifting/wrapping for each range of characters
For round-trip encryption and decryption, correctness of the encryption and decryption.
- If the value of "shift" is negative, the input is rejected.
Handle missing files and empty files.Error handling for missing file, empty file.
- End-to-end `main()` behaviour (success, missing raw file, empty raw file)

## Group Contributions

As required by the assignment guidelines, all work has been tracked throughout the development starting from the first commit and up until the final commit in this GitHub repository. For the repository link, please refer to the file `github_link.txt.
