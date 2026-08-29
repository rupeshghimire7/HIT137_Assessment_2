"""
HIT137 - Software Now - Assessment 2 - Sydney Group 5
Question 1 - Encryption module (Task 1: John Karki & Hemanta Adhikari)
 
Encrypts text using the assignment's custom substitution cipher.
"""

def shift_character_in_range(char, shift, start, end):
    """
    Move a character within a predetermined range.
    The shift is reversible because each range wraps independently.
    """
    range_size = ord(end) - ord(start) + 1
    return chr(
        (ord(char) - ord(start) + shift) % range_size
        + ord(start)
    )

def encrypt_character(char, shift1, shift2):
    """
    Encrypt one character according to the cipher rules.
    """
    if 'a' <= char <= 'n':
        return shift_character_in_range(
            char,
            shift1 * shift2,
            'a',
            'n'
        )
    elif 'o' <= char <= 'z':
        return shift_character_in_range(
            char,
            -(shift1 + shift2),
            'o',
            'z'
        )
    elif 'A' <= char <= 'M':
        return shift_character_in_range(
            char,
            -shift1,
            'A',
            'M'
        )
    elif 'N' <= char <= 'Z':
        return shift_character_in_range(
            char,
            shift2 * shift2,
            'N',
            'Z'
        )
    elif '0' <= char <= '9':
        return shift_character_in_range(
            char,
            shift1 - shift2,
            '0',
            '9'
        )
    else:
        return char

def encrypt_file(shift1, shift2, input_path, output_path):
    """
    Once the contents of input_path have been encrypted, save the result to output_path.    
    """
    if shift1 < 0 or shift2 < 0:
        raise ValueError("Shifts 1 and 2 cannot be negative.")
    try:
        with open(input_path, 'r', encoding='utf-8') as input_file:
            text = input_file.read()
    except FileNotFoundError:
        raise FileNotFoundError(
            "Could not find the file: " + input_path
        )
    if text.strip() == "":
        raise ValueError(
            "The file " + input_path + " is empty."
        )
    encrypted_text = ""
    for char in text:
        encrypted_text += encrypt_character(
            char,
            shift1,
            shift2
        )
    try:
        with open(output_path, 'w', encoding='utf-8') as output_file:
            output_file.write(encrypted_text)
    except Exception as error:
        raise Exception(
            "Could not write to "
            + output_path
            + ": "
            + str(error)
        )