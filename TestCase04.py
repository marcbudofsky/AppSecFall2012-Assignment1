def foo(num):
    return (num - 1) if (num % 2 == 1) else num

def main():
    print argv
    
    joe = frank = bob = 0
    
    joe = 56 * 29
    bob = joe / 3
    frank = joe - bob
    
    print joe, bob, frank
    
    bob = joe = frank
    
    print joe, bob, frank
    
    joe = 9
    
    for cnt in range(joe):
        print bob
    
    print foo(53)
    print foo(67)
    print foo(94)
    
main()