import pytest

from actions.encryption import (
    shift_character_in_range,
    encrypt_character,
    encrypt_file
)


def test_shift_character_forward():
    result = shift_character_in_range(
        "a", 1, "a", "n"
    )

    assert result == "b"


def test_shift_character_wraps_forward():
    result = shift_character_in_range(
        "n", 1, "a", "n"
    )

    assert result == "a"


def test_shift_character_backward():
    result = shift_character_in_range(
        "b", -1, "a", "n"
    )

    assert result == "a"


def test_encrypt_lowercase_character():
    # 2 * 3 = 6
    # a moved 6 places becomes g
    result = encrypt_character("a", 2, 3)

    assert result == "g"


def test_encrypt_lowercase_second_range():
    # -(2 + 3) = -5
    # o moved backwards within o-z becomes v
    result = encrypt_character("o", 2, 3)

    assert result == "v"


def test_encrypt_uppercase_first_range():
    # B moved backwards by 2:
    # B -> A -> M
    result = encrypt_character("B", 2, 3)

    assert result == "M"


def test_encrypt_uppercase_second_range():
    # 3 * 3 = 9
    # N moved 9 places becomes W
    result = encrypt_character("N", 2, 3)

    assert result == "W"


def test_encrypt_number():
    # 2 - 3 = -1
    # 5 becomes 4
    result = encrypt_character("5", 2, 3)

    assert result == "4"


def test_special_character_is_unchanged():
    result = encrypt_character("!", 2, 3)

    assert result == "!"


def test_space_is_unchanged():
    result = encrypt_character(" ", 2, 3)

    assert result == " "


def test_encrypt_file(tmp_path):
    input_file = tmp_path / "input.txt"
    output_file = tmp_path / "output.txt"

    input_file.write_text(
        "abc123!",
        encoding="utf-8"
    )

    encrypt_file(
        2,
        3,
        str(input_file),
        str(output_file)
    )

    encrypted_text = output_file.read_text(
        encoding="utf-8"
    )

    assert encrypted_text == "ghi012!"


def test_negative_shift1_is_rejected(tmp_path):
    input_file = tmp_path / "input.txt"
    output_file = tmp_path / "output.txt"

    input_file.write_text(
        "abc",
        encoding="utf-8"
    )

    with pytest.raises(
        ValueError,
        match="Shifts 1 and 2 cannot be negative."
    ):
        encrypt_file(
            -1,
            3,
            str(input_file),
            str(output_file)
        )


def test_negative_shift2_is_rejected(tmp_path):
    input_file = tmp_path / "input.txt"
    output_file = tmp_path / "output.txt"

    input_file.write_text(
        "abc",
        encoding="utf-8"
    )

    with pytest.raises(
        ValueError,
        match="Shifts 1 and 2 cannot be negative."
    ):
        encrypt_file(
            2,
            -3,
            str(input_file),
            str(output_file)
        )


def test_missing_input_file():
    with pytest.raises(
        FileNotFoundError,
        match="Could not find the file"
    ):
        encrypt_file(
            2,
            3,
            "missing_file.txt",
            "output.txt"
        )


def test_empty_input_file(tmp_path):
    input_file = tmp_path / "empty.txt"
    output_file = tmp_path / "output.txt"

    input_file.write_text(
        "",
        encoding="utf-8"
    )

    with pytest.raises(
        ValueError,
        match="is empty"
    ):
        encrypt_file(
            2,
            3,
            str(input_file),
            str(output_file)
        )