def verify_files(original_path, decrypted_path):
    try:
        with open(original_path, "r", encoding="utf-8") as original_file:
            original_text = original_file.read()
    except FileNotFoundError:
        raise FileNotFoundError("Could not find the file: " + original_path)

    try:
        with open(decrypted_path, "r", encoding="utf-8") as decrypted_file:
            decrypted_text = decrypted_file.read()
    except FileNotFoundError:
        raise FileNotFoundError("Could not find the file: " + decrypted_path)

    if original_text == decrypted_text:
        print("Success! The decrypted file is identical to the original file.")
        return True

    print(
        "Decryption failed because the decrypted file is NOT the same as the original file."
    )
    return False


if __name__ == "__main__":
    RAW_FILE = "text_files/raw_text.txt"
    DECRYPTED_FILE = "text_files/decrypted_text.txt"

    print("Step 3: Checking that decryption worked correctly...")

    try:
        verify_files(RAW_FILE, DECRYPTED_FILE)
    except FileNotFoundError as error:
        print("Verification failed:", error)
