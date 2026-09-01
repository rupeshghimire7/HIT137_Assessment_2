"""Cipher program: encrypts/decrypts text files using shift keys."""

from pathlib import Path

from decryption import decrypt_file
from encryption import encrypt_file
from verify import verify_files

BASE_DIR = Path(__file__).resolve().parent
TEXT_DIR = BASE_DIR / "text_files"
RAW_FILE = str(TEXT_DIR / "raw_text.txt")
ENCRYPTED_FILE = str(TEXT_DIR / "encrypted_text.txt")
DECRYPTED_FILE = str(TEXT_DIR / "decrypted_text.txt")


def ask_for_shift(message: str) -> int:
    """
    Prompt user for a non-negative integer shift value.

    Args:
        message: Prompt text to display.

    Returns:
        Non-negative integer entered by user.

    Raises:
        EOFError: If input stream is closed (testing scenario).
    """
    while True:
        try:
            user_input = input(message)
        except EOFError as e:
            raise EOFError("Input stream closed") from e

        try:
            number = int(user_input)
        except ValueError:
            print("Not a valid whole number. Please try again.")
            continue

        if number < 0:
            print("The number is not allowed to be negative. Please try again.")
            continue

        return number


def main() -> None:
    """
    Main workflow: encrypt raw_text.txt, decrypt it, verify result.

    Prompts user for shift1 and shift2, runs full encrypt-decrypt-verify pipeline.
    Exits early on file or validation errors.
    """
    print("HIT137 Assessment 2 - Question 1")
    print("Encrypt and decrypt text using keys.")
    print()

    try:
        shift1 = ask_for_shift("Enter shift1 (non-negative integer): ")
        shift2 = ask_for_shift("Enter shift2 (non-negative integer): ")
    except EOFError:
        return

    print()
    print(f"Step 1: Encrypting {RAW_FILE} ...")

    try:
        TEXT_DIR.mkdir(parents=True, exist_ok=True)
        encrypt_file(shift1, shift2, RAW_FILE, ENCRYPTED_FILE)
        print(f"Done. Encrypted file saved as {ENCRYPTED_FILE}")
    except (FileNotFoundError, ValueError) as error:
        print(f"Encryption failed: {error}")
        return

    print()
    print(f"Step 2: Decrypting {ENCRYPTED_FILE} ...")

    try:
        decrypt_file(shift1, shift2, ENCRYPTED_FILE, DECRYPTED_FILE)
        print(f"Done. Decrypted file saved as {DECRYPTED_FILE}")
    except (FileNotFoundError, ValueError) as error:
        print(f"Decryption failed: {error}")
        return

    print()
    print("Step 3: Checking that decryption worked correctly...")

    try:
        verify_files(RAW_FILE, DECRYPTED_FILE)
    except FileNotFoundError as error:
        print(f"Verification failed: {error}")
        return


if __name__ == "__main__":
    main()