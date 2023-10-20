# Lark parser and AST visitor for PlayCode

<mark>October 20, 2023</mark> by [Michael Sjöberg](/about.html)

I never really use parser generators. But I have many language-related ideas that I want to explore without writing a new parser each time, or worse, update after every grammar change... So, I have decided to re-implement a subset of PlayCode using [Lark](https://github.com/lark-parser/lark).

## Lark grammar

A Lark parser is generated based on the `.lark` grammar file, so first need to translate PlayCode's pseudo-grammar into a proper grammar using Lark's syntax. It's very similar to the EBNF dialects that I'm used to, so all good.

Below is a subset of PlayCode's grammar in Lark. It's somewhat simplified to make it more readable, you can see the full up-to-date grammar here: [github.com/mxsjoberg/playcode/blob/main/pc.lark](https://github.com/mxsjoberg/playcode/blob/main/pc.lark)

```lark
assign_stmt : IDENTIFIER "=" expr

expr : term
     | term "+" term        -> add
     | term "-" term        -> sub

term : factor
     | factor "*" factor    -> mul
     | factor "/" factor    -> div

factor : NUMBER             -> number
       | IDENTIFIER         -> identifier
       | "(" expr ")"

COMMENT : ("--" | "->") /[^\n]*/

%import common.CNAME        -> IDENTIFIER
%import common.NUMBER
%import common.WS

%ignore WS
%ignore COMMENT
```

I like the built-in patterns for numbers, strings, whitespace, and so on. The `-> add` is an alias to match case for addition expression (and not assert as in PlayCode).

Here's an example program and the generated AST:

```python
x = 2
y = 2 + (x - 1)
```

```
Tree(Token('RULE', 'program'), [
    Tree(Token('RULE', 'assign_stmt'), [
        Token('IDENTIFIER', 'x'),
        Tree(Token('RULE', 'expr'), [
            Tree(Token('RULE', 'term'), [
                Tree('number', [Token('NUMBER', '2')])
            ])
        ])
    ]),
    Tree(Token('RULE', 'assign_stmt'), [
        Token('IDENTIFIER', 'y'),
        Tree('add', [
            Tree(Token('RULE', 'term'), [
                Tree('number', [Token('NUMBER', '2')])
            ]),
            Tree(Token('RULE', 'term'), [
                Tree(Token('RULE', 'factor'), [
                    Tree('sub', [
                        Tree(Token('RULE', 'term'), [
                            Tree('identifier', [Token('IDENTIFIER', 'x')])
                        ]),
                        Tree(Token('RULE', 'term'), [
                            Tree('number', [Token('NUMBER', '1')])
                        ])
                    ])
                ])
            ])
        ])
    ])
])
```

It's a verbose tree. Maybe a little too verbose?

## AST visitor

Writing the AST visitor is surprisingly straightforward as well, basically just matching rule names and aliases. Again, I'm only showing the parts of the visitor function that is relevant for this subset of the grammar, see the full up-to-date AST visitor here: [github.com/mxsjoberg/playcode/blob/main/pc.py](https://github.com/mxsjoberg/playcode/blob/main/pc.py)

```python
def visitor(tree):
    match tree.data:
        case "assign_stmt":
            left, right = tree.children
            SYMBOL_TABLE[left] = visitor(right)
        case "expr":
            return visitor(tree.children[0])
        case "term":
            return visitor(tree.children[0])
        case "factor":
            return visitor(tree.children[0])
        case "number":
            return int(tree.children[0])
        case "identifier":
            return SYMBOL_TABLE[tree.children[0]]
        case "add":
            left, right = tree.children
            return int(visitor(left)) + int(visitor(right))
        case "sub":
            left, right = tree.children
            return int(visitor(left)) - int(visitor(right))
```

Running this and printing the symbol table gives the expected result.

```python
print(SYMBOL_TABLE)
# {Token('IDENTIFIER', 'x'): 2, Token('IDENTIFIER', 'y'): 3}
```
