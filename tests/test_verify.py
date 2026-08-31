import pytest

from src.cipher_text.verify import verify_files


def test_matching_files_return_true(tmp_path, capsys):
    original_file = tmp_path / "original.txt"
    decrypted_file = tmp_path / "decrypted.txt"

    original_file.write_text("Hello World 123!", encoding="utf-8")

    decrypted_file.write_text("Hello World 123!", encoding="utf-8")

    result = verify_files(str(original_file), str(decrypted_file))

    assert result is True

    captured = capsys.readouterr()

    assert "Success!" in captured.out


def test_different_files_return_false(tmp_path, capsys):
    original_file = tmp_path / "original.txt"
    decrypted_file = tmp_path / "decrypted.txt"

    original_file.write_text("Hello World 123!", encoding="utf-8")

    decrypted_file.write_text("Hello World 456!", encoding="utf-8")

    result = verify_files(str(original_file), str(decrypted_file))

    assert result is False

    captured = capsys.readouterr()

    assert "Decryption failed" in captured.out


def test_missing_original_file(tmp_path):
    original_file = tmp_path / "missing.txt"
    decrypted_file = tmp_path / "decrypted.txt"

    decrypted_file.write_text("Hello World", encoding="utf-8")

    with pytest.raises(FileNotFoundError, match="Could not find the file"):
        verify_files(str(original_file), str(decrypted_file))


def test_missing_decrypted_file(tmp_path):
    original_file = tmp_path / "original.txt"
    decrypted_file = tmp_path / "missing.txt"

    original_file.write_text("Hello World", encoding="utf-8")

    with pytest.raises(FileNotFoundError, match="Could not find the file"):
        verify_files(str(original_file), str(decrypted_file))


def test_two_empty_files_match(tmp_path):
    original_file = tmp_path / "original.txt"
    decrypted_file = tmp_path / "decrypted.txt"

    original_file.write_text("", encoding="utf-8")

    decrypted_file.write_text("", encoding="utf-8")

    result = verify_files(str(original_file), str(decrypted_file))

    assert result is True
