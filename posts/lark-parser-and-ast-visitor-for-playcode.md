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

factor : SIGNED_NUMBER      -> number
       | IDENTIFIER         -> identifier
       | "(" expr ")"

COMMENT : "--" /[^\n]*/

%import common.CNAME -> IDENTIFIER
%import common.SIGNED_NUMBER
%import common.WS

%ignore WS
%ignore COMMENT
```

I like the built-in patterns for numbers, strings, whitespace, and so on. The `-> add` is an alias to match case for addition expression (and not assert as in PlayCode).

Parsing the grammar and generating the parser looks like this:

```python
parser = Lark(open("pc.lark", "r").read(), start="assign_stmt", parser="lalr")
```

Then simply `parser.parse()` input file to generate the AST:

```python
file = open(sys.argv[1], "r").read()
tree = parser.parse(file)
```

Here's an example input and the resulting AST:

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

Writing the AST visitor is surprisingly straightforward, basically just matching rule names, aliases, and returning the expected behaviour.

Again, I'm only including the parts of the visitor function that is relevant for this post, see the full up-to-date AST visitor here: [github.com/mxsjoberg/playcode/blob/main/pc.py](https://github.com/mxsjoberg/playcode/blob/main/pc.py)

```python
def visitor(tree):
    match tree.data:
        case "assign_stmt":
            left, right = tree.children
            SYMBOL_TABLE[left.children[0].value] = visitor(right)
        case "expr":
            return visitor(tree.children[0])
        case "term":
            return visitor(tree.children[0])
        case "factor":
            return visitor(tree.children[0])
        case "add":
            left, right = tree.children
            return int(visitor(left)) + int(visitor(right))
        case "sub":
            left, right = tree.children
            return int(visitor(left)) - int(visitor(right))
        case "number":
            return int(tree.children[0])
        case "identifier":
            return SYMBOL_TABLE[str(tree.children[0])]
```

Running this on the AST and printing the symbol table.

```python
visitor(tree)
print(SYMBOL_TABLE)
# {'x': 2, 'y': 3}
```

# Replacing PlayCode's parser and interpreter

I have replaced both the PlayCode parser and interpreter with the Lark generated parser and AST visitor. I think it will be much more maintainable and faster to make changes to the grammar, which is the whole point of an experimental programming language.

PlayCode is open source and all code is available [here](https://github.com/mxsjoberg/playcode).
