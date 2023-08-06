cstenv.py
cstenv means: custom env lang.

loading a file
    cstenv.load_file(NAME)


defining variables
    let $varname$ = "hello world!"
    let $int$ = 1

loading variables values
    cstenv.var["YOURVARNAMEHERE *with no dollar signs.*"]
