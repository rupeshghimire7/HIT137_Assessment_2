# HIT137 Assessment 2 – Sydney Group 5

This is our group submission for HIT137 Software Now, Assessment 2. The repo has all our source code, tests, and output files for each question.

**Question 1 – Cipher:** Hemanta Adhikari (s403355) & John Karki (s403518)

## Folder structure

```
.
├── docs
│   ├── HIT137 Assignment 2 S2 2026.pdf
│   ├── raw_text.txt
│   ├── sample_input.txt
│   └── sample_output.txt
├── github_link.txt
├── README.md
├── requirements.txt
├── src
│   └── cipher_text
│       ├── cipher.py               # main program: prompts for shift1/shift2, runs the pipeline
│       ├── encryption.py           # encrypt_character, encrypt_file
│       ├── decryption.py           # decrypt_character, decrypt_file
│       ├── verify.py               # verify_files
│       └── text_files
│           ├── raw_text.txt        # input text
│           ├── encrypted_text.txt  # output after encryption
│           └── decrypted_text.txt  # output after decryption
└── tests                           # outside src — run from project root
    ├── conftest.py
    ├── test_cipher.py
    ├── test_encryption.py
    ├── test_decryption.py
    └── test_verify.py
```

## Question 1 – Cipher

Hemanta wrote the encryption side and John wrote the decryption and verification. Together they form a custom substitution cipher that takes two numbers — `shift1` and `shift2` — and uses them to scramble text, then reverse it back.

### How the cipher works

Each character in the file gets shifted by a different amount depending on what it is:

| Character | What happens |
|---|---|
| Lowercase `a`–`n` | shifted forward by `shift1 × shift2` |
| Lowercase `o`–`z` | shifted backward by `shift1 + shift2` |
| Uppercase `A`–`M` | shifted backward by `shift1` |
| Uppercase `N`–`Z` | shifted forward by `shift2²` |
| Digits `0`–`9` | shifted forward by `shift1 − shift2` |
| Spaces, punctuation, everything else | left as-is |

Each range wraps around on itself, so no character ever escapes its group and the whole thing can be reversed exactly.

### How to run

All commands below are run from inside `src/cipher_text/`.

> ⚠️ **shift1 and shift2 must be the same when you encrypt and decrypt.** If you use different numbers, the decryption will come out wrong and verification will fail.

**To test encryption only (Hemanta's part):**
```bash
python encryption.py
```
Enter your shift values and it will encrypt `text_files/raw_text.txt` into `text_files/encrypted_text.txt`.

**To test decryption only (John's part):**
```bash
python decryption.py
```
Enter the same shift values used during encryption and it will decrypt `text_files/encrypted_text.txt` into `text_files/decrypted_text.txt`.

**To test verification only (John's part):**
```bash
python verify.py
```
Compares `text_files/raw_text.txt` with `text_files/decrypted_text.txt` and tells you if they match. You need to have run both encryption and decryption first with the same shift values.

**To run the whole pipeline at once:**
```bash
python cipher.py
```
Enter shift values once and it automatically encrypts, decrypts, and verifies in one go.

### What each file does

- `encryption.py` — written by Hemanta. Has `shift_character_in_range`, `encrypt_character`, and `encrypt_file`.
- `decryption.py` — written by John. Has `shift_character_in_range`, `decrypt_character`, and `decrypt_file`.
- `verify.py` — written by Hemanta. Has `verify_files` which compares the original and decrypted files.
- `cipher.py` — ties everything together. Has `ask_for_shift` and `main`.

### Tests

The tests are in the `tests/` folder at the project root, not inside `src/`. To run them, go to the project root first:

```bash
cd ~/HIT137-Assessment-2
pytest tests/
```

or with verbose output:

```bash
python -m pytest -v tests/
```

`conftest.py` handles adding `src/cipher_text` to the Python path so the imports work correctly from outside that folder.

### Test results

```
$ pytest tests/
================================================================================ test session starts ================================================================================
platform linux -- Python 3.13.5, pytest-8.3.4, pluggy-1.5.0
rootdir: /HIT137-Assessment-2
plugins: anyio-4.7.0
collected 43 items

tests/test_cipher.py ........                                                                                                                                                 [ 18%]
tests/test_decryption.py ...............                                                                                                                                      [ 53%]
tests/test_encryption.py ...............                                                                                                                                      [ 88%]
tests/test_verify.py .....                                                                                                                                                    [100%]

================================================================================ 43 passed in 0.15s ================================================================================
```

```
$ python -m pytest -v tests/
================================================================================ test session starts ================================================================================
platform linux -- Python 3.13.5, pytest-8.3.4, pluggy-1.5.0 -- /home/hemanta/anaconda3/bin/python
cachedir: .pytest_cache
rootdir: /HIT137-Assessment-2
plugins: anyio-4.7.0
collected 43 items

tests/test_cipher.py::test_ask_for_shift_accepts_valid_number PASSED                                                                                                          [  2%]
tests/test_cipher.py::test_ask_for_shift_accepts_zero PASSED                                                                                                                  [  4%]
tests/test_cipher.py::test_ask_for_shift_rejects_text PASSED                                                                                                                  [  6%]
tests/test_cipher.py::test_ask_for_shift_rejects_negative_number PASSED                                                                                                       [  9%]
tests/test_cipher.py::test_ask_for_shift_rejects_decimal PASSED                                                                                                               [ 11%]
tests/test_cipher.py::test_main_completes_encryption_and_decryption PASSED                                                                                                    [ 13%]
tests/test_cipher.py::test_main_handles_missing_raw_file PASSED                                                                                                               [ 16%]
tests/test_cipher.py::test_main_handles_empty_raw_file PASSED                                                                                                                 [ 18%]
tests/test_decryption.py::test_shift_character_forward PASSED                                                                                                                 [ 20%]
tests/test_decryption.py::test_shift_character_wraps_forward PASSED                                                                                                           [ 23%]
tests/test_decryption.py::test_shift_character_backward PASSED                                                                                                                [ 25%]
tests/test_decryption.py::test_decrypt_lowercase_character PASSED                                                                                                             [ 27%]
tests/test_decryption.py::test_decrypt_lowercase_second_range PASSED                                                                                                          [ 30%]
tests/test_decryption.py::test_decrypt_uppercase_first_range PASSED                                                                                                           [ 32%]
tests/test_decryption.py::test_decrypt_uppercase_second_range PASSED                                                                                                          [ 34%]
tests/test_decryption.py::test_decrypt_number PASSED                                                                                                                          [ 37%]
tests/test_decryption.py::test_special_character_is_unchanged PASSED                                                                                                          [ 39%]
tests/test_decryption.py::test_space_is_unchanged PASSED                                                                                                                      [ 41%]
tests/test_decryption.py::test_decrypt_file PASSED                                                                                                                            [ 44%]
tests/test_decryption.py::test_negative_shift1_is_rejected PASSED                                                                                                             [ 46%]
tests/test_decryption.py::test_negative_shift2_is_rejected PASSED                                                                                                             [ 48%]
tests/test_decryption.py::test_missing_input_file PASSED                                                                                                                      [ 51%]
tests/test_decryption.py::test_empty_input_file PASSED                                                                                                                        [ 53%]
tests/test_encryption.py::test_shift_character_forward PASSED                                                                                                                 [ 55%]
tests/test_encryption.py::test_shift_character_wraps_forward PASSED                                                                                                           [ 58%]
tests/test_encryption.py::test_shift_character_backward PASSED                                                                                                                [ 60%]
tests/test_encryption.py::test_encrypt_lowercase_character PASSED                                                                                                             [ 62%]
tests/test_encryption.py::test_encrypt_lowercase_second_range PASSED                                                                                                          [ 65%]
tests/test_encryption.py::test_encrypt_uppercase_first_range PASSED                                                                                                           [ 67%]
tests/test_encryption.py::test_encrypt_uppercase_second_range PASSED                                                                                                          [ 69%]
tests/test_encryption.py::test_encrypt_number PASSED                                                                                                                          [ 72%]
tests/test_encryption.py::test_special_character_is_unchanged PASSED                                                                                                          [ 74%]
tests/test_encryption.py::test_space_is_unchanged PASSED                                                                                                                      [ 76%]
tests/test_encryption.py::test_encrypt_file PASSED                                                                                                                            [ 79%]
tests/test_encryption.py::test_negative_shift1_is_rejected PASSED                                                                                                             [ 81%]
tests/test_encryption.py::test_negative_shift2_is_rejected PASSED                                                                                                             [ 83%]
tests/test_encryption.py::test_missing_input_file PASSED                                                                                                                      [ 86%]
tests/test_encryption.py::test_empty_input_file PASSED                                                                                                                        [ 88%]
tests/test_verify.py::test_matching_files_return_true PASSED                                                                                                                  [ 90%]
tests/test_verify.py::test_different_files_return_false PASSED                                                                                                                [ 93%]
tests/test_verify.py::test_missing_original_file PASSED                                                                                                                       [ 95%]
tests/test_verify.py::test_missing_decrypted_file PASSED                                                                                                                      [ 97%]
tests/test_verify.py::test_two_empty_files_match PASSED                                                                                                                       [100%]

================================================================================ 43 passed in 0.14s ================================================================================
```

The tests cover shifting and wrapping for every character range, the full encrypt-then-decrypt round trip, what happens when you pass negative shifts, missing files, empty files, and the full `main()` flow end to end.

## Group contributions

Everything has been committed to GitHub as we went, as required by the assignment. The repo link is in `github_link.txt`.