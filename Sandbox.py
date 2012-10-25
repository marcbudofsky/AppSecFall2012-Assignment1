##
# CS 9163: Application Security
# Professor Justin Cappos, Professor Dan Guido
# Sandbox.py
#
# @author       Marc Budofsky <mrb543@students.poly.edu>
# @created      September 6, 2012
# @modified     September 17, 2012
#
# Secure Turing Complete Sandbox Challenge
# Executes Python Scripts, using a limited subset of builtin functions
##

#---Imports-------------------------------------------------------------
import sys
import inspect
import resource
import compiler
import collections
from __builtin__ import *

#---Globals-------------------------------------------------------------
MAX_MEMORY  = 1024 * 512        # Set Maximum Memory to 512 MB

# List of All Functions for eval()/exec()
all_functions_list = [func for (func, obj) in inspect.getmembers(__builtins__) if inspect.isbuiltin(obj)]

# Blacklist of Functions for eval()/exec()
blacklist_functions_list = [
    '__import__', 'apply', 'bytearray', 'compile', 'delattr', 'dir',
    'exec', 'eval', 'execfile', 'file', 'getattr', 'globals', 'hasattr',
    'id', 'input',  'locals', 'memoryview', 'open', 'reload', 'setattr', 
    'vars', 'type',
]

## Compute Allowed Functions for eval()/exec() by Subtracting Blacklist from All Functions
all_functions_multiset = collections.Counter(all_functions_list)
blacklist_functions_multiset = collections.Counter(blacklist_functions_list)

allowed_functions_list = sorted(list((all_functions_multiset - blacklist_functions_multiset).elements()))

# Convert to Dictionary
allowed_functions_dict = dict([ (foo, locals().get(foo)) for foo in allowed_functions_list ])
allowed_functions_dict['__name__'] = __name__       # Include to Avoid Errors in Certain Test Cases

# Allowed List of Built In Types
allowed_types_list = [
    'True', 'False', 'int', 'float', 'long', 'complex',
    'str', 'unicode', 'list', 'tuple', 'buffer', 'xrange',
]

# Convert to Dictionary
allowed_types_dict = dict([ (foo, locals().get(foo)) for foo in allowed_types_list ])

# Compute Total List of Allowed Builtins (Functions and Types)
all_allowed_dict = dict(allowed_types_dict.items() + allowed_functions_dict.items())

# List of Allowed Abstract Syntax Trees (ASTs) for User Code Checking [traverseNode(node)]
allowed_nodes = [
    'Add', 'And', 'AssAttr', 'AssList', 'AssName', 'AssTuple', 'Assert', 'Assign', 'AugAssign',
    'Bitand', 'Bitor', 'Bitxor', 'Break',
    'CallFunc', 'Class', 'Compare', 'Const', 'Continue',
    'Decorators', 'Dict', 'Discard', 'Div',
    'Ellipsis', 'Expression', 'FloorDiv', 'For', 'Function',
    'Getattr', 'Global', 'If', 'IfExp', 'Invert', 'Keyword',
    'LeftShift', 'List', 'ListComp', 'ListCompFor', 'ListCompIf',
    'Mod', 'Module', 'Mul', 'Name', 'Not', 
    'Or', 'Pass', 'Power', 'Print', 'Printnl', 
    'Raise', 'Return', 'RightShift',
    'Slice', 'Sliceobj', 'Stmt', 'Sub', 'Subscript',
    'TryExcept', 'TryFinally', 'Tuple', 
    'UnaryAdd', 'UnarySub', 'While', 'Yield'
]

#---System Settings-----------------------------------------------------
# Set Minimum/Maximum Data and Stack Memory
resource.setrlimit(resource.RLIMIT_DATA, (MAX_MEMORY, MAX_MEMORY))
resource.setrlimit(resource.RLIMIT_STACK, (MAX_MEMORY, MAX_MEMORY))

#---Functions-----------------------------------------------------------
## Check Script for Safety
# Receives an AST node tree to traverse and check to make sure all 
# of the nodes are allowed in to be used in the application. If a 
# node is found that is not allowed, an exception is raised.  Functions
# are not checked here due to a whitelist that is passed to the execfile()
# call in main().
def traverseNode(node):
    if node.__class__.__name__ not in allowed_nodes:
        # raise Exception("Error in user code. Program will now exit.")
        raise SyntaxError("%s is not an allowed function!"%node.__class__.__name__)
        
    for childNode in node.getChildNodes():
        traverseNode(childNode)

def main():
    # Ensure application was started properly
    if (len(sys.argv) < 2):
    	print "Usage:", sys.argv[0], "script_to_run.py { <script_to_run_arg_1> <script_to_run_arg_2> ... }"
    	sys.exit(1)
    
    # Store User Script in Local variable
    scriptToRun = sys.argv[1]
        
    try:
        # Create a Local copy of allowed functions; Update several options to ensure proper operation
        user_allowed_dict = all_allowed_dict.copy()
        user_allowed_dict["__builtins__"] = None
        user_allowed_dict["argv"] = sys.argv[1:]
        user_allowed_dict["exit"] = sys.exit
        
        # Create a list of AST Nodes from file; Traverse Nodes to make sure all are allowed
        scriptNodes = compiler.parseFile(scriptToRun)
        traverseNode(scriptNodes)
        
        # Execute File, with limited subset of builtin functions
        execfile(scriptToRun,user_allowed_dict)
    except IOError:
        # Raised if File not found
        print "File '" + scriptToRun + "' could not be found"
    except SystemExit:
        # Raised when Script makes a call to "exit()"; Silently ignore.
        # Without this exception, Sandbox would exit abruptly without
        # deleting `user_allowed_dict` properly
        pass
    except NameError:
        # Inform user script has stopped working due to undeclared function
        print "Unknown function found in " + scriptToRun
    except Exception:
        # General Exception; Raised when unsafe nodes are encountered
        print "An error occured while running " + scriptToRun
    finally:
        # Delete Local copy of allowed functions
        del(user_allowed_dict)
        
if __name__ == "__main__":
    main()