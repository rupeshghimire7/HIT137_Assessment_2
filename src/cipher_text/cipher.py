"""
HIT137 - Software Now - Assessment 2
Sydney Group 5
 
Question 1: File Encryption / Decryption Cipher
 
This program reads raw_text.txt, encrypts it using a custom substitution
cipher driven by two user-supplied non-negative integer keys (shift1,
shift2), decrypts the result back, and verifies that the decrypted text
matches the original.
 
MEMBERS (Task 1):
HEMANTA ADHIKARI - s403355
JOHN KARKI - (s403518)
 
NOTE: Run with `python cipher.py` from this directory. You will be
prompted for shift1 and shift2, and the program will automatically
encrypt raw_text.txt, decrypt the result, and verify the round trip.
"""

from encryption import encrypt_file
from decryption import decrypt_file
from verify import verify_files

RAW_FILE = "text_files/raw_text.txt"
ENCRYPTED_FILE = "text_files/encrypted_text.txt"
DECRYPTED_FILE = "text_files/decrypted_text.txt"

def ask_for_shift(message):
    while True:
        user_input = input(message)

        try:
            number = int(user_input)
        except ValueError:
            print("Not a valid whole number. Please try again.")
            continue

        if number < 0:
            print("The number is not allowed to be negative. Please try again.")
            continue

        return number

def main():
    print("HIT137 Assessment 2 - Question 1")
    print("Encrypt and decrypt text using keys.")
    print()

    shift1 = ask_for_shift(
        "Enter shift1 (non-negative integer): "
    )

    shift2 = ask_for_shift(
        "Enter shift2 (non-negative integer): "
    )

    print()
    print("Step 1: Encrypting", RAW_FILE, "...")

    try:
        encrypt_file(
            shift1,
            shift2,
            RAW_FILE,
            ENCRYPTED_FILE
        )

        print(
            "Done. Encrypted file saved as",
            ENCRYPTED_FILE
        )

    except (FileNotFoundError, ValueError) as error:
        print("Encryption failed:", error)
        return

    print()
    print("Step 2: Decrypting", ENCRYPTED_FILE, "...")

    try:
        decrypt_file(
            shift1,
            shift2,
            ENCRYPTED_FILE,
            DECRYPTED_FILE
        )

        print(
            "Done. Decrypted file saved as",
            DECRYPTED_FILE
        )

    except (FileNotFoundError, ValueError) as error:
        print("Decryption failed:", error)
        return

    print()
    print("Step 3: Checking that decryption worked correctly...")

    try:
        verify_files(
            RAW_FILE,
            DECRYPTED_FILE
        )

    except FileNotFoundError as error:
        print("Verification failed:", error)
        return

if __name__ == "__main__":
    main()