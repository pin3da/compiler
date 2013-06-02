Minipascal compiler
===================

Manuel Felipe Pineda -
Carlos Alvaro Gonzales

A minipascal compiler for my compliers course on Universidad Tecnologica de Pereira.

this is a free software project, if you want copy/change/modify for academic purposes, feel free to do it (Remember to give credit and thanks to the creators).

if you want to check the code, you can run any of pascal codes in test dir

### to run
    
    python <phase>.py path_to_file.pas

where <phase> can be: mpaslexer , mpasparser , semantic


- Lexer returns a list with all tokens of program
- Parser generate a .png image which will contains the AST for your progam, this file will be create at "path_to_file.png"
- Semantic checks your progam and advertises you about the problems

### to compile

    python mpascal.py path_to_file.pas

This section is incomplete

##enjoy!


_________
https://github.com/pin3da/compiler
