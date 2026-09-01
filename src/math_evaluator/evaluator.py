import os
import sys
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).resolve().parent
TEXT_FILES_DIR = BASE_DIR / "text_files"
DEFAULT_INPUT_PATH = TEXT_FILES_DIR / "sample_input.txt"

# For lint, specifying OSError type
class EvaluationOutputError(OSError):
    """Raised when the evaluator cannot write the output file."""


def tokenize(expr: str) -> list[tuple[str, str | None]]:
    """
    Scans a mathematical expression and breaks it down into a list of typed tokens.

    Args:
        expr (str): The raw string expression to tokenize.

    Returns:
        List[Tuple[str, Union[str, None]]]: A list of tuples containing token types and values.

    Raises:
        ValueError: If an invalid character or malformed number is encountered.
    """
    tokens: list[tuple[str, str | None]] = []
    i = 0
    n = len(expr)

    while i < n:
        c = expr[i]

        if c.isspace():
            i += 1
            continue

        if c.isdigit():
            start = i
            while i < n and expr[i].isdigit():
                i += 1
            if i < n and expr[i] == ".":
                i += 1
                if i >= n or not expr[i].isdigit():
                    raise ValueError(
                        f"Invalid number literal near position {start}: "
                        f"'.' must be followed by at least one digit"
                    )
                while i < n and expr[i].isdigit():
                    i += 1
            tokens.append(("NUM", expr[start:i]))
            continue

        if c in "+-*/%^":
            tokens.append(("OP", c))
            i += 1
            continue

        if c == "(":
            tokens.append(("LPAREN", "("))
            i += 1
            continue

        if c == ")":
            tokens.append(("RPAREN", ")"))
            i += 1
            continue

        raise ValueError(f"Unexpected character {c!r} at position {i}")

    tokens.append(("END", None))
    return tokens


def tokens_to_string(tokens: list[tuple[str, str | None]]) -> str:
    """
    Formats a list of tokens into the required string representation.

    Args:
        tokens (List[Tuple[str, Union[str, None]]]): The token list.

    Returns:
        str: A space-separated string of bracketed tokens.
    """
    parts = []
    for ttype, value in tokens:
        if ttype == "END":
            parts.append("[END]")
        else:
            parts.append(f"[{ttype}:{value}]")
    return " ".join(parts)


def _peek(tokens: list[tuple[str, Any]], pos: list[int]) -> tuple[str, Any]:
    """Returns the current token without consuming it."""
    return tokens[pos[0]]


def _advance(tokens: list[tuple[str, Any]], pos: list[int]) -> tuple[str, Any]:
    """Consumes the current token and advances the position pointer."""
    tok = tokens[pos[0]]
    pos[0] += 1
    return tok


def parse(tokens: list[tuple[str, Any]]) -> tuple[str, Any]:
    """
    Top-level entry point to parse a full token list into an Abstract Syntax Tree (AST).

    Args:
        tokens (List[Tuple[str, Any]]): The token list ending with [END].

    Returns:
        Tuple[str, Any]: The root node of the parsed AST.

    Raises:
        ValueError: If trailing tokens exist after parsing the main expression.
    """
    pos = [0]
    node = parse_expression(tokens, pos)
    if _peek(tokens, pos)[0] != "END":
        raise ValueError(f"Unexpected trailing token {_peek(tokens, pos)}")
    return node


def parse_expression(tokens: list[tuple[str, Any]], pos: list[int]) -> tuple[str, Any]:
    """
    Level 1 Parser: Handles addition and subtraction (left-associative).

    Args:
        tokens (List[Tuple[str, Any]]): The token stream.
        pos (List[int]): A mutable list containing the current index.

    Returns:
        Tuple[str, Any]: The parsed node.
    """
    node = parse_term(tokens, pos)
    while _peek(tokens, pos)[0] == "OP" and _peek(tokens, pos)[1] in ("+", "-"):
        op = _advance(tokens, pos)[1]
        right = parse_term(tokens, pos)
        node = ("binop", op, node, right)
    return node


def parse_term(tokens: list[tuple[str, Any]], pos: list[int]) -> tuple[str, Any]:
    """
    Level 2 Parser: Handles multiplication, division, modulo, and implicit multiplication (left-associative).

    Args:
        tokens (List[Tuple[str, Any]]): The token stream.
        pos (List[int]): The current index.

    Returns:
        Tuple[str, Any]: The parsed node.
    """
    node, was_paren = parse_factor(tokens, pos)
    while True:
        tok = _peek(tokens, pos)
        if tok[0] == "OP" and tok[1] in ("*", "/", "%"):
            op = _advance(tokens, pos)[1]
            right, was_paren = parse_factor(tokens, pos)
            node = ("binop", op, node, right)
        elif tok[0] == "LPAREN" or (was_paren and tok[0] == "NUM"):
            right, was_paren = parse_factor(tokens, pos)
            node = ("binop", "*", node, right)
        else:
            break
    return node


def parse_factor(
    tokens: list[tuple[str, Any]], pos: list[int]
) -> tuple[tuple[str, Any], bool]:
    """
    Level 3 Parser: Handles prefix unary minus. Rejects unary plus.

    Args:
        tokens (List[Tuple[str, Any]]): The token stream.
        pos (List[int]): The current index.

    Returns:
        Tuple[Tuple[str, Any], bool]: A tuple of the parsed node and a boolean tracking parenthesis state.

    Raises:
        ValueError: If a unary '+' is encountered.
    """
    tok = _peek(tokens, pos)
    if tok[0] == "OP" and tok[1] == "-":
        _advance(tokens, pos)
        operand, _ = parse_factor(tokens, pos)
        return ("neg", operand), False
    if tok[0] == "OP" and tok[1] == "+":
        raise ValueError("Unary '+' is not supported")
    return parse_power(tokens, pos)


def parse_power(
    tokens: list[tuple[str, Any]], pos: list[int]
) -> tuple[tuple[str, Any], bool]:
    """
    Level 4 Parser: Handles exponentiation (right-associative, binds tighter than unary minus).

    Args:
        tokens (List[Tuple[str, Any]]): The token stream.
        pos (List[int]): The current index.

    Returns:
        Tuple[Tuple[str, Any], bool]: A tuple of the parsed node and paren state.
    """
    left, was_paren = parse_atom(tokens, pos)
    tok = _peek(tokens, pos)
    if tok[0] == "OP" and tok[1] == "^":
        _advance(tokens, pos)
        right, _ = parse_factor(tokens, pos)
        return ("binop", "^", left, right), False
    return left, was_paren


def parse_atom(
    tokens: list[tuple[str, Any]], pos: list[int]
) -> tuple[tuple[str, Any], bool]:
    """
    Base Level Parser: Extracts numeric literals and handles parenthesized sub-expressions.

    Args:
        tokens (List[Tuple[str, Any]]): The token stream.
        pos (List[int]): The current index.

    Returns:
        Tuple[Tuple[str, Any], bool]: A tuple of the leaf node and paren state.

    Raises:
        ValueError: On mismatched parentheses or unexpected tokens.
    """
    tok = _peek(tokens, pos)
    if tok[0] == "NUM":
        _advance(tokens, pos)
        return ("num", float(tok[1])), False
    if tok[0] == "LPAREN":
        _advance(tokens, pos)
        node = parse_expression(tokens, pos)
        closing = _peek(tokens, pos)
        if closing[0] != "RPAREN":
            raise ValueError("Expected closing ')'")
        _advance(tokens, pos)
        return node, True
    raise ValueError(f"Unexpected token {tok}")


def format_number(value: float) -> str:
    """Formats a numeric float to an integer string or rounds to 4 decimal places."""
    if value == int(value):
        return str(int(value))
    return str(round(value, 4))


def tree_to_string(node: tuple[str, Any]) -> str:
    """
    Recursively renders an AST tuple into the required parenthesized prefix string.

    Args:
        node (Tuple[str, Any]): The current AST node.

    Returns:
        str: The string representation of the tree.

    Raises:
        ValueError: If an unknown AST node type is encountered.
    """
    kind = node[0]
    if kind == "num":
        return format_number(node[1])
    if kind == "neg":
        return f"(neg {tree_to_string(node[1])})"
    if kind == "binop":
        _, op, left, right = node
        return f"({op} {tree_to_string(left)} {tree_to_string(right)})"
    raise ValueError(f"Unknown AST node type: {kind!r}")


def evaluate_ast(node: tuple[str, Any]) -> float:
    """
    Recursively evaluates an AST to compute the final mathematical result.

    Args:
        node (Tuple[str, Any]): The root of the AST.

    Returns:
        float: The calculated result.

    Raises:
        ValueError: If division by zero, modulo by zero, or math overflow occurs.
    """
    kind = node[0]
    if kind == "num":
        return node[1]
    if kind == "neg":
        return -evaluate_ast(node[1])
    if kind == "binop":
        op = node[1]
        left = evaluate_ast(node[2])
        right = evaluate_ast(node[3])

        if op == "+":
            return left + right
        if op == "-":
            return left - right
        if op == "*":
            return left * right
        if op == "/":
            if right == 0:
                raise ValueError("Division by zero")
            return left / right
        if op == "%":
            if right == 0:
                raise ValueError("Modulo by zero")
            return left % right
        if op == "^":
            try:
                result = left**right
            except ZeroDivisionError as exc:
                raise ValueError("Division by zero") from exc
            if isinstance(result, complex):
                raise ValueError("Complex numbers not supported")
            return result

    raise ValueError(f"Unknown AST node type: {kind!r}")


def evaluate_file(input_path: str) -> list[dict[str, Any]]:
    """
    Reads mathematical expressions from a text file, parses, evaluates, and writes blocks to 'output.txt'.

    Args:
        input_path (str): The file path to read expressions from.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries representing the evaluation of each expression.
    """
    input_path_obj = Path(input_path).expanduser()
    if not input_path_obj.is_absolute():
        input_path_obj = (Path.cwd() / input_path_obj).resolve()

    if not input_path_obj.exists():
        return []

    with open(input_path_obj, "r", encoding="utf-8") as f:
        expressions = [line.strip() for line in f if line.strip()]

    results: list[dict[str, Any]] = []
    output_blocks: list[str] = []

    for expr in expressions:
        entry: dict[str, Any] = {
            "input": expr,
            "tree": "ERROR",
            "tokens": "ERROR",
            "result": "ERROR",
        }

        try:
            tokens = tokenize(expr)
            entry["tokens"] = tokens_to_string(tokens)
            try:
                parsed = parse(tokens)
                entry["tree"] = tree_to_string(parsed)
                try:
                    value = evaluate_ast(parsed)
                    if isinstance(value, float) and value.is_integer():
                        entry["result"] = int(value)
                    else:
                        entry["result"] = round(float(value), 4)
                except ValueError:
                    pass
            except ValueError:
                pass
        except ValueError:
            pass

        results.append(entry)
        output_blocks.append(
            f"Input: {entry['input']}\n"
            f"Tree: {entry['tree']}\n"
            f"Tokens: {entry['tokens']}\n"
            f"Result: {entry['result']}\n"
        )

    out_path = input_path_obj.parent / "output.txt"
    with open(out_path, "w", encoding="utf-8") as out_file:
        out_file.write("\n\n".join(output_blocks))

    return results


def main(argv: list[str] | None = None) -> None:
    """Run the evaluator against the bundled sample input unless a file path is given."""
    args = sys.argv[1:] if argv is None else argv
    input_path = args[0] if args else str(DEFAULT_INPUT_PATH)
    results = evaluate_file(input_path)
    print(f"Processed {len(results)} expression(s) from {input_path}")


if __name__ == "__main__":
    main()