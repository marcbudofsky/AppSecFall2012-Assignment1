#[x for x in [].__class__.__class__("", (),
#    {"__iter__": lambda self: self,
#    "next": lambda self: 1})()
#    if 0]

foo = []
for cnt in range(100000000):
    foo.append(cnt)

print foo