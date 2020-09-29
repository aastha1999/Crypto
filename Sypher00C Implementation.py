import numpy as np
from tabulate import tabulate
S_box={0:15,1:14,2:11,3:12,4:6,5:13,6:7,7:8,8:0,9:3,10:9,11:10,12:4,13:2,14:1,15:5} #S-Box used in Sypher00C
def get_key(val):
    for key,value in S_box.items():
        if val==value:
            return key

# For Key generation using openssl rand
# import os
# key=(os.popen('openssl rand -hex 2').read()[:-1])
# print(key)
# key=74ad
#Generated Keys
k0=7
k1=14
k2=4
k3=9
cipher=[]
pairs=[]
#Calculating Cipher text values for the message by passing the message through the Trail
for m in range(0,16):
    out1=S_box.get(m^k0)
    out2=S_box.get(out1^k1)
    out3=S_box.get(out2^k2)
    cipher.append(k3^out3)
    pairs.append(str((m,cipher[m])))
print("Values of ciphertext:")
print(cipher)
print("\n")

y_prime=np.empty([16,16],dtype=int)
#y'=S^(-1)[c XOR i] for each guess of key, inverting the S-box value of XOR of key and cipher text
for i in range(0,16):
    for c in range(0,16):
        y_prime[c][i]=get_key(cipher[c]^i)
print("y' values of all key guesses are:")
print("\n")
headers=["index","k3[0]","k3[1]","k3[2]","k3[3]","k3[4]","k3[5]","k3[6]","k3[7]","k3[8]","k3[9]","k3[10]","k3[11]","k3[12]","k3[13]","k3[14]","k3[15]"]
print(tabulate(y_prime,showindex=pairs,headers=headers,tablefmt='simple'))
print("\n")

#Calculating (d.m)XOR(d.y') for all y' for all key guesses
T0=[0]*16
T1=[0]*16
head=[]
counter=np.empty([16,32],dtype=int)
for m in range(0,16):
    for y in range(0,16):
        dot_m= 13&y
        dot_y=13&(y_prime[y][m])        
        mb1=int(dot_m%2)
        dot_m=dot_m/2
        mb2=int(dot_m%2)
        dot_m=dot_m/2
        mb3=int(dot_m%2)
        dot_m=dot_m/2
        mb4=int(dot_m%2)
        cb1=int(dot_y%2)
        dot_y=dot_y/2
        cb2=int(dot_y%2)
        dot_y=dot_y/2
        cb3=int(dot_y%2)
        dot_y=dot_y/2
        cb4=int(dot_y%2)
        dot_y=dot_y/2
        xor_t1= mb1^mb2^mb3^mb4^cb1^cb2^cb3^cb4
        xor_t0= (mb1^mb2^mb3^mb4^cb1^cb2^cb3^cb4)^1
        if(xor_t1==1):
            T1[m]+=1
        if(xor_t0==1):
            T0[m]+=1
        counter[y][2*m]=xor_t0
        counter[y][2*m+1]=xor_t1
    head.append(str((m,'T0')))
    head.append(str((m,'T1')))
print("values of [ (d.m) XOR (d.y') ]")
print("\n")
#If table overflows, uncomment the below line to print table without headings
print(tabulate(counter,showindex=pairs,tablefmt='fancy_grid'))
#print(tabulate(counter,showindex=pairs,headers=head,tablefmt='simple'))
print("\n")
print("Values of sum of T0")
print(T0)
print("\n")
print("Values of sum of T1")
print(T1)
print("\n")
Imbalance=abs(np.array(T1)-8)
print("Possible Values of k3 are:")
for i in range(0,16):
    if(Imbalance[i]==max(Imbalance)):
        print(i)
print("\n")

#Now for key Recovery of k0
rcvk0=np.empty([16,16],dtype=int)
for i in range(0,16):
    for m in range(0,16):
        rcvk0[m][i]=S_box.get(m^i)
print("m' values for all guesses of k0")
print("\n")
print(tabulate(rcvk0,showindex=pairs,headers=["index","k0[0]","k0[1]","k0[2]","k0[3]","k0[4]","k0[5]","k0[6]","k0[7]","k0[8]","k0[9]","k0[10]","k0[11]","k0[12]","k0[13]","k0[14]","k0[15]"],tablefmt='simple'))
print("\n")

counter2=np.empty([16,32],dtype=int)
T1_for_k0=[0]*16
T0_for_k0=[0]*16
#calculating (d.m')XOR(d.c) for all m' for all key guesses for k0
for m in range(0,16):
    for c in range(0,16):
        dot_c= 13&(cipher[c])
        dot_m=13&(rcvk0[c][m])
        mb1=int(dot_m%2)
        dot_m=dot_m/2
        mb2=int(dot_m%2)
        dot_m=dot_m/2
        mb3=int(dot_m%2)
        dot_m=dot_m/2
        mb4=int(dot_m%2)
        cb1=int(dot_c%2)
        dot_c=dot_c/2
        cb2=int(dot_c%2)
        dot_c=dot_c/2
        cb3=int(dot_c%2)
        dot_c=dot_c/2
        cb4=int(dot_c%2)
        dot_c=dot_c/2
        xor_t1= mb1^mb2^mb3^mb4^cb1^cb2^cb3^cb4
        xor_t0= (mb1^mb2^mb3^mb4^cb1^cb2^cb3^cb4)^1
        if(xor_t1==1):
            T1_for_k0[m]+=1
        if(xor_t0==1):
            T0_for_k0[m]+=1
        counter2[c][2*m]=xor_t0
        counter2[c][2*m+1]=xor_t1
print(" Values of [ (d.m')XOR(d.c) ] ")
#The columns represent values of T0 and T1 for a each guess of k0
print("\n")
#print(tabulate(counter2,showindex=pairs,headers=head,tablefmt='simple'))
#If table overflows, uncomment the below line to print table without headings
print(tabulate(counter2,showindex=pairs,tablefmt='fancy_grid'))
print("\n") 
print("Values of sum of T0")
print(T0_for_k0)
print("\n")   
print("Values of sum of T1")
print(T1_for_k0)
print("\n")
Imbalance=abs(np.array(T1_for_k0)-8)
print("Possible Values of k0 are:")
for i in range(0,16):
    if(Imbalance[i]==max(Imbalance)):
        print(i)
