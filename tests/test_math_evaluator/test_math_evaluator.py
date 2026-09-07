import pytest

from src.math_evaluator.evaluator import (
    evaluate_ast,
    evaluate_file,
    parse,
    tokenize,
    tokens_to_string,
    tree_to_string,
)


def test_tokenize_valid_numbers_and_operators():
    tokens = tokenize("3.14 + 5 * (2 - 8) / 4 % 2 ^ 3")
    expected = [
        ("NUM", "3.14"),
        ("OP", "+"),
        ("NUM", "5"),
        ("OP", "*"),
        ("LPAREN", "("),
        ("NUM", "2"),
        ("OP", "-"),
        ("NUM", "8"),
        ("RPAREN", ")"),
        ("OP", "/"),
        ("NUM", "4"),
        ("OP", "%"),
        ("NUM", "2"),
        ("OP", "^"),
        ("NUM", "3"),
        ("END", None),
    ]
    assert tokens == expected


def test_tokenize_invalid_number_literal():
    with pytest.raises(ValueError, match="'.' must be followed by at least one digit"):
        tokenize("5. + 3")


def test_tokenize_unexpected_character():
    with pytest.raises(ValueError, match="Unexpected character '@'"):
        tokenize("3 @ 5")


def test_tokens_to_string():
    tokens = [("NUM", "3"), ("OP", "+"), ("NUM", "5"), ("END", None)]
    assert tokens_to_string(tokens) == "[NUM:3] [OP:+] [NUM:5] [END]"


def test_parse_basic_math():
    tokens = tokenize("3 + 5 * 2")
    ast = parse(tokens)
    assert tree_to_string(ast) == "(+ 3 (* 5 2))"


def test_parse_implicit_multiplication():
    # Number adjacent to parenthesis
    tokens1 = tokenize("2(3+4)")
    ast1 = parse(tokens1)
    assert tree_to_string(ast1) == "(* 2 (+ 3 4))"

    # Parenthesis adjacent to number
    tokens2 = tokenize("(2)3")
    ast2 = parse(tokens2)
    assert tree_to_string(ast2) == "(* 2 3)"

    # Parenthesis adjacent to Parenthesis
    tokens3 = tokenize("(2)(3)")
    ast3 = parse(tokens3)
    assert tree_to_string(ast3) == "(* 2 3)"


def test_parse_unary_negation():
    tokens = tokenize("-(3 + 4)")
    ast = parse(tokens)
    assert tree_to_string(ast) == "(neg (+ 3 4))"

    tokens2 = tokenize("--5")
    ast2 = parse(tokens2)
    assert tree_to_string(ast2) == "(neg (neg 5))"


def test_parse_rejects_unary_plus():
    with pytest.raises(ValueError, match="Unary '\\+' is not supported"):
        parse(tokenize("+5"))


def test_parse_exponentiation_right_associativity():
    # 2 ^ 3 ^ 2 should evaluate as 2 ^ (3 ^ 2)
    tokens = tokenize("2^3^2")
    ast = parse(tokens)
    assert tree_to_string(ast) == "(^ 2 (^ 3 2))"


def test_parse_missing_closing_parenthesis():
    with pytest.raises(ValueError, match="Expected closing '\\)'"):
        parse(tokenize("(3 + 4"))


def test_parse_unexpected_trailing_token():
    with pytest.raises(ValueError, match="Unexpected trailing token"):
        parse(tokenize("3 + 4 5"))


def test_parse_unexpected_base_token():
    with pytest.raises(ValueError, match="Unexpected token"):
        parse(tokenize(")"))


def test_evaluate_ast_basic():
    assert evaluate_ast(parse(tokenize("3 + 5"))) == 8.0
    assert evaluate_ast(parse(tokenize("10 - 2 * 3"))) == 4.0
    assert evaluate_ast(parse(tokenize("10 / 2"))) == 5.0
    assert evaluate_ast(parse(tokenize("10 % 3"))) == 1.0


def test_evaluate_ast_division_by_zero():
    with pytest.raises(ValueError, match="Division by zero"):
        evaluate_ast(parse(tokenize("5 / 0")))


def test_evaluate_ast_modulo_by_zero():
    with pytest.raises(ValueError, match="Modulo by zero"):
        evaluate_ast(parse(tokenize("5 % 0")))


def test_evaluate_ast_complex_result():
    with pytest.raises(ValueError, match="Complex numbers not supported"):
        # Square root of negative number
        evaluate_ast(parse(tokenize("(-4)^0.5")))


def test_evaluate_ast_unknown_node():
    with pytest.raises(ValueError, match="Unknown AST node type: 'unknown'"):
        evaluate_ast(("unknown",))


def test_evaluate_file_full_pipeline(tmp_path):
    input_file = tmp_path / "input.txt"
    input_file.write_text(
        "3 + 5\n2 + 3 * 4\n-(3 + 4)\n--5\n(10 - 2) * 3 + -4 / 2\n3 @ 5\n1 / 0\n",
        encoding="utf-8",
    )

    results = evaluate_file(str(input_file))

    assert len(results) == 7
    assert results[0]["result"] == 8
    assert results[1]["result"] == 14
    assert results[2]["result"] == -7
    assert results[3]["result"] == 5
    assert results[4]["result"] == 22
    assert results[5]["result"] == "ERROR"  # @ token error
    assert results[6]["result"] == "ERROR"  # division by zero error

    # Verify output file generation
    output_file = tmp_path / "output.txt"
    assert output_file.exists()
    content = output_file.read_text(encoding="utf-8")
    assert "Input: 3 + 5" in content
    assert "Result: 8" in content
    assert "Tree: ERROR" in content  # Appears in the @ block


def test_evaluate_file_handles_missing_file():
    results = evaluate_file("does_not_exist.txt")
    assert results == []


def test_tree_to_string_unknown_node():
    with pytest.raises(ValueError, match="Unknown AST node type: 'invalid'"):
        tree_to_string(("invalid",))
