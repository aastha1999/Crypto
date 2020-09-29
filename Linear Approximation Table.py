from tabulate import tabulate
import numpy as np

# Random sbox

sbox = [ 3, 4, 5, 0, 0xc, 7, 0xd, 0xa, 1, 2, 6, 8, 9, 0xb, 0xf, 0xe]

# computing the linear approximation 
def linearApprox(input, output):
    total = 0
    for i in range(16):
        # getting input and output 
        input_masked = i & input
        output_masked = sbox[i] & output
        if (bin(input_masked).count("1") - bin(output_masked).count("1")) % 2 == 0:
            total += 1 
    # getting deviations from 1/2
    result = total - 8
    return result
#Storing Values in the table
LAT=np.empty([16,16],dtype=int)
head=[]
for i in range(16):
    for j in range(16):
        LAT[i][j]=linearApprox(i,j)
    head.append((hex(i)).replace('0x',''))
LAT=np.where(LAT==0,'.',LAT)
print(tabulate(LAT,showindex=head,headers=head,tablefmt='fancy_grid'))

#Reference: https://crypto.stackexchange.com/questions/53947/linear-approximation-table-of-s-box-for-spn
