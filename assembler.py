import os
import re
import sys
registers=[0,0,0,0,0,0]
r=["R0","R1","R2","R3","R4","R5","R6","FLAGS"]
flag = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
bin_piece=""
error=""
assembly_code_lines=0
mem={}
mem_lab={}


#convert decimal to binary
def dec2binary(num):
        return int(bin(num).replace("0b",""))

#stop the execution process in assembler
def halt():
    return

#read the instruction type, perform the instruction and add the appropriate opcode to bin_piece
def instructions(piece):
    global bin_piece
    global registers
    global flag
    global error
    global t
    global g
    global k
    global p
    global q
    instr=piece[0]
    if instr[-1]==":":
        del piece[0]
    instr=piece[0]
    if instr=="add":
        type = "A" 
        bin_piece = bin_piece + "00000" 
        registers[int(piece[1][-1])] = registers[int(piece[2][-1])] + registers[int(piece[3][-1])]
        if  piece[1] in r:
            pass
        else:
            t=-1
    elif instr=="sub":
        type = "A"
        bin_piece = bin_piece + "00001"  
        registers[int(piece[1][-1])] = registers[int(piece[2][-1])] - registers[int(piece[3][-1])]
        if  piece[1] in r and piece[2] in r and piece[3] in r:
            pass
        else:
            t=-1
    elif instr=="mul":
        type = "A"  
        bin_piece = bin_piece + "00110"
        registers[int(piece[1][-1])] = registers[int(piece[2][-1])] * registers[int(piece[3][-1])]
        if  piece[1] in r and piece[2] in r and piece[3] in r:
            pass
        else:
            t=-1
    elif instr=="mov":
        if piece[-1][0]=="R":
            type = "C"  
            bin_piece = bin_piece + "00011"
            registers[int(piece[1][-1])] = registers[int(piece[2][-1])]
            if  piece[1] in r and piece[2] in r:
                pass
            else:
                t=-1
        elif piece[-1]=="FLAGS":
            type = "C"
            bin_piece = bin_piece + "00011"
            if  piece[1] in r and piece[2] in r:
                pass
            else:
                t=-1
        elif piece[-1][0]=="$":
            type = "B"  
            bin_piece = bin_piece + "00010"
            registers[int(piece[1][-1])] = int(piece[2][1:])
            if  piece[1] in r:
                pass
            else:
                t=-1
            if  int(piece[2][1:])>=127:
                g=-1
        else:
            p = -1
            type = "B"
    elif instr=="ld":
        type = "D"
        bin_piece = bin_piece + "00100"
        if piece[2] in list(mem.keys()):
            mem[piece[2]] = registers[int(piece[1][-1])]
        else:
            q = -1

    elif instr=="st":
        type = "D"
        bin_piece = bin_piece + "00101"
        if piece[2] in list(mem.keys()):
            mem[piece[2]] = registers[int(piece[1][-1])]
        else:
            q = -1
            
    elif instr=="div":
        type = "C" 
        bin_piece = bin_piece + "00111" 
        registers[int(piece[1][-1])] = registers[int(piece[2][-1])] / registers[int(piece[3][-1])]
        if  piece[1] in r and piece[2] in r:
            pass
        else:
            t=-1
    elif instr=="rs":
        type = "B"  
        bin_piece = bin_piece + "01000"
        registers[int(piece[1][-1])] = registers[int(piece[1][-1])] >> int(piece[2][-1])
        if  piece[1] in r:
            pass
        else:
            t=-1
        if int(piece[2][1:])>=127:
            g=-1
    elif instr=="ls":
        type = "B"  
        bin_piece = bin_piece + "01001"
        registers[int(piece[1][-1])] = registers[int(piece[1][-1])] * (2 ** int(piece[2][-1]) )
        if  piece[1] in r:
            pass
        else:
            t=-1
        if int(piece[2][1:])>=127:
            g=-1
    elif instr=="xor":
        type = "A"  
        bin_piece = bin_piece + "01010"
        registers[int(piece[1][-1])] = registers[int(piece[2][-1])] ^ registers[int(piece[3][-1])]
        if  piece[1] in r:
            pass
        else:
            t=-1
    elif instr=="or":
        type = "A"  
        bin_piece = bin_piece + "01011"
        registers[int(piece[1][-1])] = registers[int(piece[2][-1])] | registers[int(piece[3][-1])]
        if  piece[1] in r:
            pass
        else:
            t=-1
    elif instr=="and":
        type = "A"  
        bin_piece = bin_piece + "01100"
        registers[int(piece[1][-1])] = registers[int(piece[2][-1])] & registers[int(piece[3][-1])] 
        if  piece[1] in r:
            pass
        else:
            t=-1
    elif instr=="not":
        type = "C"  
        bin_piece = bin_piece + "01101"
        registers[int(piece[1][-1])] = ~ registers[int(piece[2][-1])]
        if  piece[1] in r and piece[2] in r:
            pass
        else:
            t=-1
    elif instr=="cmp":
        type = "C"  
        bin_piece = bin_piece + "01110"
        flag = 1 if registers[int(piece[1][-1])] > registers[int(piece[2][-1])] else 0
        if  piece[1] in r and piece[2] in r:
            pass
        elif len(piece)>3:
            k=-1
        else:
            t=-1
    elif instr=="jmp":
        type = "E"
        bin_piece = bin_piece + "01111"
    elif instr=="jlt":
        type = "E"
        bin_piece = bin_piece + "11100"
    elif instr=="jgt":
        type = "E"
        bin_piece = bin_piece + "11101"
    elif instr=="je":
        type = "E"
        bin_piece = bin_piece + "11111"
    elif instr=="hlt":
        type = "F"
        bin_piece = bin_piece + "11010"
        halt()
    elif instr=="var":
        mem[piece[1]] = 0
        type = "var"
        return
    else:
        type = "err"
        print("Error: ",piece)
    return type

def check_size(size,num):
    num=str(num)
    #print(size," ", num)
    if len(num)==size:
        return num
    else:
        num = "0" *(size - len(num))  + num
        return num

#creates the appropriate machine code based on the instr_type
def syntax_piece(type,piece):
    global bin_piece
    if type=="A":
        bin_piece = bin_piece + "00" + check_size(3,dec2binary(int(piece[1][-1]))) + check_size(3,dec2binary(int(piece[2][-1]))) + check_size(3,dec2binary(int(piece[3][-1])))
    elif type=="B":
        syn=[5,1,3,7]
        bin_piece = bin_piece + "0" + check_size(3,dec2binary(int(piece[1][-1]))) + check_size(7,dec2binary(int(piece[2][1:])))
    elif type=="C":
        syn=[5,5,3,3]
        if piece[2][0]=="R":
            bin_piece = bin_piece + "00000" + check_size(3,dec2binary(int(piece[1][-1]))) + check_size(3,dec2binary(int(piece[2][-1])))
        elif piece[2]=="FLAGS":
            bin_piece = bin_piece + "00000" + check_size(3,dec2binary(int(piece[1][-1]))) + "111"
    elif type=="D":
        syn=[5,1,3,7]
        if q == 0:
            bin_piece = bin_piece + "0" + check_size(3,dec2binary(int(piece[1][-1]))) + check_size(7,dec2binary(int(list(mem.keys()).index(piece[2]) + assembly_code_lines)))
        elif q == -1:
            return
    elif type=="E":
        syn=[5,4,7]
        bin_piece = bin_piece + "0000" +  check_size(7,dec2binary(int(mem_lab[piece[1]])))
    elif type=="F":
        syn=[5,11]
        bin_piece = bin_piece + "00000000000"
    return

#processes the input code and creates 
def assembler(input):
    type = instructions(piece)
    if type=="err":
        global z
        z=-1
        return
    elif type=="var":
        return
    syntax_piece(type,piece)
    return



if __name__ == "__main__":
    z = 0
    t = 0
    l = 0
    g = 0
    k = 0
    p = 0
    q = 0
    var_err = 0
    assembly_code_lines = 0
    mem_lab = {}
    #file0 = open('input.txt', 'r')
    file1 = open('output', 'w')

    input_lines = []
    for line in sys.stdin:
        input_lines.append(line.strip())

    for line in input_lines:
        piece = re.split(r'\s+|\t+', line.strip())
        if (piece[0] in ["add","sub","mov","ld","st","mul","div","rs","ls",
                         "xor","or","and","not","cmp","jmp","jlt","jgt","je","hlt"] or piece[0][-1] == ":"):
            assembly_code_lines += 1
        else:
            continue

        if piece[0][-1] == ":":
            mem_lab[piece[0][0:-1]] = assembly_code_lines - 1
        else:
            continue

    for line in input_lines:
        bin_piece = ""
        # piece is being referred to the single line of a code
        piece = re.split(r'\s+|\t+', line.strip())
        #send the read data to assembler to process
        try:
            assembler(piece)
        except:
            print("Invalid")
            break
        if z == -1:
            print("Wrong instruction")
            break
        if t == -1:
            print("Wrong register")
            break
        if k == -1:
            print("more than 2 values passed in cmp")
            break
        if g == -1:
            print("Imm value too high")
            break
        if p == -1:
            print("Wrong phrase used in mov")
            break
        if q == -1:
            print("Undefined variable used.")
            break
        if bin_piece == "1101000000000000":
            l = -1  
        if bin_piece=="":
            continue
        else:
            file1.write(bin_piece + "\n") 

    else:
        if bin_piece == "1101000000000000":
            file1.close()
            #file0.close()
            #print("Completed")
        else:
            if l == -1:
                error = "Halt not encountered at last but before"
                print(error)
            else:
                error = "Halt not encountered and end reached"
                print(error)
            file1.close()
            #file0.close()

    file = open("output","r")
    data = file.read()
    sys.stdout.write(data)
    exit()