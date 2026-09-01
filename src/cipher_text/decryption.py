"""Decryption module: reverses two-key substitution cipher."""


class CipherWriteError(OSError):
    """Raised when the decrypted output file cannot be written."""


def shift_character_in_range(char, shift, start, end):
    """
    Reverse/shift a character in a given character range.
    """
    range_size = ord(end) - ord(start) + 1
    return chr((ord(char) - ord(start) + shift) % range_size + ord(start))


def decrypt_character(char, shift1, shift2):
    """
    Reverse the encryption for one character.
    """
    if "a" <= char <= "n":
        return shift_character_in_range(char, -(shift1 * shift2), "a", "n")
    elif "o" <= char <= "z":
        return shift_character_in_range(char, shift1 + shift2, "o", "z")
    elif "A" <= char <= "M":
        return shift_character_in_range(char, shift1, "A", "M")
    elif "N" <= char <= "Z":
        return shift_character_in_range(char, -(shift2 * shift2), "N", "Z")
    elif "0" <= char <= "9":
        return shift_character_in_range(char, -(shift1 - shift2), "0", "9")
    else:
        return char


def decrypt_file(shift1, shift2, input_path, output_path):
    """
    Decrypt input_path and write the result to output_path.
    """
    if shift1 < 0 or shift2 < 0:
        raise ValueError("Shifts 1 and 2 cannot be negative.")
    try:
        with open(input_path, "r", encoding="utf-8") as input_file:
            encrypted_text = input_file.read()
    except FileNotFoundError:
        raise FileNotFoundError("Could not find the file: " + input_path)
    if encrypted_text.strip() == "":
        raise ValueError("The file " + input_path + " is empty.")
    decrypted_text = ""
    for char in encrypted_text:
        decrypted_text += decrypt_character(char, shift1, shift2)
    try:
        with open(output_path, "w", encoding="utf-8") as output_file:
            output_file.write(decrypted_text)
    except OSError as error:
        raise CipherWriteError(f"Could not write to {output_path}: {error}") from error


if __name__ == "__main__":
    from pathlib import Path
    
    BASE_DIR = Path(__file__).resolve().parent

    try:
        TEXT_DIR = BASE_DIR / "text_files"
    except:
        TEXT_DIR = Path("text_files")
        

    RAW_FILE = str(TEXT_DIR / "raw_text.txt")
    ENCRYPTED_FILE = str(TEXT_DIR / "encrypted_text.txt")
    DECRYPTED_FILE = str(TEXT_DIR / "decrypted_text.txt")

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

    shift1 = ask_for_shift("Enter shift1 (non-negative integer): ")
    shift2 = ask_for_shift("Enter shift2 (non-negative integer): ")

    print()
    print("Step 2: Decrypting", ENCRYPTED_FILE, "...")

    try:
        decrypt_file(shift1, shift2, ENCRYPTED_FILE, DECRYPTED_FILE)
        print("Done. Decrypted file saved as", DECRYPTED_FILE)
    except (FileNotFoundError, ValueError) as error:
        print("Decryption failed:", error)
