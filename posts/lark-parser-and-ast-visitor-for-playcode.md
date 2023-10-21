# Lark parser generator and AST visitor for PlayCode

<mark>October 20, 2023</mark> by [Michael Sjöberg](/about.html)

I have never really used parser generators. I briefly tried YACC, Bison, and ANTLR, but didn't like it. I prefer to write my own recursive descent parsers, it's more fun (sometimes!) and it's nice to have full control over the AST layout.

However, I do have many language-related ideas lined up for PlayCode, and it would be great to not having to re-write parts of the parser every time there is a change in the grammar.

So, in this post, I want to explore implementing a subset of PlayCode using [Lark](https://github.com/lark-parser/lark).

## Lark grammar

A Lark parser is generated from the `.lark` grammar file, so first need to translate PlayCode's pseudo-grammar into the syntax used by Lark. It's [very similar](https://lark-parser.readthedocs.io/en/latest/grammar.html) to EBNF.

Below is a subset of PlayCode's grammar for Lark. You can see the full up-to-date grammar [here](https://github.com/mxsjoberg/playcode/blob/main/pc.lark).

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

I like the built-in patterns for numbers, strings, whitespace, and so on. The `->` followed by `add`, `sub`, etc., are aliases to match for addition and subtraction expressions (and not inline asserts as in PlayCode).

Parsing the grammar file and creating a parser looks like this:

```python
parser = Lark(open("pc.lark", "r").read(), start="assign_stmt", parser="lalr")
```

Simple enough. Then to parse input file to generate an AST.

```python
file = open(sys.argv[1], "r").read()
tree = parser.parse(file)
```

Here's an example input (in file passed as `sys.argv[1]`) and the resulting AST:

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

This is a much more verbose tree than what I would normally construct when writing a parser, especially for such as simple input. Maybe a little too verbose? I could always do another pass over the AST (a pre-visitor?) to reconstruct it without the `Tree`, `Token`, and `RULE` all over the place.

## AST visitor

Building the AST visitor is surprisingly straightforward, basically just matching rule names, aliases, and returning the expected behaviour. Again, I'm only including the parts of the function that is relevant for this post, see the full up-to-date code [here](https://github.com/mxsjoberg/playcode/blob/main/pc.py).

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

```python
visitor(tree)
print(SYMBOL_TABLE)
# {'x': 2, 'y': 3}
```

Now, this is nice. You can basically write the typical calculator example in only a few lines with the correct grammar.

# Replacing the old parser and interpreter

I have replaced the PlayCode tokenizer, parser, and interpreter with the Lark generated parser and AST visitor. I think it will be much more maintainable frequent changes to the grammar, which is the whole point of an experimental programming language.

PlayCode is open source and all code is available [here](https://github.com/mxsjoberg/playcode).
