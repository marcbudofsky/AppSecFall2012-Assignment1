##
# CS 9163: Application Security
# Professor Justin Cappos, Professor Dan Guido
# Sandbox_Small.py
#
# @author       Marc Budofsky <mrb543@students.poly.edu>
# @created      September 6, 2012
# @modified     September 7, 2012
#
# Secure Turing Complete Sandbox Challenge
##

#---Imports-------------------------------------------------------------

#---Globals-------------------------------------------------------------
DEBUG       = False
MAX_MEMORY  = 2048

# Blacklist of Functions for eval()/exec(): http://lybniz2.sourceforge.net/safeeval.html
#                                           http://docs.python.org/library/functions.html
blacklist_functions_list = [
    "__import__",
    # "abs", "all", "any",
    "apply",
    # "basestring", "bin", "bool", "buffer",
    "bytearray",
    # "callable", "chr", "classmethod", "cmp", "coerce", "complex",
    "compile", "delattr",
    # "dict", "dir", "divmod", "enumerate",
    "exec", "eval", "execfile", "file",
    # "filter", "float", "format", "frozenset",
    "getattr", "globals", "hasattr",
    # "hash", "help", "hex",
    "id", "input", 
    # "int", "intern", "isinstance", "issubclass", "iter",
    "locals", 
    # "len", "list", "long",
    # "map", "max", "min", "next", "object", "oct", "ord",
    "memoryview", "open",
    # "pow", "print", "property", "range",
    "raw_input", "reload",
    # "reduce", "repr", "reversed", "round", "set",
    "setattr",
    # "slice", "sorted", "staticmethod", "str", "sum", "super",
    # "tuple", "type", "unichr", "unicode",
    "vars",
    # "xrange", "zip",
]

blacklist_functions_dict = dict([ (foo, None) for foo in blacklist_functions_list ])

#---System Settings-----------------------------------------------------
# Set Minimum/Maximum Data Memory:  http://docs.python.org/library/resource.html
#                                   http://stackoverflow.com/questions/2308091/how-to-limit-python-heap-size
# resource.setrlimit(resource.RLIMIT_DATA, (MAX_MEMORY, MAX_MEMORY))

#---Functions-----------------------------------------------------------
testCase01 = """
for foo in range(10,0,-1): 
    print foo
"""

testCase02 = """
def fib(x):
    if x == 0:
        return 0
    elif x == 1:
        return 1
    else:
        return fib(x-1) + fib(x-2)
        
for foo in range (10):
    print fib(foo)
"""

testCase03 = "print locals()"

while(True):
    print "---Sandbox Menu-----------------------------------------------------"
    print "\t1. Count from 10 to 1"
    print "\t2. Compute first 10 Fibonacci Numbers"
    print "\t3. User Defined Script"
    print "\t0. Exit"
    print "--------------------------------------------------------------------"
    menuOption = int(raw_input("Selection: "))
    
    if menuOption == 1:
        filename = "TestCase01.py"
    elif menuOption == 2:
        filename = "TestCase02.py"
    elif menuOption == 3:
        filename = raw_input("File Name: ")
    elif menuOption == 0:
        break
    else:
        print "Invalid Menu Selection"
        
    try:
        execfile(filename,{"__builtins__":None},blacklist_functions_dict)
    except NameError:
        execfile(filename)
    except ImportError:
        print "Imports are not allowed"
    except TypeError:
        print "Code contains an unallowed function"