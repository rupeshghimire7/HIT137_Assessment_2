# HIT137-Assessment-2

HIT137 Software Now – Assessment 2, Sydney Group 5. This repository contains our group implementation of the assignment, including source code, test files, and outputs.

**Question 1 – Cipher:** Hemanta Adhikari (s403355) & John Karki

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

## Question 1 – Cipher (Encryption / Decryption)

`Q1_Cipher` implements a custom substitution cipher driven by two non-negative integer keys, `shift1` and `shift2`.

### Cipher rules

| Character range | Shift applied |
|---|---|
| Lowercase `a`–`n` | forward by `shift1 * shift2` |
| Lowercase `o`–`z` | backward by `shift1 + shift2` |
| Uppercase `A`–`M` | backward by `shift1` |
| Uppercase `N`–`Z` | forward by `shift2 ** 2` |
| Digits `0`–`9` | forward by `shift1 - shift2` |
| Everything else (spaces, punctuation, symbols, newlines) | unchanged |

Each range wraps independently (modular arithmetic), so encryption is fully reversible by applying the inverse shift in `decryption.py`.

### How to run

From inside `Q1_Cipher/`:

```bash
python cipher.py
```

You will be prompted for `shift1` and `shift2` (non-negative integers). The program will then automatically:

1. Encrypt `raw_text.txt` → `encrypted_text.txt`
2. Decrypt `encrypted_text.txt` → `decrypted_text.txt`
3. Verify that `decrypted_text.txt` matches `raw_text.txt` and print the result

### Modules

- **`actions/encryption.py`** – `shift_character_in_range`, `encrypt_character`, `encrypt_file`
- **`actions/decryption.py`** – `shift_character_in_range`, `decrypt_character`, `decrypt_file`
- **`verification/verify.py`** – `verify_files(original_path, decrypted_path) -> bool`
- **`cipher.py`** – `ask_for_shift`, `main` (entry point, ties the three modules together)

### Tests

Tests live in `Q1_Cipher/tests` and use `pytest` with `monkeypatch`/`tmp_path` fixtures to isolate file I/O and simulate user input. `conftest.py` adds the project root to `sys.path` so the `actions`/`verification` packages can be imported directly.

Run all Q1 tests from `Q1_Cipher/` (either command works):

```bash
pytest tests/
```

or, using the module runner (recommended if `pytest` isn't on your PATH, or to make sure the current Python environment's `pytest` is used):

```bash
python -m pytest tests/
```

Add `-v` for verbose per-test output, e.g. `python -m pytest tests/ -v`.

### Test run output

Standard run:

```
$ pytest
================================= test session starts =================================
platform linux -- Python 3.13.5, pytest-8.3.4, pluggy-1.5.0
rootdir: /home/hemanta/Documents/CDU/Software Now/assessment-2/HIT137-Assessment-2/Q1_Cipher
plugins: anyio-4.7.0
collected 43 items

tests/test_cipher.py ........                                                    [ 18%]
tests/test_decryption.py ...............                                        [ 53%]
tests/test_encryption.py ...............                                        [ 88%]
tests/test_verify.py .....                                                      [100%]

================================== 43 passed in 0.08s ==================================
```

Verbose run:

```
$ python -m pytest -v tests/
================================= test session starts =================================
platform linux -- Python 3.13.5, pytest-8.3.4, pluggy-1.5.0 -- /home/hemanta/anaconda3/bin/python
cachedir: .pytest_cache
rootdir: /home/hemanta/Documents/CDU/Software Now/assessment-2/HIT137-Assessment-2/Q1_Cipher
plugins: anyio-4.7.0
collected 43 items

tests/test_cipher.py::test_ask_for_shift_accepts_valid_number PASSED             [  2%]
tests/test_cipher.py::test_ask_for_shift_accepts_zero PASSED                     [  4%]
tests/test_cipher.py::test_ask_for_shift_rejects_text PASSED                     [  6%]
tests/test_cipher.py::test_ask_for_shift_rejects_negative_number PASSED          [  9%]
tests/test_cipher.py::test_ask_for_shift_rejects_decimal PASSED                  [ 11%]
tests/test_cipher.py::test_main_completes_encryption_and_decryption PASSED       [ 13%]
tests/test_cipher.py::test_main_handles_missing_raw_file PASSED                  [ 16%]
tests/test_cipher.py::test_main_handles_empty_raw_file PASSED                    [ 18%]
tests/test_decryption.py::test_shift_character_forward PASSED                    [ 20%]
tests/test_decryption.py::test_shift_character_wraps_forward PASSED              [ 23%]
tests/test_decryption.py::test_shift_character_backward PASSED                   [ 25%]
tests/test_decryption.py::test_decrypt_lowercase_character PASSED                [ 27%]
tests/test_decryption.py::test_decrypt_lowercase_second_range PASSED             [ 30%]
tests/test_decryption.py::test_decrypt_uppercase_first_range PASSED              [ 32%]
tests/test_decryption.py::test_decrypt_uppercase_second_range PASSED             [ 34%]
tests/test_decryption.py::test_decrypt_number PASSED                             [ 37%]
tests/test_decryption.py::test_special_character_is_unchanged PASSED             [ 39%]
tests/test_decryption.py::test_space_is_unchanged PASSED                         [ 41%]
tests/test_decryption.py::test_decrypt_file PASSED                               [ 44%]
tests/test_decryption.py::test_negative_shift1_is_rejected PASSED                [ 46%]
tests/test_decryption.py::test_negative_shift2_is_rejected PASSED                [ 48%]
tests/test_decryption.py::test_missing_input_file PASSED                        [ 51%]
tests/test_decryption.py::test_empty_input_file PASSED                          [ 53%]
tests/test_encryption.py::test_shift_character_forward PASSED                    [ 55%]
tests/test_encryption.py::test_shift_character_wraps_forward PASSED              [ 58%]
tests/test_encryption.py::test_shift_character_backward PASSED                   [ 60%]
tests/test_encryption.py::test_encrypt_lowercase_character PASSED                [ 62%]
tests/test_encryption.py::test_encrypt_lowercase_second_range PASSED             [ 65%]
tests/test_encryption.py::test_encrypt_uppercase_first_range PASSED              [ 67%]
tests/test_encryption.py::test_encrypt_uppercase_second_range PASSED             [ 69%]
tests/test_encryption.py::test_encrypt_number PASSED                             [ 72%]
tests/test_encryption.py::test_special_character_is_unchanged PASSED             [ 74%]
tests/test_encryption.py::test_space_is_unchanged PASSED                         [ 76%]
tests/test_encryption.py::test_encrypt_file PASSED                               [ 79%]
tests/test_encryption.py::test_negative_shift1_is_rejected PASSED                [ 81%]
tests/test_encryption.py::test_negative_shift2_is_rejected PASSED                [ 83%]
tests/test_encryption.py::test_missing_input_file PASSED                        [ 86%]
tests/test_encryption.py::test_empty_input_file PASSED                          [ 88%]
tests/test_verify.py::test_matching_files_return_true PASSED                     [ 90%]
tests/test_verify.py::test_different_files_return_false PASSED                   [ 93%]
tests/test_verify.py::test_missing_original_file PASSED                         [ 95%]
tests/test_verify.py::test_missing_decrypted_file PASSED                        [ 97%]
tests/test_verify.py::test_two_empty_files_match PASSED                         [100%]

================================== 43 passed in 0.09s ==================================
```

Coverage includes:
- Correct shifting/wrapping behaviour for each character range
- Round-trip encryption → decryption correctness
- Rejection of negative shift values
- Missing-file and empty-file error handling
- End-to-end `main()` behaviour (success, missing raw file, empty raw file)

## Group Contributions

All work has been tracked via commits to this GitHub repository throughout development, as required by the assignment guidelines. See `github_link.txt` for the repository link.