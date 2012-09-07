##
# CS 9163: Application Security
# Professor Justin Cappos, Professor Dan Guido
# Sandbox.py
#
# @author       Marc Budofsky <mrb543@students.poly.edu>
# @created      September 6, 2012
# @modified     September 6, 2012
#
# Secure Turing Complete Sandbox Challenge
##

#---Imports-------------------------------------------------------------
import resource, time, threading

#---Globals-------------------------------------------------------------
DEBUG       = False
MAX_MEMORY  = 4096

# Create Blacklist of Functions for eval(): http://lybniz2.sourceforge.net/safeeval.html
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
resource.setrlimit(resource.RLIMIT_DATA, (MAX_MEMORY, MAX_MEMORY))

#---Functions-----------------------------------------------------------
testFunction01 = "__import__ os"

try:
    print eval(testFunction01,{"__builtins__":None},blacklist_functions_dict)
except TypeError:
    print "Code contains an unallowed function"