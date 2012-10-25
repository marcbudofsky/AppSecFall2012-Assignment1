##
# CS 9163: Application Security
# Professor Justin Cappos, Professor Dan Guido
# TestCase03.py
# 
# @author       Marc Budofsky <mrb543@students.poly.edu>
# @created      September 10, 2012
# @modified     September 10, 2012
# 
# Compute Factorial; Print out values
##

def factorial(x):
    if x == 0:
        return 1
    else:
        return x * factorial(x-1)
        
if len(argv) < 2:
    print "Usage:", argv[0], "number"
    exit()
    
try:
    rng = int(argv[1])
except:
    print "A number is required to run:", str(argv[1])[1:-1]
    exit()
    
for foo in range (rng):
    fact = factorial(foo)

print fact
