
class TokenizeError(Exception):
    # Raised when an expression cannot be broken into valid tokens
    pass


class ParseError(Exception):
    # Raised when a token stream does not match the grammar
    pass


# Tokanizer

def tokenize(expr):

    tokens = []
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
            if i < n and expr[i] == '.':
                i += 1
                if i >= n or not expr[i].isdigit():
                    raise TokenizeError(
                        f"Invalid number literal near position {start}: "
                        f"'.' must be followed by at least one digit"
                    )
                while i < n and expr[i].isdigit():
                    i += 1
            tokens.append(('NUM', expr[start:i]))
            continue

        if c in '+-*/%^':
            tokens.append(('OP', c))
            i += 1
            continue

        if c == '(':
            tokens.append(('LPAREN', '('))
            i += 1
            continue

        if c == ')':
            tokens.append(('RPAREN', ')'))
            i += 1
            continue

        raise TokenizeError(f"Unexpected character {c!r} at position {i}")

    tokens.append(('END', None))
    return tokens


def tokens_to_string(tokens):
    parts = []
    for ttype, value in tokens:
        if ttype == 'END':
            parts.append('[END]')
        else:
            parts.append(f'[{ttype}:{value}]')
    return ' '.join(parts)

# Parser


def _peek(tokens, pos):
    return tokens[pos[0]]


def _advance(tokens, pos):
    tok = tokens[pos[0]]
    pos[0] += 1
    return tok


def parse(tokens):
    # Parse a full token list into an AST. Top-level entry point
    pos = [0]
    node = parse_expression(tokens, pos)
    if _peek(tokens, pos)[0] != 'END':
        raise ParseError(f"Unexpected trailing token {_peek(tokens, pos)}")
    return node


def parse_expression(tokens, pos):
    # For + and -, left-associative
    node = parse_term(tokens, pos)
    while _peek(tokens, pos)[0] == 'OP' and _peek(tokens, pos)[1] in ('+', '-'):
        op = _advance(tokens, pos)[1]
        right = parse_term(tokens, pos)
        node = ('binop', op, node, right)
    return node


def parse_term(tokens, pos):
    # For * / % and implicit multiplication, left-associative
    node, was_paren = parse_factor(tokens, pos)
    while True:
        tok = _peek(tokens, pos)
        if tok[0] == 'OP' and tok[1] in ('*', '/', '%'):
            op = _advance(tokens, pos)[1]
            right, was_paren = parse_factor(tokens, pos)
            node = ('binop', op, node, right)
        elif tok[0] == 'LPAREN' or (was_paren and tok[0] == 'NUM'):
            right, was_paren = parse_factor(tokens, pos)
            node = ('binop', '*', node, right)
        else:
            break
    return node


def parse_factor(tokens, pos):
    # For prefix unary minus. Returns (node, was_paren)
    tok = _peek(tokens, pos)
    if tok[0] == 'OP' and tok[1] == '-':
        _advance(tokens, pos)
        operand, _ = parse_factor(tokens, pos)
        return ('neg', operand), False
    if tok[0] == 'OP' and tok[1] == '+':
        raise ParseError("Unary '+' is not supported")
    return parse_power(tokens, pos)


def parse_power(tokens, pos):
    # For  ^, right-associative, binds tighter than unary minus
    left, was_paren = parse_atom(tokens, pos)
    tok = _peek(tokens, pos)
    if tok[0] == 'OP' and tok[1] == '^':
        _advance(tokens, pos)
        right, _ = parse_factor(tokens, pos)  # recurse for right-assoc + unary
        return ('binop', '^', left, right), False
    return left, was_paren


def parse_atom(tokens, pos):
    tok = _peek(tokens, pos)
    if tok[0] == 'NUM':
        _advance(tokens, pos)
        return ('num', float(tok[1])), False
    if tok[0] == 'LPAREN':
        _advance(tokens, pos)
        node = parse_expression(tokens, pos)
        closing = _peek(tokens, pos)
        if closing[0] != 'RPAREN':
            raise ParseError("Expected closing ')'")
        _advance(tokens, pos)
        return node, True
    raise ParseError(f"Unexpected token {tok}")


# Tree stringification

def format_number(value):

    if value == int(value):
        return str(int(value))
    return str(round(value, 4))


def tree_to_string(node):
    # Rendering an AST node as the required parenthesised prefix string
    kind = node[0]
    if kind == 'num':
        return format_number(node[1])
    if kind == 'neg':
        return f"(neg {tree_to_string(node[1])})"
    if kind == 'binop':
        _, op, left, right = node
        return f"({op} {tree_to_string(left)} {tree_to_string(right)})"
    raise ValueError(f"Unknown AST node type: {kind!r}")


# Self-test against the spec's sample expressions

""" 
if __name__ == "__main__":
    samples = [
        "3 + 5",
        "2 + 3 * 4",
        "-(3 + 4)",
        "--5",
        "(10 - 2) * 3 + -4 / 2",
        "3 @ 5",
        "1 / 0",
    ]
    for expr in samples:
        print(f"Input: {expr}")
        try:
            toks = tokenize(expr)
            print(f"Tokens: {tokens_to_string(toks)}")
        except TokenizeError as e:
            print("Tokens: ERROR")
            print(f"Tree: ERROR   ({e})")
            print()
            continue

        try:
            tree = parse(toks)
            print(f"Tree: {tree_to_string(tree)}")
        except ParseError as e:
            print(f"Tree: ERROR   ({e})")
        print()

"""
