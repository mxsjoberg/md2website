# Writing an Interactive Interpreter in Ruby

*October 11, 2023*

I like Ruby. I used to get a chance to write Ruby when working on my personal website (Rails app). However, I recently made the (regrettable?) decision to automate my recreational website programming by generating it from Markdown, so I don't have any active projects using Ruby...

This project aims to fix that! And at the same time, explore different aspects of interactive interpretation of code in a browser-based environment. It's a catchy title. I'm not sure what it all means yet.

I'm thinking something like writing code and being able to "see" into the lexing, parsing, and interpreting processes at each keystroke. Is this feasible? No idea. But it's an idea (and I get to use Ruby again)!

I did not forget about PlayCode (my other language implementation project). It's still very much on my mind and I will get back to it as soon as I feel for working on back-end stuff (targeting LLVM IR). There will be a post on this too soon.

---

## The Plan

I'll start by writing what I consider boilerplate in compilers, lexer and parser (yes, no parser generator [1]). I'll then write a simple interpreter that will be able to execute arithmetic expressions. The parser will enforce operator precedence.

I'm going to use Pascal as the language to interpret. It's simple enough to manage to implement a large subset in a reasonable amount of time. I've also worked with Pascal grammar before so should be easier and faster to get to the more interesting parts.

On the Ruby side, there will be a Sinatra application that serves the front-end (HTML, CSS, JS) and provide the back-end API for the interpreter.

The goal is to interactively provide information about the program as the programmer is still typing. Such as details about token generation, AST structure, potential issues in code, and of course the result or output of the program.

## Ruby web app

The Ruby web app is currently at a cool 25 lines. I don't see this changing too much.

```ruby
require "sinatra"
require "json"
# auto-reload
require "sinatra/reloader"

require_relative "parser"
require_relative "interpreter"

set :views, File.join(settings.root, "views")

get "/" do
    @title = "Pascal in Ruby"
    erb :index
end

post "/update" do
    content_type :json
    request_body = JSON.parse(request.body.read)
    # parse
    characters, tokens, ast, issues = parse(request_body["input"])
    # interpret
    result = interpret(ast)
    # return json
    { message: "ok", characters: characters, tokens: tokens.to_json, ast: ast.to_json, issues: issues.to_json, result: result }.to_json
end
```

I like this. It's short, readable, and just works. It's loading the Sinatra dependencies, setting up auto-reload, and importing parser and interpreter (separate files).

The `/update` route is the API endpoint to parse and interpret, which then returns number of characters (length of program), the generated tokens and AST, any detected issues, and result.

The front-end is nothing more than a few lines of JavaScript fetch, other JavaScript glue-code, and some styling.

## Implementation

The parser is the big chunk of code now. It's currently at 100+ lines (tokenizer and parser is combined).

```ruby
# expr      ::= term (('+' | '-') term)*
# term      ::= factor (('*' | '/') factor)*
# factor    ::= number | '(' expr ')'
```  

It takes this grammar and returns a sequence of tokens and AST. For example, here's output from `20+2-(2*4)`:

```ruby
# tokens
[
    {"type":"number","value":"20","pos":1},
    {"type":"operator","value":"+","pos":2},
    {"type":"number","value":"2","pos":3},
    {"type":"operator","value":"-","pos":4},
    {"type":"parentheses","value":"(","pos":5},
    {"type":"number","value":"2","pos":6},
    {"type":"operator","value":"*","pos":7},
    {"type":"number","value":"4","pos":8},
    {"type":"parentheses","value":")","pos":9}
]
```

```ruby
# ast
[
    "-", [
        ["+",
            ["20","2"]
        ],
        ["*",
            ["2","4"]
        ]
    ]
]
```

It's also detecting issues without breaking program, here's output from `2+`:

```ruby
# tokens
[
    {"type":"number","value":"2","pos":0},
    {"type":"operator","value":"+","pos":1}
]
```

```ruby
# issues
[
    {"pos":2,"issue":"expected term after operator"}
]
```

It's trying to tell you that it expected another number or expression after the addition operator. I might make this clearer later, but it works for now.

There should be a reasonable result with or without issues though, so an input of `2+` results in `2` and `1+(2` results in `3` (assuming closing parentheses at end of input).

## Current status

Operator precedence seems to work, it's updating information on each keystroke, and not too slow (yet).

![https://raw.githubusercontent.com/mxsjoberg/pascal-in-ruby/main/pascal_in_ruby.png](https://raw.githubusercontent.com/mxsjoberg/pascal-in-ruby/main/pascal_in_ruby.png)

Now I just need to add the rest of the language... I'll make another post when it can interpret a larger subset of the Pascal grammar.

The repo for this project is here: [github.com/mxsjoberg/pascal-in-ruby](https://github.com/mxsjoberg/pascal-in-ruby)

[1] *I don't like parser generators. It's a nice idea and always consider using one, but it's just too much "magic" for my taste. I want to control the whole process.*
