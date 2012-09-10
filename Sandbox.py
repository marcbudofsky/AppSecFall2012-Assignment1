##
# CS 9163: Application Security
# Professor Justin Cappos, Professor Dan Guido
# Sandbox.py
#
# @author       Marc Budofsky <mrb543@students.poly.edu>
# @created      September 6, 2012
# @modified     September 10, 2012
#
# Secure Turing Complete Sandbox Challenge
# Language Run by Sandbox is similar to Python
##

#---Imports-------------------------------------------------------------
import resource, inspect, os, collections, threading, sys
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
    '__import__', # 'import',
    # 'abs', 'all', 'any',
    'apply',
    # 'basestring', 'bin', 'bool', 'buffer',
    'bytearray',
    # 'callable', 'chr', 'classmethod', 'cmp', 'coerce', 'complex',
    'compile', 'delattr', 'dir',
    # 'dict', 'divmod', 'enumerate',
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
    # 'raw_input', 
    'reload',
    # 'reduce', 'repr', 'reversed', 'round', 'set',
    'setattr',
    # 'slice', 'sorted', 'staticmethod', 'str', 'sum', 'super',
    # 'tuple', 'type', 'unichr', 'unicode',
    'vars',
    # 'xrange', 'zip',
]

# Compute Allowed Functions for eval()/exec(): http://stackoverflow.com/questions/5094083/find-the-overlap-between-2-python-lists
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
    print "\t3. Compute 10!"
    print "\t4. Malicious Test"
    print "\t5. User Defined Script"
    print "\t6. Print Sandbox Information"
    print "\t0. Exit"
    print "--------------------------------------------------------------------"

# Allow User Functions in Sandbox:
#   http://stackoverflow.com/questions/10850052/python-have-a-user-defined-function-as-an-input-while-keeping-the-source-code-i
def createUserFunction(src):
    comp = compile(src, "<string>", "exec")
    exec comp
    functionName = list(set(locals()))[0]
    functionCall = locals()[functionName]
    return functionCall

def main(args):
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
            filename = "TestCase03.py"
            print "Compute 10!"
        elif menuOption == 4:
            filename = "malicious.py"
            print "Malicious Test"
        elif menuOption == 5:
            filename = raw_input("File Name: ")
            print filename
        elif menuOption == 6:
            mem = resource.getrlimit(resource.RLIMIT_DATA)
            print "\nSandbox Information"
            print "Memory Limit: " + str(mem[0]) + " Kb"
            print "Allowed Functions: " + str(allowed_functions_list)[1:-1] + "\n"
        elif menuOption == 0:
            break
        else:
            print "Invalid Menu Selection"
        
        try:
            user_functions_dict = allowed_functions_dict.copy()
            user_functions_dict["__builtins__"] = None
            appfile = [line.replace('\n','') for line in open(filename, "r") if line[0] != "#"]
            for cnt in range(len(appfile)):
                if appfile[cnt].find("def") != -1:
                    functionDef  = appfile[cnt].split(' ')[1]
                    functionCode = [appfile[cnt]]
                    safeCode = True
                    while (appfile[cnt].strip() != ""):
                        cnt += 1
                        functionCode.append(appfile[cnt].replace("    ", "\t"))
                        if any(blacklist in appfile[cnt] for blacklist in blacklist_functions_list):
                            safeCode = False
                    if safeCode:
                        functionName = functionCode[0].split(' ')[1].split('(')[0]
                        
                        functionSrc = "\n".join(funcLine for funcLine in functionCode)
                        functionComp = createUserFunction(functionSrc)
                        user_functions_dict[functionName] = functionComp
                        
            execfile(filename,user_functions_dict)
        except IOError:
            if menuOption == 5:
                print "File could not be found"
            else:
                pass
        except NameError, e:
            # print "Unknown function found in code..."
            print "NameError: ", e
        except TypeError, e:
            print "TypeError: ", e
        except ImportError, e:
            print "ImportError: ", e
        finally:
            del(user_functions_dict)
        
main(sys.argv)

# Remove menu >> pass filename as arg to program
# Make sure use of 'execfile()' is allowed
# Check ability to override built in functions with malicious code >> possibly wrap built-ins that are blacklisted