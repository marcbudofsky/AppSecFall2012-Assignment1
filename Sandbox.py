##
# CS 9163: Application Security
# Professor Justin Cappos, Professor Dan Guido
# Sandbox.py
#
# @author       Marc Budofsky <mrb543@students.poly.edu>
# @created      September 6, 2012
# @modified     September 7, 2012
#
# Secure Turing Complete Sandbox Challenge
##

#---Imports-------------------------------------------------------------
import resource, inspect, os, collections, threading
from __builtin__ import *

#---Globals-------------------------------------------------------------
DEBUG       = False
MAX_MEMORY  = 4096

# List of All Functions for eval()/exec():  http://stackoverflow.com/questions/4040620/is-it-possible-to-list-all-functions-in-a-module
#                                           http://docs.python.org/library/inspect.html
all_functions_list = [func for (func, obj) in inspect.getmembers(__builtins__) if inspect.isbuiltin(obj)]

# Blacklist of Functions for eval()/exec(): http://lybniz2.sourceforge.net/safeeval.html
#                                           http://docs.python.org/library/functions.html
blacklist_functions_list = [
    '__import__',
    # 'abs', 'all', 'any',
    'apply',
    # 'basestring', 'bin', 'bool', 'buffer',
    'bytearray',
    # 'callable', 'chr', 'classmethod', 'cmp', 'coerce', 'complex',
    'compile', 'delattr',
    # 'dict', 'dir', 'divmod', 'enumerate',
    'exec', 'eval', 'execfile', 'file',
    # 'filter', 'float', 'format', 'frozenset',
    'getattr', 'globals', 'hasattr',
    # 'hash', 'help', 'hex',
    'id', 'input', 
    # 'int', 'intern', 'isinstance', 'issubclass', 'iter',
    'locals', 
    # 'len', 'list', 'long',
    # 'map', 'max', 'min', 'next', 'object', 'oct', 'ord',
    'memoryview', 'open',
    # 'pow', 'print', 'property', 'range',
    'raw_input', 'reload',
    # 'reduce', 'repr', 'reversed', 'round', 'set',
    'setattr',
    # 'slice', 'sorted', 'staticmethod', 'str', 'sum', 'super',
    # 'tuple', 'type', 'unichr', 'unicode',
    'vars',
    # 'xrange', 'zip',
]

# Compute Allowed Functions: http://stackoverflow.com/questions/5094083/find-the-overlap-between-2-python-lists
all_functions_multiset = collections.Counter(all_functions_list)
blacklist_functions_multiset = collections.Counter(blacklist_functions_list)

allowed_functions_list = sorted(list((all_functions_multiset - blacklist_functions_multiset).elements()))

allowed_functions_dict = dict([ (foo, locals().get(foo)) for foo in allowed_functions_list ])

#---System Settings-----------------------------------------------------
# Set Minimum/Maximum Data Memory:  http://docs.python.org/library/resource.html
#                                   http://stackoverflow.com/questions/2308091/how-to-limit-python-heap-size
resource.setrlimit(resource.RLIMIT_DATA, (MAX_MEMORY, MAX_MEMORY))

#---Functions-----------------------------------------------------------
def printMenu():
    print "---Sandbox Menu-----------------------------------------------------"
    print "\t1. Count from 10 to 1"
    print "\t2. Compute first 10 Fibonacci Numbers"
    print "\t3. Sandbox"
    print "\t4. User Defined Script"
    print "\t5. Print Sandbox Information"
    print "\t0. Exit"
    print "--------------------------------------------------------------------"

def main():
    while(True):
        printMenu()
        menuOption = int(raw_input("Selection: "))
        filename = ""
        
        if menuOption == 1:
            filename = "TestCase01.py"
            print "Count from 10 to 1"
        elif menuOption == 2:
            filename = "TestCase02.py"
            print "Compute first 10 Fibonacci Numbers"
        elif menuOption == 3:
            filename = "Sandbox_Small.py"
        elif menuOption == 4:
            filename = raw_input("File Name: ")
            print filename
        elif menuOption == 5:
            mem = resource.getrlimit(resource.RLIMIT_DATA)
            print "\nSandbox Information"
            print "Memory Limit: " + str(mem[0]) + " Kb"
            print "Allowed Functions: " + str(allowed_functions_list)[1:-1] + "\n"
        elif menuOption == 0:
            break
        else:
            print "Invalid Menu Selection"
        
        try:
            execfile(filename,{"__builtins__":None},allowed_functions_dict)
        except IOError:
            if menuOption == 4:
                print "File could not be found"
            else:
                pass
        except TypeError:
            print "Code contains an unallowed function"
        #execfile(filename,{"__builtins__":None},allowed_functions_dict)
        
main()