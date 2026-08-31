import pytest

from src.cipher_text.decryption import (
    decrypt_character,
    decrypt_file,
    shift_character_in_range,
)


def test_shift_character_forward():
    result = shift_character_in_range("a", 1, "a", "n")

    assert result == "b"


def test_shift_character_wraps_forward():
    result = shift_character_in_range("n", 1, "a", "n")

    assert result == "a"


def test_shift_character_backward():
    result = shift_character_in_range("b", -1, "a", "n")

    assert result == "a"


def test_decrypt_lowercase_character():
    # Encryption changes a -> g.
    # Decryption should change g -> a.
    result = decrypt_character("g", 2, 3)

    assert result == "a"


def test_decrypt_lowercase_second_range():
    # Encryption changes o -> v.
    # Decryption should change v -> o.
    result = decrypt_character("v", 2, 3)

    assert result == "o"


def test_decrypt_uppercase_first_range():
    # Encryption changes B -> M.
    # Decryption should change M -> B.
    result = decrypt_character("M", 2, 3)

    assert result == "B"


def test_decrypt_uppercase_second_range():
    # Encryption changes N -> W.
    # Decryption should change W -> N.
    result = decrypt_character("W", 2, 3)

    assert result == "N"


def test_decrypt_number():
    # Encryption changes 5 -> 4.
    # Decryption should change 4 -> 5.
    result = decrypt_character("4", 2, 3)

    assert result == "5"


def test_special_character_is_unchanged():
    result = decrypt_character("!", 2, 3)

    assert result == "!"


def test_space_is_unchanged():
    result = decrypt_character(" ", 2, 3)

    assert result == " "


def test_decrypt_file(tmp_path):
    encrypted_file = tmp_path / "encrypted.txt"
    decrypted_file = tmp_path / "decrypted.txt"

    encrypted_file.write_text("ghi012!", encoding="utf-8")

    decrypt_file(2, 3, str(encrypted_file), str(decrypted_file))

    decrypted_text = decrypted_file.read_text(encoding="utf-8")

    assert decrypted_text == "abc123!"


def test_negative_shift1_is_rejected(tmp_path):
    input_file = tmp_path / "encrypted.txt"
    output_file = tmp_path / "decrypted.txt"

    input_file.write_text("ghi", encoding="utf-8")

    with pytest.raises(ValueError, match="Shifts 1 and 2 cannot be negative."):
        decrypt_file(-1, 3, str(input_file), str(output_file))


def test_negative_shift2_is_rejected(tmp_path):
    input_file = tmp_path / "encrypted.txt"
    output_file = tmp_path / "decrypted.txt"

    input_file.write_text("ghi", encoding="utf-8")

    with pytest.raises(ValueError, match="Shifts 1 and 2 cannot be negative."):
        decrypt_file(2, -3, str(input_file), str(output_file))


def test_missing_input_file():
    with pytest.raises(FileNotFoundError, match="Could not find the file"):
        decrypt_file(2, 3, "missing_file.txt", "output.txt")


def test_empty_input_file(tmp_path):
    input_file = tmp_path / "empty.txt"
    output_file = tmp_path / "output.txt"

    input_file.write_text("", encoding="utf-8")

    with pytest.raises(ValueError, match="is empty"):
        decrypt_file(2, 3, str(input_file), str(output_file))
