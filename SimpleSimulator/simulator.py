import sys
from bitstring import BitArray

pc = 0
pc_next=0
r = ["0","0","0","0","0","0","0",["0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0"]]

mem = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
hlt = 0
out = []

def decimal_to_binary(decimal_string,len):
    decimal = int(decimal_string)
    binary = BitArray(uint=decimal, length=len)
    return binary.bin


def print_flag(flag):
    binary_string = ''.join(str(bit) for bit in flag)
    return(binary_string)

def operate(line):
    global pc
    global hlt
    global pc_next
    instr = line[0:5]
    if instr == "00000": #add
        r[BitArray(bin=line[7:10]).uint] = str(int(r[BitArray(bin=line[10:13]).uint]) + int(r[BitArray(bin=line[13::]).uint]))
        r[7] = ["0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0"]
        pc_next = pc + 1

    elif instr == "00001": #sub
        r[BitArray(bin=line[7:10]).uint] = str(int(r[BitArray(bin=line[10:13]).uint]) + int(r[BitArray(bin=line[13::]).uint]))
        r[7] = ["0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0"]
        pc_next = pc + 1

    elif instr == "00110": #mul
        r[BitArray(bin=line[7:10]).uint] = str(int(r[BitArray(bin=line[10:13]).uint]) * int(r[BitArray(bin=line[13::]).uint]))
        r[7] = ["0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0"]
        pc_next = pc + 1

    elif instr == "01010": #xor
        r[BitArray(bin=line[7:10]).uint] = str(int(r[BitArray(bin=line[10:13]).uint]) ^ int(r[BitArray(bin=line[13::]).uint]))
        r[7] = ["0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0"]
        pc_next = pc + 1

    elif instr == "01011": #or
        r[BitArray(bin=line[7:10]).uint] = str(int(r[BitArray(bin=line[10:13]).uint]) | int(r[BitArray(bin=line[13::]).uint]))
        r[7] = ["0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0"]
        pc_next = pc + 1

    elif instr == "01100": #and
        r[BitArray(bin=line[7:10]).uint] = str(int(r[BitArray(bin=line[10:13]).uint]) & int(r[BitArray(bin=line[13::]).uint]))
        r[7] = ["0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0"]
        pc_next = pc + 1

    elif instr == "10001": #mod
        r[BitArray(bin=line[7:10]).uint] = str(int(r[BitArray(bin=line[10:13]).uint]) % int(r[BitArray(bin=line[13::]).uint]))
        r[7] = ["0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0"]
        pc_next = pc + 1

    elif instr == "10100": #pow
        r[BitArray(bin=line[7:10]).uint] = str(int(r[BitArray(bin=line[10:13]).uint]) ** int(r[BitArray(bin=line[13::]).uint]))
        print("please--->",BitArray(bin=line[7:10]).uint)
        r[7] = ["0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0"]
        pc_next = pc + 1

    elif instr == "10000": #xnor
        r[BitArray(bin=line[7:10]).uint] = (str(int(not(int(r[BitArray(bin=line[10:13]).uint]) ^ int(r[BitArray(bin=line[13::]).uint])))))
        r[7] = ["0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0"]
        pc_next = pc + 1

    elif instr == "10010": #nor
        r[BitArray(bin=line[7:10]).uint] = (str(int(not(int(r[BitArray(bin=line[10:13]).uint]) | int(r[BitArray(bin=line[13::]).uint])))))
        r[7] = ["0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0"]
        pc_next = pc + 1

    elif instr == "10011": #nand
        r[BitArray(bin=line[7:10]).uint] = (str(int(not(int(r[BitArray(bin=line[10:13]).uint]) & int(r[BitArray(bin=line[13::]).uint])))))
        r[7] = ["0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0"]
        print(r)
        pc_next = pc + 1
    
    elif instr == "00010": #mov-reg-imm
        r[BitArray(bin=line[6:9]).uint] = str(BitArray(bin=line[-7::]).uint)
        #print(BitArray(bin=line[6:9]).uint) 
        #print("this--->",r[BitArray(bin=line[6:9]).uint])
        r[7] = ["0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0"]
        pc_next = pc + 1

    elif instr == "01000": #rs
        r[BitArray(bin=line[6:9]).uint] = str(int(r[BitArray(bin=line[6:9]).uint]) >> int(r[BitArray(bin=line[-7::]).uint]))
        r[7] = ["0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0"]
        pc_next = pc + 1

    elif instr == "01001": #ls
        r[BitArray(bin=line[6:9]).uint] = str(int(r[BitArray(bin=line[6:9]).uint]) * int(( 2 ** r[BitArray(bin=line[-7::]).uint] )))
        r[7] = ["0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0"]
        pc_next = pc + 1

    elif instr == "00011": #mov-reg-reg
        #print("line:",line)
        #print(r)
        #print("Eureka?!-------------->",BitArray(bin=line[-3::]).uint)
        if BitArray(bin=line[-3::]).uint == 7:
            #print("huh???",print_flag( r[BitArray(bin=line[-3::]).uint]))
            r[BitArray(bin=line[-6:-3]).uint] =  BitArray(bin=str(int(print_flag( r[BitArray(bin=line[-3::]).uint]).replace(",","")))).uint
        else:
            r[BitArray(bin=line[-6:-3]).uint] = r[BitArray(bin=line[-3::]).uint] 
        r[7] = ["0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0"]
        pc_next = pc + 1

    elif instr == "00111": #div
        if int(line[-3::]) == 0:
            r[0] = "0"
            r[1] = "0"
            r[7][-4] = "1"
        else:
            r[0] = str(int([BitArray(bin=line[-6:-3]).uint]) // int(r[BitArray(bin=line[-3::]).uint]))
            r[1] = str(int(r[BitArray(bin=line[-6:-3]).uint]) % int(r[BitArray(bin=line[-3::]).uint]))
        r[7] = ["0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0"]
        pc_next = pc + 1
    
    elif instr == "01101": #not
        r[BitArray(bin=line[-6:-3]).uint] = str(~ int(r[BitArray(bin=line[-3::]).uint] ))
        r[7] = ["0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0"]
        pc_next = pc + 1
    
    elif instr == "01110": #cmp
        num1 = int(r[BitArray(bin=line[10:13]).uint])
        num2 = int(r[BitArray(bin=line[13::]).uint])
        if num1>num2:
            r[7][-2] = "1"
        elif num1 == num2:
            r[7][-1] = "1"
        else:
            r[7][-3] = "1"
        pc_next = pc + 1

    elif instr == "00100": #ld
        #print(line)
        #print("----->",line[-7::])
        #print(line[-10:-7])
        r[BitArray(bin=line[-10:-7]).uint] = str(decimal_to_binary(mem[BitArray(bin=line[-7::]).uint],16))
        #print("r: ",r)
        r[7] = ["0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0"]
        pc_next = pc + 1

    elif instr == "00101": #st
        mem[BitArray(bin=line[-7::]).uint] = int(r[BitArray(bin=line[-10:-7]).uint])
        r[7] = ["0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0"]
        pc_next = pc + 1

    elif instr == "01111": #jmp
        pc_next = BitArray(bin=line[-7::]).uint
        r[7] = ["0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0"]

    elif instr == "11100": #jlt
        if r[7][-3]=="1":
            pc_next = BitArray(bin=line[-7::]).uint
        else:
            pc_next = pc + 1
        r[7] = ["0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0"]
    
    elif instr == "11101": #jgt
        #print("chiptole",BitArray(bin=line[-7::]).uint)
        #print("mem:",mem)
        #print("needed ->",r[7][-2])
        if r[7][-2]=="1":
            pc_next = BitArray(bin=line[-7::]).uint
            #print("pc ------------->",pc)
        else:
            pc_next = pc + 1
        r[7] = ["0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0"]
        #sys.exit()

    elif instr == "11111": #je
        if r[7][-1]=="1":
            pc_next = BitArray(bin=line[-7::]).uint
        else:
            pc_next = pc + 1
        r[7] = ["0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0"]

    elif instr == "11010": #hlt
        hlt = 1
        r[7] = ["0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0"]
        #pc += 1
        return

if __name__ == "__main__":

    bin_input = []
    #file = open("input", "r")
    file_o = open("output","w")
    '''data = [line.strip() for line in file.readlines() if line.strip()]
    print(data)
    for line in data:
        bin_input.append(line)'''

    for line in sys.stdin:
        bin_input.append(line.strip())

    for i in range(len(bin_input)):
        mem[i] = bin_input[i]

    while (pc_next < len(bin_input) and hlt == 0):
        pc = pc_next
        #print(bin_input[pc])
        #print(pc,len(bin_input))
        operate(bin_input[pc])
        write=decimal_to_binary(pc,7)+" "*8+decimal_to_binary(r[0],16)+" "+decimal_to_binary(r[1],16)+" "+decimal_to_binary(r[2],16)+" "+decimal_to_binary(r[3],16)+" "+decimal_to_binary(r[4],16)+" "+decimal_to_binary(r[5],16)+" "+decimal_to_binary(r[6],16)+" "+print_flag(r[7]).replace(",","")
        file_o.write(write+"\n")
        

    for i in range(len(bin_input)):
        file_o.write(bin_input[i]+"\n")
    
    for i in range(len(bin_input),len(mem)):
        file_o.write(decimal_to_binary(mem[i],16)+"\n")

    file_o.close()

    file = open("output","r")
    data = file.read()
    sys.stdout.write(data)
    file.close()
    exit()
