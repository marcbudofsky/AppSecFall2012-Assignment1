##
# CS 9163: Application Security
# Professor Justin Cappos, Professor Dan Guido
# maliciousTest.py
# 
# @author       Marc Budofsky <mrb543@students.poly.edu>
# @created      September 16, 2012
# @modified     September 16, 2012
# 
# Malicious Test Code
# Found On: http://www.python-forum.org/pythonforum/viewtopic.php?f=2&t=23456
##

[x for x in [].__class__.__class__("", (),
    {"__iter__": lambda self: self,
    "next": lambda self: 1})()
    if 0]