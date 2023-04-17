from typing import Any
import re
import math
var = {}

class token:
    typ: str
    val: str

    def __init__(self, typ, val):
        self.typ = typ
        self.val = val

    def __repr__(self):
        return f"token({self.typ!r}, {self.val!r})"

def convert_num(string):
    try:
        float(string)
        return float(string)
    except ValueError:
        raise ValueError(f"is not numeric {string}")

def lex(s: str) -> list[token]:

    tokens = []
    i = 0

    while i < len(s):
        if s[i].isspace():
            i += 1
        elif s[i].isalpha():
            end = i + 1
            while end < len(s) and (s[end].isalnum() or s[end] == "_"):
                end += 1
            assert end >= len(s) or not (s[end].isalnum() or s[end] == "_")

            word = s[i:end]

            if word in ["true", "false"]:
                tokens.append(token("kw", word))
            else:
                tokens.append(token("var", word))
            i = end
        elif s[i].isnumeric():
            end = i + 1
            while end < len(s) and (
                s[end].isnumeric() or (s[end] == "." and s[end + 1].isnumeric())
            ):
                end += 1
            assert end >= len(s) or not (
                s[end].isnumeric() or (s[end] == "." and s[end + 1].isnumeric())
            )
            num = s[i:end]
            tokens.append(token("num", convert_num(num)))
            i = end
        elif s[i: i + 2] == "++":
            tokens.append(token("sym", "++"))
            i += 2
        elif s[i: i + 2] == "--":
            tokens.append(token("sym", "--"))
            i += 2
        elif s[i] == "!":
            tokens.append(token("sym", "!"))
            i += 1
        elif s[i] == "(":
            tokens.append(token("sym", "("))
            i += 1
        elif s[i] == ")":
            tokens.append(token("sym", ")"))
            i += 1
        elif s[i] == "+":
            tokens.append(token("sym", "+"))
            i += 1
        elif s[i] == "-":
            tokens.append(token("sym", "-"))
            i += 1
        elif s[i] == "*":
            tokens.append(token("sym", "*"))
            i += 1
        elif s[i] == "/":
            tokens.append(token("sym", "/"))
            i += 1
        elif s[i] == "%":
            tokens.append(token("sym", "%"))
            i += 1
        elif s[i] == "^":
            tokens.append(token("sym", "^"))
            i += 1
        elif s[i: i + 2] == "||":
            tokens.append(token("sym", "||"))
            i += 2
        elif s[i: i + 2] == "&&":
            tokens.append(token("sym", "&&"))
            i += 2
        elif s[i] == "=":
            tokens.append(token("sym", "="))
            i += 1
        else:
            raise SyntaxError(f"unexpected character {s[i]}")
    return tokens

class ast:
    typ: str
    children: tuple[Any, ...]

    def __init__(self, typ: str, *children: Any):
        self.typ = typ
        self.children = children

    def __repr__(self):
        return f'ast({self.typ!r}, {", ".join([repr(c) for c in self.children])})'

def parse(s: str) -> ast:
    ts = lex(s)
    a, i = equal(ts, 0)

    if i != len(ts):
        raise SyntaxError(f"expected EOF, found {ts[i:]!r}")
    return a

def equal(ts: list[token], i: int) -> tuple[ast, int]:
    if i >= len(ts):
        raise SyntaxError("expected addition, found EOF")
    lhs, i = add(ts, i)
    while i < len(ts) and ts[i].typ == "sym" and ts[i].val == "=":
        rhs, i = add(ts, i + 1)
        lhs = ast("=", lhs, rhs)
    return lhs, i

def add(ts: list[token], i: int) -> tuple[ast, int]:
    if i >= len(ts):
        raise SyntaxError("expected addition, found EOF")
    lhs, i = sub(ts, i)
    while i < len(ts) and ts[i].typ == "sym" and ts[i].val == "+":
        rhs, i = sub(ts, i + 1)
        lhs = ast("+", lhs, rhs)
    return lhs, i


def sub(ts: list[token], i: int) -> tuple[ast, int]:
    if i >= len(ts):
        raise SyntaxError("expected subtraction, found EOF")
    lhs, i = mul(ts, i)
    while i < len(ts) and ts[i].typ == "sym" and ts[i].val == "-":
        rhs, i = mul(ts, i + 1)
        lhs = ast("-", lhs, rhs)
    return lhs, i

def mul(ts: list[token], i: int) -> tuple[ast, int]:
    if i >= len(ts):
        raise SyntaxError("expected subtraction, found EOF")
    lhs, i = div(ts, i)
    while i < len(ts) and ts[i].typ == "sym" and ts[i].val == "*":
        rhs, i = div(ts, i + 1)
        lhs = ast("*", lhs, rhs)
    return lhs, i

def div(ts: list[token], i: int) -> tuple[ast, int]:
    if i >= len(ts):
        raise SyntaxError("expected subtraction, found EOF")
    lhs, i = remainder(ts, i)
    while i < len(ts) and ts[i].typ == "sym" and ts[i].val == "/":
        rhs, i = remainder(ts, i + 1)
        lhs = ast("/", lhs, rhs)
    return lhs, i

def remainder(ts: list[token], i: int) -> tuple[ast, int]:
    if i >= len(ts):
        raise SyntaxError("expected subtraction, found EOF")
    lhs, i = exp(ts, i)
    while i < len(ts) and ts[i].typ == "sym" and ts[i].val == "%":
        rhs, i = exp(ts, i + 1)
        lhs = ast("%", lhs, rhs)
    return lhs, i

def exp(ts: list[token], i: int) -> tuple[ast, int]:
    if i >= len(ts):
        raise SyntaxError("expected subtraction, found EOF")
    temp = []
    lhs, i = disj(ts, i)
    temp.append(lhs)
    while i < len(ts) and ts[i].typ == "sym" and ts[i].val == "^":
        rhs, i = disj(ts, i + 1)
        temp.append(rhs)
    t = len(temp) - 1
    la = temp[t]
    while t >= 1:
        la = ast("^", temp[t - 1], la)
        t = t - 1
    return la, i


def disj(ts: list[token], i: int) -> tuple[ast, int]:
    if i >= len(ts):
        raise SyntaxError("expected conjunction, found EOF")
    lhs, i = conj(ts, i)
    while i < len(ts) and ts[i].typ == "sym" and ts[i].val == "||":
        rhs, i = conj(ts, i + 1)
        lhs = ast("||", lhs, rhs)
    return lhs, i

def conj(ts: list[token], i: int) -> tuple[ast, int]:
    if i >= len(ts):
        raise SyntaxError("expected conjunction, found EOF")
    lhs, i = neg(ts, i)
    while i < len(ts) and ts[i].typ == "sym" and ts[i].val == "&&":
        rhs, i = neg(ts, i + 1)
        lhs = ast("&&", lhs, rhs)
    return lhs, i

def neg(ts: list[token], i: int) -> tuple[ast, int]:
    if i >= len(ts):
        raise SyntaxError("expected negation, found EOF")

    if ts[i].typ == "sym" and ts[i].val == "!":
        a, i = neg(ts, i + 1)
        return ast("!", a), i
    if ts[i].typ == "sym" and ts[i].val == "-":
        a, i = neg(ts, i + 1)
        return ast("-", a), i
    if ts[i].typ == "sym" and ts[i].val == "--":
        a, i = neg(ts, i + 1)
        return ast("--", a), i
    if ts[i].typ == "sym" and ts[i].val == "++":
        a, i = neg(ts, i + 1)
        return ast("++", a), i
    else:
        return atom(ts, i)

def atom(ts: list[token], i: int) -> tuple[ast, int]:
    t = ts[i]
    if t.typ == "var":
        return ast("var", t.val), i + 1
    elif t.typ == "kw" and t.val in ["true", "false"]:
        return ast("val", t.val == "true"), i + 1
    elif t.typ == "num":
        return ast("val", t.val), i + 1
    elif t.typ == "sym" and t.val == "(":
        a, i = add(ts, i + 1)

        if i >= len(ts):
            raise SyntaxError(f"expeprintcted right paren, got EOF")

        if not (ts[i].typ == "sym" or ts[i].val == ")"):
            raise SyntaxError(f'expected right paren, got "{ts[i]}"')
        return a, i + 1
    raise SyntaxError(f'expected atom, got "{ts[i]}"')

def interp(a: ast, env: set[str]) -> bool:
    if a.typ == "val":
        return a.children[0]
    elif a.typ == "var":
        return a.children[0] in env
    elif a.typ == "!":
        return not interp(a.children[0], env)
    elif a.typ == "&&":
        return interp(a.children[0], env) and interp(a.children[1], env)
    elif a.typ == "||":
        return interp(a.children[0], env) or interp(a.children[1], env)
    raise SyntaxError(f"unknown operation {a.typ}")

def result(a: ast) -> float:
    if a.typ == "+":
        return result(a.children[0]) + result(a.children[1])
    elif a.typ == "-" and len(a.children) > 1:
        return result(a.children[0]) - result(a.children[1])
    elif a.typ == "-" and len(a.children) == 1:
        return -result(a.children[0])
    elif a.typ == "++" and len(a.children) == 1:
        return result(ast("=", a.children[0], ast("+", a.children[0], ast("val", 1))))
    elif a.typ == "--" and len(a.children) == 1:
        return result(ast("=", a.children[0], ast("-", a.children[0], ast("val", 1))))
    elif a.typ == "*":
        return result(a.children[0]) * result(a.children[1])
    elif a.typ == "/":
        return result(a.children[0]) / result(a.children[1])
    elif a.typ == "%":
        return result(a.children[0]) % result(a.children[1])
    elif a.typ == "^":
        return math.pow(result(a.children[0]), result(a.children[1]))
    elif a.typ == "=":
        var[a.children[0].children[0]] = result(a.children[1])
        return var
    elif a.typ == "val":
        return a.children[0]
    elif a.typ == 'var':
        if a.children[0] in var.keys():
            return var[a.children[0]]
        elif a.children[0] not in var.keys():
            var[a.children[0]] = 0.0
            return var[a.children[0]]
        else:
            raise SyntaxError(f'unknown operation {a.typ}')

while True:
    try:
        user_input = input()
        output = ""
        if re.match(r"^\s*print\s+\w*", user_input, re.IGNORECASE):
            string = re.sub(r"^\s*print\s+", "",
                            user_input.rstrip(), re.IGNORECASE)
            test = string.split(",")
            for i in range(len(test)):
                temp = parse(test[i])
                output += f"{result(temp)} "
            print(output.strip())
        elif user_input == "":
            continue
        else:
            result(parse(user_input))
    except SyntaxError:
        print(f"parse error")
    except ZeroDivisionError:
        output += f"divide by zero"
        print(output.strip())
    except EOFError:
        break