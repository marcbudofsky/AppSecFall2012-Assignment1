##
# CS 9163: Application Security
# Professor Justin Cappos, Professor Dan Guido
# Sandbox.py
#
# @author       Marc Budofsky <mrb543@students.poly.edu>
# @created      September 6, 2012
# @modified     September 14, 2012
#
# Secure Turing Complete Sandbox Challenge
# Executes 'Pythonic' Scripts (Limited Subset of Python)
##

#---Imports-------------------------------------------------------------
import os
import sys
import inspect
import resource
import collections
from __builtin__ import *

#---Globals-------------------------------------------------------------
MAX_MEMORY  = 1024 * 16

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
    # 'tuple', 'unichr', 'unicode',
    'vars', 'type',
    # 'xrange', 'zip',
]

# Compute Allowed Functions for eval()/exec(): http://stackoverflow.com/questions/5094083/find-the-overlap-between-2-python-lists
all_functions_multiset = collections.Counter(all_functions_list)
blacklist_functions_multiset = collections.Counter(blacklist_functions_list)

allowed_functions_list = sorted(list((all_functions_multiset - blacklist_functions_multiset).elements()))

allowed_functions_dict = dict([ (foo, locals().get(foo)) for foo in allowed_functions_list ])

# Allowed List of Built In Types
allowed_types_list = [
    'True', 'False',
    'int', 'float', 'long', 'complex',
    'str', 'unicode', 'list', 'tuple', 'buffer', 'xrange',
]

allowed_types_dict = dict([ (foo, locals().get(foo)) for foo in allowed_types_list ])

# Compute Total List of Allows
all_allowed_dict = dict(allowed_types_dict.items() + allowed_functions_dict.items())

#---System Settings-----------------------------------------------------
# Set Minimum/Maximum Data Memory:  http://docs.python.org/library/resource.html
#                                   http://stackoverflow.com/questions/2308091/how-to-limit-python-heap-size
resource.setrlimit(resource.RLIMIT_DATA, (MAX_MEMORY, MAX_MEMORY))
resource.setrlimit(resource.RLIMIT_STACK, (MAX_MEMORY, MAX_MEMORY))

#---Functions-----------------------------------------------------------
# Allow User Functions in Sandbox:
#   http://stackoverflow.com/questions/10850052/python-have-a-user-defined-function-as-an-input-while-keeping-the-source-code-i
def createUserFunction(src):
    comp = compile(src, "<string>", "exec")
    exec comp
    functionName = list(set(locals()))[0]
    functionCall = locals()[functionName]
    return functionCall
    
def main():
    if (len(sys.argv) < 2):
    	print "Usage:", sys.argv[0], "script_to_run.py { <script_to_run_arg_1> <script_to_run_arg_2> ... }"
    	sys.exit(1)
    
    scriptToRun = sys.argv[1]
        
    try:
        user_allowed_dict = all_allowed_dict.copy()
        user_allowed_dict["__builtins__"] = None
        user_allowed_dict["argv"] = sys.argv[1:]
        user_allowed_dict["exit"] = sys.exit
        appfile = [line.replace('\n','') for line in open(scriptToRun, "r") if line[0] != "#"]
        for cnt in range(len(appfile)):
            if appfile[cnt].find("def") != -1:
                functionDef = appfile[cnt].split(' ')[1]
                functionCode = [appfile[cnt]]
                safeCode = True
                while (appfile[cnt].strip() != ""):
                    cnt += 1
                    functionCode.append(appfile[cnt].replace(" ", "\t"))
                    # if any(blacklist in appfile[cnt] for blacklist in blacklist_functions_list):
                    #   safeCode = False
                if safeCode:
                    functionName = functionCode[0].split(' ')[1].split('(')[0]
                    
                    functionSrc = "\n".join(funcLine for funcLine in functionCode)
                    functionComp = createUserFunction(functionSrc)
                    user_functions_dict[functionName] = functionComp
        execfile(scriptToRun,user_allowed_dict)
    except IOError:
        print "File '" + scriptToRun + "' could not be found"
    except SystemExit:
        pass
    except NameError:
        print "Unknown function found in " + scriptToRun
    except:
        print "Error in executing " + scriptToRun
    finally:
        del(user_allowed_dict)
        
main()

## Moshe Notes
# Check if classes are allowed
# Use compile module to traverse tree