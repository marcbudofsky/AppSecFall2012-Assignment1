# Xor 2 Numbers
try:
    num1 = int(argv[1])
    num2 = int(argv[2])
except:
    print "One of the arguments is not a number:", str(argv[1:])[1:-1]
    exit()
    
bin1 = bin(num1)[2:]
bin2 = bin(num2)[2:]
bin3 = ""

# Padding
if len(bin1) > len(bin2):
    bin2 = bin2.zfill(len(bin1))
else:
    bin1 = bin1.zfill(len(bin2))

for cnt in range(len(bin1)):
    tmp = (int(bin1[cnt]) + int(bin2[cnt])) % 2
    bin3 += str(tmp)
    
num = 0

for cnt in range(len(bin3)):
    num += int(bin3[cnt]) << (len(bin3) - (cnt + 1))
    
print num