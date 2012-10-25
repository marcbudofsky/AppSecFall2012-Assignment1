##
# Brainfuck Interpreter in Python
# Modified From: https://github.com/lionaneesh/Brainfuck-Python-Interpreter
#
# Used to prove Turing-Completeness for Sandbox.py
##

tape 		   = [int(i) for i in '0' * 3000] 
ptr 		   = 0

def incPtr():
    global ptr
    global tape
    ptr += 1
	
def decPtr():
    global ptr
    global tape
    ptr -= 1

def incByte():
    global ptr
    global tape
    tape[ptr] += 1

def decByte():
    global ptr
    global tape
    tape[ptr] -= 1

def outByte():
    global ptr
    global tape
    print chr(tape[ptr])
    
def getByte():
    global ptr
    global tape
    tape[ptr] = getchar()

def loop(code):
    global ptr
    global tape
    while tape[ptr] != 0:
        bf_eval(code)

commandsList = {'>' : incPtr,
                '<' : decPtr,
                '+' : incByte,
                '-' : decByte,
                '.' : outByte,
                ',' : getByte,
                '[' : loop }

def getchar():
    return ord(raw_input()[0])

def numOccurences(code, tok):
    depth = 0
    loc = code.find(tok)
    while loc != -1:
        loc = code.find(tok, loc+1)
        depth += 1
    return depth

def skipOccurences(code, tok, times):
    c = -1
    for cnt in range(times):
        c = code.find(tok, c+1)
        if c == -1:
            return -1
    return c

def bf_eval(code):
    if not isinstance(code, str):
        return -1
    else:
        cnt = 0
        while cnt < len(code):
            if code[cnt] in commandsList:
                if code[cnt] == '[':
                    subCnt = 0
                    endLoop = code.find(']', cnt)
                    if endLoop == -1:   # Error, no ']' found
                        return -1
                    loopDepth = numOccurences(code[cnt+1:endLoop], '[') # Check for nested loops
                    if loopDepth > 0:   # Nested Loops Found
                        foo     = skipOccurences(code[cnt+1:], ']', loopDepth)  # Find End of Loop
                        subCnt 	= foo + len(code[:cnt+1]) 
                        bar     = code.find(']', subCnt+1)
                        if bar == -1:
                            return -1
                        else:
                            loopDepth = numOccurences(code[subCnt+1:bar], '[') # Check for Additional Nested Loops
                            if loopDepth > 0:   # Handle Nested Loops
                                baz     = skipOccurences(code[subCnt+1:], ']', loopDepth)
                                subCnt 	= baz + subCnt
                                bar     = code.find(']', subCnt+1)
                                if bar == -1:
                                    return -1
                            endLoop = bar
                    # Evaluate Loop
                    loop(code[cnt+1:endLoop])
                    cnt = endLoop
                else:
                    # Execute Command
                    commandsList[code[cnt]]()
            cnt += 1

bf_eval(raw_input(">>>"))