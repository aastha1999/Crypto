import numpy as np
from copy import copy
from tabulate import tabulate

# Rijndael S-box
sbox = np.array( [0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67,
            0x2b, 0xfe, 0xd7, 0xab, 0x76, 0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59,
            0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0, 0xb7,
            0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1,
            0x71, 0xd8, 0x31, 0x15, 0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05,
            0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75, 0x09, 0x83,
            0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29,
            0xe3, 0x2f, 0x84, 0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b,
            0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf, 0xd0, 0xef, 0xaa,
            0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c,
            0x9f, 0xa8, 0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc,
            0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2, 0xcd, 0x0c, 0x13, 0xec,
            0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19,
            0x73, 0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee,
            0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb, 0xe0, 0x32, 0x3a, 0x0a, 0x49,
            0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
            0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4,
            0xea, 0x65, 0x7a, 0xae, 0x08, 0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6,
            0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a, 0x70,
            0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9,
            0x86, 0xc1, 0x1d, 0x9e, 0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e,
            0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf, 0x8c, 0xa1,
            0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0,
            0x54, 0xbb, 0x16] )

# For Key generation using openssl rand
# import os
# key=(os.popen('openssl rand -hex 16').read()[:-1])
# print(key)
key='0aea88fbafb0350b66b62eaa62340c40'

s1 = np.array([0x0a,0xea,0x88,0xfb,
     0xaf,0xb0,0x35,0x0b,
     0x66,0xb6,0x2e,0xaa,
     0x62,0x34,0x0c,0x40])

s2 = np.array([0x1a,0xea,0x88,0xfb,
     0xaf,0xb0,0x35,0x0b,
     0x66,0xb6,0x2e,0xaa,
     0x62,0x34,0x0c,0x40])

s1xs2=[0]*16

def print_states(s1,s2):
    print("State 1")
    print(tabulate(s1.reshape(4,4),tablefmt='fancy_grid'))
    print("\n")
    print("State 2")
    print(tabulate(s2.reshape(4,4),tablefmt='fancy_grid'))
    print("\n")

def print_matrix_xor(s1xs2,s1,s2):
    for i in range(16):
        s1xs2=s1^s2
    print(tabulate(s1xs2.reshape(4,4),tablefmt='fancy_grid'))
    print("\n")

print_states(s1,s2)
print("Matrix after Xoring the states:")
print_matrix_xor(s1xs2,s1,s2)

print("Round 1 of AES Starts")
print("\n")
master_key=np.array(['0x83','0x52', '0xed', '0x2f',
                     '0x83' ,'0x20', '0x83', '0x83',
                     '0x52' ,'0x04', '0xed', '0xb7',
                     '0x04' ,'0x20', '0x83', '0x83'])
print("Master key")
print((tabulate(master_key.reshape(4,4),tablefmt='fancy_grid')))
print("\n")

#Xoring the states with the master key
def key_xor(key,s1,s2):
    for i in range(16):
        key[i]=int(key[i],16)
        s1[i]=s1[i]^(int(master_key[i]))
        s2[i]=s2[i]^(int(master_key[i]))

key_xor(master_key,s1,s2)
print("States after Xoring with Master Key")
print_states(s1,s2)

print("Matrix after Xoring the states with Master Key:")
print_matrix_xor(s1xs2,s1,s2)

#Applying Confusion: Substitute Bytes
def subByte(s1,s2):
    for i in range(16):
        s1[i]=sbox[s1[i]]
        s2[i]=sbox[s2[i]]

subByte(s1,s2)
print("States after SubBytes Operation:")
print_states(s1,s2)

print("Matrix after Xoring the states after SubBytes Operation:")
print_matrix_xor(s1xs2,s1,s2)


#Applying Diffusion, Part1:Shift Rows
def shiftRow(s1,s2):
    for i in range(1,4):
        (s1.reshape(4,4))[i]=np.roll((s1.reshape(4,4))[i], -i)
        (s2.reshape(4,4))[i]=np.roll((s2.reshape(4,4))[i], -i)

shiftRow(s1,s2)
print("States after ShiftRows Operation:")
print_states(s1,s2)

print("Matrix after Xoring the states after ShiftRows Operation:")
print_matrix_xor(s1xs2,s1,s2)

#Applying Diffusion, Part2: Mix Columns
# Reference: http://anh.cs.luc.edu/331/code/aes.py , https://gist.github.com/raullenchai/2920069 , https://en.wikipedia.org/wiki/Rijndael_MixColumns
# Each column is used as a polynomial. It is then multiplied with 3x^3 + x^2 + x + 2 then their resultant is taken modulo with x^4 + 1. After this, it simplifies to a simple matrix multiplication.

# Galois Multiplication
def galoisMult(a, b):
    p = 0
    hiBitSet = 0
    for i in range(8):
        if b & 1 == 1:
            p ^= a
        hiBitSet = a & 0x80
        a <<= 1
        if hiBitSet == 0x80:
            a ^= 0x1b
        b >>= 1
    return p % 256

# galois multiplication of 1 column of the 4x4 matrix
def mixColumn(column):
    temp = copy(column)
    column[0] = galoisMult(temp[0],2) ^ galoisMult(temp[3],1) ^ \
                galoisMult(temp[2],1) ^ galoisMult(temp[1],3)
    column[1] = galoisMult(temp[1],2) ^ galoisMult(temp[0],1) ^ \
                galoisMult(temp[3],1) ^ galoisMult(temp[2],3)
    column[2] = galoisMult(temp[2],2) ^ galoisMult(temp[1],1) ^ \
                galoisMult(temp[0],1) ^ galoisMult(temp[3],3)
    column[3] = galoisMult(temp[3],2) ^ galoisMult(temp[2],1) ^ \
                galoisMult(temp[1],1) ^ galoisMult(temp[0],3)

# mixColumns is a wrapper for mixColumn - generates a "virtual" column from the state table and applies the galois math
def mixColumns(state):
    for i in range(4):
        column = []
        # create the column by taking the same item out of each "virtual" row
        for j in range(4):
            column.append(state[j*4+i])

        # apply mixColumn on our virtual column
        mixColumn(column)

        # transfer the new values back into the state table
        for j in range(4):
            state[j*4+i] = column[j]

mixColumns(s1)
mixColumns(s2)
print("States after MixColumns Operation:")
print_states(s1,s2)

print("Matrix after Xoring the states after MixColumns Operation:")
print_matrix_xor(s1xs2,s1,s2)

#Round Key 1
k0=np.array([['0x6e', '0x3c', '0xd1', '0xfe'],
             ['0x2a' ,'0x0a', '0x89', '0x0a'],
             ['0xbe', '0xba', '0x57', '0xe0'],
             ['0x11', '0x31', '0xb2', '0x31']])
k0=k0.reshape(16,)
print("Round Key 1")
print(tabulate(k0.reshape(4,4),tablefmt='fancy_grid'))
print("\n")

#Key XOR with Round key 1
key_xor(k0,s1,s2)
print("States after Xoring with Round Key 1")
print_states(s1,s2)

print("Matrix after Xoring the states with Round Key 1:")
print_matrix_xor(s1xs2,s1,s2)

print("Round 1 of AES Complete")
print("\n")
print("Round 2 Starts")
print("\n")

subByte(s1,s2)
print("States after SubBytes Operation:")
print_states(s1,s2)

print("Matrix after Xoring the states after SubBytes Operation:")
print_matrix_xor(s1xs2,s1,s2)

shiftRow(s1,s2)
print("States after ShiftRows Operation:")
print_states(s1,s2)

print("Matrix after Xoring the states after ShiftRows Operation:")
print_matrix_xor(s1xs2,s1,s2)

mixColumns(s1)
mixColumns(s2)
print("States after MixColumns Operation:")
print_states(s1,s2)

print("Matrix after Xoring the states after MixColumns Operation:")
print_matrix_xor(s1xs2,s1,s2)

#Round Key for round 2
k1=np.array([['0x0b', '0x37', '0xe6', '0x18'],
 ['0xcb' ,'0xc1', '0x48', '0x42'],
 ['0x79', '0xc3', '0x94', '0x74'],
 ['0xaa' ,'0x9b', '0x29' ,'0x18']])

k1=k1.reshape(16,)
print("Round Key 2")
print(tabulate(k1.reshape(4,4),tablefmt='fancy_grid'))
print("\n")

#Key XOR with Round key 1
key_xor(k1,s1,s2)
print("States after Xoring with Round Key 2")
print_states(s1,s2)

print("Matrix after Xoring the states with Round Key 2:")
print_matrix_xor(s1xs2,s1,s2)

print("Round 2 of AES Complete")
print("\n")
