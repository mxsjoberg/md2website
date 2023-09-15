# Crafting the Language of Play – Part 1: Introduction and operator precedence

*May 2023*

This is the first post in a series of posts on implementing the new non-trivial programming language, PlayCode. It is open source and all code is available [here](https://github.com/mrsjoberg/playcode).

- [What is PlayCode?](#what-is-playcode)
    - [Implementation language and method](#implementation-language-and-method)
- [Operator precedence](#operator-precedence)
- [Lexer](#lexer)
- [Parser](#parser)
    - [Program](#program)
    - [Expression](#expression)
    - [Term](#term)
    - [Factor](#factor)
- [Interpreter](#interpreter)

## <a name="what-is-playcode" class="anchor"></a> [What is PlayCode?](#what-is-playcode)

The general idea behind PlayCode is to make a playful programmig language and to function as a testbed for experimental programming language features. It is not really meant to be used for anything serious, but rather as a playground for new ideas. So, the implementation need to be easy to manage, change, and build on.

PlayCode is procedural because knowing-how is more important than knowing-that, i.e. [street smarts](https://en.wikipedia.org/wiki/Procedural_knowledge). It will most likely be dynamically typed because no one have time for types anyway. There will be numbers, strings, lists, if-statements, for-loops, variables, and comments. There will probably also be a lot of things that are not yet decided.

Additionally, and more importantly, there will be two main features that will make PlayCode exciting:

- Tags `@<tag>` and goto tag `goto @<tag>` to enable any statement to become a function, so that basically every line can be called from anywhere in the program and return itself once. Imagine playing an instrument where each key or string can be played at any moment and always return some sound.

- Swaps `swap <a> <b>` to swap the values of two variables, which is useful for example when sorting.

Below are examples of valid programs.

```
print 42
```

```
x = 42
-- comment
if x < 0:
    print false
else
    print "positive"
end
```

```
-- swap
x = 2
y = 3
swap x y
print y == 2 -> true
```

```
-- tags
x = 0
@inc x++
goto @inc
print x -> 2
```

There are two ways to include comments, `--` and `->`, which also can be used as helpers in source for more readable code.

### <a name="implementation-language-and-method" class="anchor"></a> [Implementation language and method](#implementation-language-and-method)

I started working on PlayCode before writing this post and managed to implement a basic but working structure for lexer and parser in C++ (mainly to refresh my knowledge of C++ programming). The code is available [here](https://github.com/mrsjoberg/playcode/blob/main/fpc.cpp). However, having to refresh it in the first place is probably due to its insane complexity. It is not a very fun language to work with, so decided to start over in Python. I could always rewrite in C++, C, or something like Zig later if performance is important. 

Python is my go-to language to express ideas, and since Python 3.4+ there is support for enumerations and 3.10+ structural pattern matching (switch statements). Maybe can be used for compiler-writing now?

The method is to start with a subset of the language as per [an incremental approach](http://scheme2006.cs.uchicago.edu/11-ghuloum.pdf). Not necessary the smallest subset or adding a single operator at a time, but managable pieces. This means there will be a working interpreter in each post. I will probably look at code generation later, but interpreting is good enough to get started with exploring programming language features.

## <a name="operator-precedence" class="anchor"></a> [Operator precedence](#operator-precedence)

In this post, the goal is to implement this subset:

```python
# program       ::= PRINT expression
# expression    ::= term ((PLUS | MINUS) term)*
# term          ::= factor ((MULTIPLY | DIVIDE) factor)*
# factor        ::= INTEGER | LPAR expression RPAR

PRINT       = "PRINT"
INTEGER     = "INTEGER"
PLUS        = "+"
MINUS       = "-"
MULTIPLY    = "*"
DIVIDE      = "/"
LPAR        = "("
RPAR        = ")"

RESERVED = [
    "PRINT"
]
```

I have defined two classes to deal with tokens (using classes makes this more readable later).

```python
class TokenType(Enum):
    KEYWORD     = 100
    INTEGER     = 201
    PLUS        = 301
    MINUS       = 302
    MULTIPLY    = 304
    DIVIDE      = 305
    LPAR        = 401
    RPAR        = 402

class Token(object):
    def __init__(self, m_type, m_value):
        self.m_type = m_type
        self.m_value = m_value

    def __repr__(self):
        if self.m_value:
            return f"Token({self.m_type}, '{self.m_value}')"
        else:
            return f"Token({self.m_type})"
```

Here are examples of valid programs (note that `->` is start of comment):

```
print 42
```

```
print 4 + 2 -> 6
```

```
print 1 + (2 * 4) - (6 / 2) -> 6
```

## <a name="lexer" class="anchor"></a> [Lexer](#lexer)

Building a lexer is fairly straightforward. It is just the usual read-each-char in source routine and match with defined tokens.

```python
def tokenize(source):
    tokens = []
    current_line = 1
    current_char = ''
    current_char_index = 0

    while current_char_index < len(source):
        current_char = source[current_char_index]
        match current_char:
            # ...

    return tokens
```

I am skipping whitespace, so first cases match whitespace characters and increment the lexer accordingly.

```python
case ' ' | '\t' | '\r':
    current_char_index += 1
case '\n':
    current_line += 1
    current_char_index += 1
```

The next cases match operators, nothing fancy here. Comments are first matched with `-` and if next character is another `-` or `>` then the rest is skipped until newline.

```python
case '+':
    tokens.append(Token(TokenType.PLUS, PLUS))
    current_char_index += 1
case '-':
    # comments
    next_char = source[current_char_index + 1]
    if next_char == '-' or next_char == '>':
        current_char_index += 1
        # skip until newline
        while source[current_char_index] != '\n':
            current_char_index += 1
    # minus
    else:
        tokens.append(Token(TokenType.MINUS, MINUS))
        current_char_index += 1
case '*':
    tokens.append(Token(TokenType.MULTIPLY, MULTIPLY))
    current_char_index += 1
case '/':
    tokens.append(Token(TokenType.DIVIDE, DIVIDE))
    current_char_index += 1
```

The next case matches parentheses, again nothing fancy.

```python
case '(':
    tokens.append(Token(TokenType.LPAR, LPAR))
    current_char_index += 1
case ')':
    tokens.append(Token(TokenType.RPAR, RPAR))
    current_char_index += 1
```

Then there is the default case, which matches numbers (currently integers) with `isdigit` and identifiers with `isalpha`.

```python
case _:
    if current_char.isdigit():
        # ...
    elif current_char.isalpha():
        # ...
    else:
        raise Exception("Unknown character:", current_char)
```

Numbers can be multi-digit, so each subsequent character that `isdigit` is concatenated to a `number`-string.

```python
number = str(current_char)
current_char_index += 1
while source[current_char_index].isdigit() and current_char_index < len(source):
    number += str(source[current_char_index])
    current_char_index += 1
tokens.append(Token(TokenType.INTEGER, number))
```

Same goes for identifiers, which is also checked against a list of reserved keywords. There are no variables yet so identifiers not in `RESERVED` is discarded.

```python
identifier = str(current_char)
current_char_index += 1
while source[current_char_index].isalpha() and current_char_index < len(source):
    identifier += str(source[current_char_index])
    current_char_index += 1
if identifier.upper() in RESERVED:
    tokens.append(Token(TokenType.KEYWORD, identifier.upper()))
```

The lexer is now complete.

```python
tokens = tokenize("print 1 + (2 * 4) - (6 / 2) -> 6")
for token in tokens: print(token)
# Token(TokenType.KEYWORD, 'PRINT')
# Token(TokenType.INTEGER, '1')
# Token(TokenType.PLUS, '+')
# Token(TokenType.LPAR, '(')
# Token(TokenType.INTEGER, '2')
# Token(TokenType.MULTIPLY, '*')
# Token(TokenType.INTEGER, '4')
# Token(TokenType.RPAR, ')')
# Token(TokenType.MINUS, '-')
# Token(TokenType.LPAR, '(')
# Token(TokenType.INTEGER, '6')
# Token(TokenType.DIVIDE, '/')
# Token(TokenType.INTEGER, '2')
# Token(TokenType.RPAR, ')')
```

## <a name="parser" class="anchor"></a> [Parser](#parser)

The parser is predictive and recursive descent. It starts with `parse`, which takes the flat list of tokens and returns a nested list of tokens (representing a tree structure for a valid program).

It works by recursively calling non-terminals, i.e. program, expression, term, and factor until finding a terminal (currently only `INTEGER`).

```python
def parse(tokens):
    tree = []
    current_token = None
    current_token_index = 0

    while current_token_index < len(tokens):
        program, current_token_index = parse_program(tokens, current_token_index)
        tree = program

    return tree
```

### <a name="program" class="anchor"></a> [Program](#program)

The program production rule is the starting point in the grammar, so `parse_program` is the first non-terminal called. It matches the current token with `PRINT`, which is currently the only acceptable statement in the language. It then calls `parse_expression` to parse the expression as per the grammar rule.

```python
# program ::= PRINT expression
def parse_program(tokens, current_token_index):
    program = []
    current_token = tokens[current_token_index]
    current_token_index += 1
    
    # PRINT
    if current_token.m_value == PRINT:
        program.append(current_token)
        # expression
        expression, current_token_index = parse_expression(tokens, current_token_index)
        program.append(expression)
    else:
        raise Exception("parse_program", "Unexpected token:", tokens[current_token_index])

    return program, current_token_index
```

### <a name="expression" class="anchor"></a> [Expression](#expression)

The expression, term, and factor rules are primarily there to enforce operator precedence, where the expression rule is the highest precedence, followed by term, and then factor.

It works by first calling `parse_term`, which is non-optional, then matches either of the tokens `PLUS` or `MINUS` followed by another `parse_term`, zero or more times.

```python
# expression ::= term ((PLUS | MINUS) term)*
def parse_expression(tokens, current_token_index):
    expression = []
    
    # term
    term, current_token_index = parse_term(tokens, current_token_index)
    expression = term

    while current_token_index < len(tokens) and (tokens[current_token_index].m_type == TokenType.PLUS or tokens[current_token_index].m_type == TokenType.MINUS):
        current_token = tokens[current_token_index]
        current_token_index += 1
        match current_token.m_type:
            # PLUS
            case TokenType.PLUS:
                # term
                term, current_token_index = parse_term(tokens, current_token_index)
                expression = [current_token, [expression, term]]
            # MINUS
            case TokenType.MINUS:
                # term
                term, current_token_index = parse_term(tokens, current_token_index)
                expression = [current_token, [expression, term]]
            case _:
                raise Exception("parse_expression", "Unexpected token:", tokens[current_token_index])

    return expression, current_token_index
```

### <a name="term" class="anchor"></a> [Term](#term)

The term rule is similar to the expression rule but matches `MULTIPLY` or `DIVIDE` instead of `PLUS` or `MINUS`. It first calls `parse_factor`, which is non-optional, then the optional part zero or more times.

```python
# term ::= factor ((MULTIPLY | DIVIDE) factor)*
def parse_term(tokens, current_token_index):
    term = []
    
    # factor
    factor, current_token_index = parse_factor(tokens, current_token_index)
    term = factor

    while current_token_index < len(tokens) and (tokens[current_token_index].m_type == TokenType.MULTIPLY or tokens[current_token_index].m_type == TokenType.DIVIDE):
        current_token = tokens[current_token_index]
        current_token_index += 1
        match current_token.m_type:
            # MULTIPLY
            case TokenType.MULTIPLY:
                # factor
                factor, current_token_index = parse_factor(tokens, current_token_index)
                term = [current_token, [term, factor]]
            # DIVIDE
            case TokenType.DIVIDE:
                # factor
                factor, current_token_index = parse_factor(tokens, current_token_index)
                term = [current_token, [term, factor]]
            case _:
                raise Exception("parse_term", "Unexpected token:", tokens[current_token_index])

    return term, current_token_index
```

### <a name="factor" class="anchor"></a> [Factor](#factor)

The factor rule has the lowest precedence and matches either an `INTEGER` or `LPAR`, which indicates the start of another expression. If `LPAR` is matched, then it calls `parse_expression` and the process starts all over again. It finally matches `RPAR` or raises an error (no closing parantheses).

```python
# factor ::= INTEGER | LPAR expression RPAR
def parse_factor(tokens, current_token_index):
    factor = []
    current_token = tokens[current_token_index]
    current_token_index += 1
    
    match current_token.m_type:
        # INTEGER
        case TokenType.INTEGER:
            factor = current_token
        # LPAR
        case TokenType.LPAR:
            # expression
            expression, current_token_index = parse_expression(tokens, current_token_index)
            factor = expression
            # RPAR
            if current_token_index < len(tokens) and tokens[current_token_index].m_type == TokenType.RPAR:
                current_token_index += 1
            else:
                raise Exception("parse_factor", "Expecting ')':")
        case _:
            raise Exception("parse_factor", "Unexpected token:", tokens[current_token_index])

    return factor, current_token_index
```

There is also a helper function to print nested list as tree.

```python
def print_tree(tree, indent_level=-1):
    if isinstance(tree, list):
        for item in tree:
            print_tree(item, indent_level + 1)
    else:
        indent = '\t' * indent_level
        print(f"{indent}{tree}")
```

The parser is now complete.

```python
tokens = tokenize("print 1 + (2 * 4) - (6 / 2) -> 6")
tree = parse(tokens)
print_tree(tree)
# Token(TokenType.KEYWORD, 'PRINT')
#     Token(TokenType.MINUS, '-')
#             Token(TokenType.PLUS, '+')
#                 Token(TokenType.INTEGER, '1')
#                     Token(TokenType.MULTIPLY, '*')
#                         Token(TokenType.INTEGER, '2')
#                         Token(TokenType.INTEGER, '4')
#             Token(TokenType.DIVIDE, '/')
#                 Token(TokenType.INTEGER, '6')
#                 Token(TokenType.INTEGER, '2')

```

## <a name="interpreter" class="anchor"></a> [Interpreter](#interpreter)

The interpreter is the final step. It takes the tree, recursively evaluates it, and returns the result. Nothing more than that as of yet. It works by matching the left-most node, which should be a keyword, operator, or number, and evaluating the right (children).

In our example program, it matches the keyword (currently only `PRINT`) and calls `interpret` on the right node. If it is an operator then it evaluates the expression on the right node and returns the result. A number simply returns the number.

```python
def interpret(tree):
    result = ''
    node = tree
    if isinstance(node, list):
        left = node[0]
        right = node[1]
    else:
        left = node
        right = None

    match left.m_type:
        case TokenType.KEYWORD if left.m_value == PRINT:
            print(interpret(right))
        case TokenType.PLUS:
            result = int(interpret(right[0])) + int(interpret(right[1]))
        case TokenType.MINUS:
            result = int(interpret(right[0])) - int(interpret(right[1]))
        case TokenType.MULTIPLY:
            result = int(interpret(right[0])) * int(interpret(right[1]))
        case TokenType.DIVIDE:
            result = int(interpret(right[0])) / int(interpret(right[1]))
        case _:
            # NUMBER
            if left.m_value.isdigit():
                return left.m_value
            else:
                raise Exception("interpret", "Unexpected node:", node)

    return result
```

```python
tokens = tokenize("print 1 + (2 * 4) - (6 / 2) -> 6")
tree = parse(tokens)

interpret(tree)
# 6
```

It prints `6`, which is the correct behaviour.

