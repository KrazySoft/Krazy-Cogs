from brainfuck import Interpreter
import sys

if len(sys.argv) < 2:
    print("Please initiate Interpreter with {} [code]".format(sys.argv[0]))
else:
    code = str(sys.argv[1])

    interp = Interpreter(channel = 1, tapeLength = -1, wordLength = 8)
    print(interp.Interpret(code))
    print("Run Complete")
