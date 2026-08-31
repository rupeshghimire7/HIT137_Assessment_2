from src.cipher_text.cipher import ask_for_shift, main


def test_ask_for_shift_accepts_valid_number(monkeypatch):
    monkeypatch.setattr(
        "builtins.input",
        lambda message: "5"
    )

    result = ask_for_shift(
        "Enter shift: "
    )

    assert result == 5


def test_ask_for_shift_accepts_zero(monkeypatch):
    monkeypatch.setattr(
        "builtins.input",
        lambda message: "0"
    )

    result = ask_for_shift(
        "Enter shift: "
    )

    assert result == 0


def test_ask_for_shift_rejects_text(monkeypatch):
    inputs = iter([
        "hello",
        "5"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda message: next(inputs)
    )

    result = ask_for_shift(
        "Enter shift: "
    )

    assert result == 5


def test_ask_for_shift_rejects_negative_number(monkeypatch):
    inputs = iter([
        "-5",
        "3"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda message: next(inputs)
    )

    result = ask_for_shift(
        "Enter shift: "
    )

    assert result == 3


def test_ask_for_shift_rejects_decimal(monkeypatch):
    inputs = iter([
        "2.5",
        "4"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda message: next(inputs)
    )

    result = ask_for_shift(
        "Enter shift: "
    )

    assert result == 4


def test_main_completes_encryption_and_decryption(
    monkeypatch,
    tmp_path,
    capsys
):
    monkeypatch.chdir(tmp_path)

    original_text = "Hello World 123! abc XYZ"

    (tmp_path / "text_files").mkdir()

    (
        tmp_path / "text_files" / "raw_text.txt"
    ).write_text(
        original_text,
        encoding="utf-8"
    )

    inputs = iter([
        "2",
        "3"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda message: next(inputs)
    )

    main()

    encrypted_file = (
        tmp_path / "text_files" / "encrypted_text.txt"
    )

    decrypted_file = (
        tmp_path / "text_files" / "decrypted_text.txt"
    )

    assert encrypted_file.exists()
    assert decrypted_file.exists()

    decrypted_text = decrypted_file.read_text(
        encoding="utf-8"
    )

    assert decrypted_text == original_text

    captured = capsys.readouterr()

    assert "Step 1: Encrypting" in captured.out
    assert "Step 2: Decrypting" in captured.out
    assert "Step 3: Checking" in captured.out
    assert "Success!" in captured.out


def test_main_handles_missing_raw_file(
    monkeypatch,
    tmp_path,
    capsys
):
    monkeypatch.chdir(tmp_path)

    inputs = iter([
        "2",
        "3"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda message: next(inputs)
    )

    main()

    captured = capsys.readouterr()

    assert "Encryption failed:" in captured.out


def test_main_handles_empty_raw_file(
    monkeypatch,
    tmp_path,
    capsys
):
    monkeypatch.chdir(tmp_path)

    (tmp_path / "text_files").mkdir()

    (
        tmp_path / "text_files" / "raw_text.txt"
    ).write_text(
        "",
        encoding="utf-8"
    )

    inputs = iter([
        "2",
        "3"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda message: next(inputs)
    )

    main()

    captured = capsys.readouterr()

    assert "Encryption failed:" in captured.out
    assert "is empty" in captured.out