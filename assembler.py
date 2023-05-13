
registers=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
mem_addr=0
flag = 0
pc=0
bin_piece=""
error=""

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
    instr=piece[0]
    if instr=="add":
        type = "A" 
        bin_piece = bin_piece + "00000" 
        registers[int(piece[1][-1])] = registers[int(piece[2][-1])] + registers[int(piece[3][-1])]
    elif instr=="sub":
        type = "A"
        bin_piece = bin_piece + "00001"  
        registers[int(piece[1][-1])] = registers[int(piece[2][-1])] - registers[int(piece[3][-1])]
    elif instr=="mul":
        type = "A"  
        bin_piece = bin_piece + "00110"
        registers[int(piece[1][-1])] = registers[int(piece[2][-1])] * registers[int(piece[3][-1])]
    elif instr=="mov":
        if piece[-1][0:2]=="reg":
            type = "C"  
            bin_piece = bin_piece + "00011"
            registers[int(piece[1][-1])] = registers[int(piece[2][-1])]
        elif piece[-1][0]=="$":
            type = "B"  
            bin_piece = bin_piece + "00010"
            registers[int(piece[1][-1])] = int(piece[2][1:])
    elif instr=="ld":
        type = "D"
        bin_piece = bin_piece + "00100"
        #add here
        #registers[int(piece[1][-1])] = 
    elif instr=="st":
        type = "D"
        bin_piece = bin_piece + "00101"
        #add here
        # = registers[int(piece[1][-1])] 
    elif instr=="div":
        type = "C" 
        bin_piece = bin_piece + "00111" 
        registers[int(piece[1][-1])] = registers[int(piece[2][-1])] / registers[int(piece[3][-1])]
    elif instr=="rs":
        type = "B"  
        bin_piece = bin_piece + "01000"
        registers[int(piece[1][-1])] = registers[int(piece[1][-1])] >> int(piece[2][-1])
    elif instr=="ls":
        type = "B"  
        bin_piece = bin_piece + "01001"
        registers[int(piece[1][-1])] = registers[int(piece[1][-1])] * (2 ** int(piece[2][-1]) )
    elif instr=="xor":
        type = "A"  
        bin_piece = bin_piece + "01010"
        registers[int(piece[1][-1])] = registers[int(piece[2][-1])] ^ registers[int(piece[3][-1])]
    elif instr=="or":
        type = "A"  
        bin_piece = bin_piece + "01011"
        registers[int(piece[1][-1])] = registers[int(piece[2][-1])] | registers[int(piece[3][-1])]
    elif instr=="and":
        type = "A"  
        bin_piece = bin_piece + "01100"
        registers[int(piece[1][-1])] = registers[int(piece[2][-1])] & registers[int(piece[3][-1])] 
    elif instr=="not":
        type = "C"  
        bin_piece = bin_piece + "01101"
        registers[int(piece[1][-1])] = ~ registers[int(piece[2][-1])]
    elif instr=="cmp":
        type = "C"  
        bin_piece = bin_piece + "01110"
        flag = 1 if registers[int(piece[1][-1])] > registers[int(piece[2][-1])] else 0
    elif instr=="jmp":
        type = "E"
        bin_piece = bin_piece + "01111"
        #add here
    elif instr=="jlt":
        type = "E"
        bin_piece = bin_piece + "11100"
        #add here
    elif instr=="jgt":
        type = "E"
        bin_piece = bin_piece + "11101"
        #add here
    elif instr=="je":
        type = "E"
        bin_piece = bin_piece + "11111"
        #add here
    elif instr=="hlt":
        type = "F"
        bin_piece = bin_piece + "11010"
        halt()
    else:
        type = "err"
        error = "wrong instruction type"
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
        #print(bin_piece)
        bin_piece = bin_piece + "0" + check_size(3,dec2binary(int(piece[1][-1]))) + check_size(7,dec2binary(int(piece[2][1:])))
        #print(bin_piece)
    elif type=="C":
        syn=[5,5,3,3]
        bin_piece = bin_piece + "00000" + check_size(3,dec2binary(int(piece[1][-1]))) + check_size(3,dec2binary(int(piece[2][-1])))
    elif type=="D":
        syn=[5,1,3,7]
        bin_piece = bin_piece + "0" + check_size(3,dec2binary(int(piece[1][-1]))) + check_size(7,dec2binary(int(piece[2][-1])))
    elif type=="E":
        syn=[5,4,7]
        bin_piece = bin_piece + "0000" + check_size(3,dec2binary(int(piece[1][-1]))) + check_size(7,dec2binary(int(mem_addr)))
    elif type=="F":
        syn=[5,11]
        bin_piece = bin_piece + "00000000000"
    return

#processes the input code and creates 
def assembler(input):
    type = instructions(piece)
    syntax_piece(type,piece)
    return


#read the data from input file
if __name__ == "__main__":
    file0 = open('input.txt', 'r')
    file1 = open('output', 'w')
    input = file0.readlines()
    for line in input:
        # piece is being referred to the single line of a code 
        piece = line.split()                   
    #send the read data to assembler to process
        assembler(input)
        file1.write(bin_piece+"\n")
        bin_piece=""
    else:
        if bin_piece == "1101000000000000":
            file1.close
            file0.close
            print("Completed Successfully")
        else:
            error = "Halt not encountered and end reached"
            print("error, ",error)
            file1.close
            file0.close
    exit