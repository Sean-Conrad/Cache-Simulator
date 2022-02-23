
import math
from array import *  # this is to use all forms of array
f = open('test3Machine.txt')

class set0():
    valid = 0
    way0tag = 0
    way1tag = 0
    way0age = 0
    way1age = 0
class set1():
    valid = 0
    way0tag = 0
    way1tag = 0
    way0age = 0
    way1age = 0
class set2():
    valid = 0
    way0tag = 0
    way1tag = 0
    way0age = 0
    way1age = 0
class set3():
    valid = 0
    way0tag = 0
    way1tag = 0
    way0age = 0
    way1age = 0

class cacheInfo():
    missCount = 0
    hitCount = 0
    totalCount = 0
    mode = 0

def twos_comp(z, bits):
    if (z & (1 << (bits - 1))) != 0:  # if sign is neg
        z = z - (1 << bits)  # compute negative value
    return z

def addi(x, y, z):
    z = twos_comp(z, 16)
    w = registers[x] + z
    registers.pop(y)
    registers.insert(y, w)
    #print(registers)    HERE
def ori(x, y, z):
    z = twos_comp(z, 16)
    w = registers[x] + z
    registers.pop(y)
    registers.insert(y, w)

def branchtaken(z, pc):
    imm = hex(int(z, 2))
    imm = twos_comp(int(imm, 16), 16)
    pc = pc + 4 + (imm * 4)
    return pc

def storeword (x,y,z, userChoice, offset):

    z = twos_comp(z,16)
    t = registers[y]
    addr = registers[x] + z
    memory[hex(addr)] = t
    if cacheInfo.mode == 1:
        print('********************** STORE WORD: ********************** ')
        print('Hex Address:   ', hex(addr))
    hexAsBin = bin(int(hex(addr), 16))[2:].zfill(32)
    cacheSend(userChoice, hexAsBin, offset)

def loadword (x,y,z, userChoice, offset):  # rs,rt,imm

    z = twos_comp(z, 16)
    addr = registers[x] + z
    t = memory[hex(addr)]
    if cacheInfo.mode == 1:
        print('********************** LOAD WORD: ********************** ')
        print('Hex Address:   ', hex(addr))
    registers.pop(y)
    registers.insert(y, t)
    HexAsBin = bin(int(hex(addr), 16))[2:].zfill(32)
    cacheSend(userChoice, HexAsBin, offset)

def add(x, y, z):
    w = registers[z] + registers[y]
    registers.pop(x)
    registers.insert(x, w)

def sub(x, y, z): # rd, rs, rt
    w = registers[y] - registers[z]
    registers.pop(x)
    registers.insert(x, w)

def slt(x,y,z):  # rd, rs, rt
    if registers[y] < registers[z]:
        registers.pop(x)
        registers.insert(x, 1)
    else:
        registers.pop(x)
        registers.insert(x, 0)

def addu(x, y, z):
    w = registers[z] + registers[y]
    registers.pop(x)
    registers.insert(x, w)


def div(x,y):
    w = registers[x] / registers[y]
    w1 = int(w)
    registers.pop(31)
    registers.insert(31,w1)

    w = registers[x] % registers[y]
    registers.pop(32)
    registers.insert(32,w)

def mult(x,y,z):
    w = registers[y] * registers[z]
    registers.pop(x)
    registers.insert(x, w)


def mflo(rd):
    w = registers[31]
    registers.pop(rd)
    registers.insert(rd, w)


def mfhi(rd):
    w =  registers[32]
    registers.pop(rd)
    registers.insert(rd, w)

def cacheSend(config, memAddr, offsetSize):

    if (config == '1'):
        cacheConfig1(memAddr, offsetSize)
    elif (config == '2'):
        cacheConfig2(memAddr, offsetSize)
    elif (config == '3'):
        cacheConfig3(memAddr, offsetSize)
    elif (config == '4'):
        cacheConfig4(memAddr, offsetSize)

def cacheConfig1(memAddr, offsetSize):
    blockEnd = 32 - offsetSize
    setEnd = 30 - offsetSize
    binToDec = hex(int(str(memAddr), 2))
    cacheInfo.totalCount+= 1
    if cacheInfo.mode == '1':
        print('In Binary:     ', memAddr[0:32])
        print('Block#:        ', memAddr[0: int(blockEnd)])
        print('Current SetID: ', memAddr[int(setEnd): int(blockEnd)])
        print('Current Tag:   ', memAddr[0: int(setEnd)])
        print('Comparing to...')
        print('Count:  ',cacheInfo.totalCount)

    if cacheInfo.mode == '1':
        print('Current Address:', binToDec)

    if (set1.valid == 0):


        cacheInfo.missCount+= 1
        set1.valid = 1
        set1.way0tag = memAddr[0: int(blockEnd)]


        if cacheInfo.mode == '1':
            print('Cache miss!\n\n')
            print('New Tag: ', set1.way0tag)
        return

    if (set1.way0tag == memAddr[0 : int(blockEnd)]):
        cacheInfo.hitCount+= 1
        if cacheInfo.mode == '1':
            print('Cache hit!\n\n')
    else:
        cacheInfo.missCount+= 1
        set1.way0tag = memAddr[0: int(blockEnd)]


        if cacheInfo.mode == '1':
            print('Cache miss!\n\n')



def cacheConfig2(memAddr, offsetSize):
    blockEnd = 32 - offsetSize
    setEnd = 30 - offsetSize
    cacheInfo.totalCount+= 1

    if cacheInfo.mode == '1':
        print('In Binary:     ', memAddr[0:32])
        print('Block#:        ', memAddr[0: int(blockEnd)])
        print('Current SetID: ', memAddr[int(setEnd): int(blockEnd)])
        print('Current Tag:   ', memAddr[0: int(setEnd)])
        print('Count:  ',cacheInfo.totalCount)



    if memAddr[int(setEnd) + 2 : int(blockEnd) + 2] == '00':
        if (set0.valid == 0):

            cacheInfo.missCount+= 1
            set0.valid = 1
            set0.way0tag = memAddr[0: int(setEnd)]
            if cacheInfo.mode == '1':
                print('Cache miss!\n\n')
                print('Tag Updated ')
            return
        if (set1.way0tag == memAddr[0 : int(setEnd)]):

            cacheInfo.hitCount+= 1
            if cacheInfo.mode == '1':
                print('Cache hit!\n\n')
        else:

            cacheInfo.missCount+= 1
            set0.way0tag = memAddr[0: int(setEnd)]
            if cacheInfo.mode == '1':
                print('Cache miss!\n\n')
                print('Tag Updated ')
    elif memAddr[int(setEnd) + 2: int(blockEnd) + 2] == '01':
        if (set1.valid == 0):

            cacheInfo.missCount+= 1
            set1.valid = 1
            set1.way0tag = memAddr[0: int(setEnd)]
            if cacheInfo.mode == '1':
                print('Cache miss!\n\n')
                print('Tag Updated ')
            return
        if (set1.way0tag == memAddr[0 : int(setEnd)]):

            cacheInfo.hitCount+= 1
            if cacheInfo.mode == '1':
                print('Cache hit!\n\n')

        else:

            cacheInfo.missCount+= 1
            set1.way0tag = memAddr[0: int(setEnd)]
            if cacheInfo.mode == '1':
                print('Cache miss!\n\n')
                print('Tag Updated ')
    elif memAddr[int(setEnd) + 2 : int(blockEnd) + 2] == '10':
        if (set2.valid == 0):

            cacheInfo.missCount+= 1
            set2.valid = 1
            set2.way0tag = memAddr[0: int(setEnd)]
            if cacheInfo.mode == '1':
                print('Cache miss!\n\n')
                print('Tag Updated ')
            return

        if (set2.way0tag == memAddr[0 : int(setEnd)]):

            cacheInfo.hitCount+= 1
            if cacheInfo.mode == '1':
                print('Cache hit!\n\n')
        else:

            cacheInfo.missCount+= 1
            set2.way0tag = memAddr[0: int(setEnd)]
            if cacheInfo.mode == '1':
                print('Cache miss!\n\n')
                print('Tag Updated ')
    elif memAddr[int(setEnd) + 2: int(blockEnd) + 2] == '11':
        if (set3.valid == 0):

            cacheInfo.missCount+= 1
            set3.valid = 1
            set3.way0tag = memAddr[0: int(setEnd)]
            if cacheInfo.mode == '1':
                print('Cache miss!\n\n')
                print('Tag Updated ')
            return
        if (set3.way0tag == memAddr[0 : int(setEnd)]):

            cacheInfo.hitCount+= 1
            if cacheInfo.mode == '1':
                print('Cache hit!\n\n')
        else:

            cacheInfo.missCount+= 1
            set3.way0tag = memAddr[0: int(setEnd)]
            if cacheInfo.mode == '1':
                print('Cache miss!\n\n')
                print('Tag Updated ')



def cacheConfig3(memAddr, offsetSize):    # 2 way, 4 set, 64   OFFSET is 6 SetID is bit 26:27
    blockEnd = 32 - offsetSize
    setEnd = 30 - offsetSize
    cacheInfo.totalCount+= 1

    if cacheInfo.mode == '1':
        print('In Binary:     ', memAddr[0:32])
        print('Block#:        ', memAddr[0: int(blockEnd)])
        print('Current SetID: ', memAddr[int(setEnd): int(blockEnd)])
        print('Current Tag:   ', hex(int((memAddr[0: int(setEnd)]), 2)))
        print('Count:  ', cacheInfo.totalCount)

    set0.way0age += 1
    set0.way1age += 1
    set1.way0age += 1
    set1.way1age += 1
    set2.way0age += 1
    set2.way1age += 1
    set3.way0age += 1
    set3.way1age += 1



    if memAddr[int(setEnd): int(blockEnd)] == '00':
        if (set0.valid == 0):

            cacheInfo.missCount+= 1
            set0.valid = 1
            set0.way0tag = memAddr[0: int(setEnd)]
            if cacheInfo.mode == '1':
                print('Cache miss!\n\n')
                print('Tag Updated ')
            return
        if (set0.way0tag == memAddr[0 : int(setEnd)]):

            cacheInfo.hitCount+= 1
            if cacheInfo.mode == '1':
                print('Cache hit!\n\n')
        else:

            cacheInfo.missCount+= 1
            set0.way0tag = memAddr[0: int(setEnd)]
            if cacheInfo.mode == '1':
                print('Cache miss!\n\n')
                print('Tag Updated ')



    elif memAddr[int(setEnd): int(blockEnd)] == '01':
        if (set1.valid == 0):

            cacheInfo.missCount+= 1
            set1.valid = 1
            set1.way0tag = memAddr[0: int(setEnd)]
            if cacheInfo.mode == '1':
                print('Cache miss!\n\n')
                print('Tag Updated ')
            return
        if (set1.way0tag == memAddr[0 : int(setEnd)]):

            cacheInfo.hitCount+= 1
            if cacheInfo.mode == '1':
                print('Cache hit!\n\n')
        else:

            cacheInfo.missCount+= 1
            set1.way0tag = memAddr[0: int(setEnd)]
            if cacheInfo.mode == '1':
                print('Cache miss!\n\n')
                print('Tag Updated ')

    elif memAddr[int(setEnd): int(blockEnd)] == '10':
        if (set2.valid == 0):

            cacheInfo.missCount+= 1
            set2.valid = 1
            set2.way0tag = memAddr[0: int(setEnd)]
            if cacheInfo.mode == '1':
                print('Cache miss!\n\n')
                print('Tag Updated ')
            return

        if (set2.way0tag == memAddr[0 : int(setEnd)]):

            cacheInfo.hitCount+= 1
            if cacheInfo.mode == '1':
                print('Cache hit!\n\n')
        else:

            cacheInfo.missCount+= 1
            set2.way0tag = memAddr[0: int(setEnd)]
            if cacheInfo.mode == '1':
                print('Cache miss!\n\n')
                print('Tag Updated ')

    elif memAddr[int(setEnd): int(blockEnd)] == '11':
        if (set3.valid == 0):

            cacheInfo.missCount+= 1
            set3.valid = 1
            set3.way0tag = memAddr[0: int(setEnd)]
            if cacheInfo.mode == '1':
                print('Cache miss!\n\n')
                print('Tag Updated ')
            return
        if (set3.way0tag == memAddr[0 : int(setEnd)]):

            cacheInfo.hitCount+= 1
            if cacheInfo.mode == '1':
                print('Cache hit!\n\n')
        else:

            cacheInfo.missCount+= 1
            set3.way0tag = memAddr[0: int(setEnd)]
            if cacheInfo.mode == '1':
                print('Cache miss!\n\n')
                print('Tag Updated ')





def cacheConfig4(memAddr, offsetSize):
    blockEnd = 32 - offsetSize
    setEnd = 30 - offsetSize
    cacheInfo.totalCount+= 1
    if cacheInfo.mode == '1':
        print('In Binary:     ', memAddr[0:32])
        print('Block#:        ', memAddr[0: int(blockEnd)])
        print('Current SetID: ', memAddr[int(setEnd): int(blockEnd)])
        print('Current Tag:   ', hex(int((memAddr[0: int(setEnd)]), 2)))
        print('Count:  ', cacheInfo.totalCount)

    set0.way0age += 1
    set0.way1age += 1
    set1.way0age += 1
    set1.way1age += 1
    set2.way0age += 1
    set2.way1age += 1
    set3.way0age += 1
    set3.way1age += 1



    if memAddr[int(setEnd): int(blockEnd)] == '00':
        if (set0.valid == 0):

            cacheInfo.missCount+= 1
            set0.valid = 1
            set0.way0tag = memAddr[0: int(setEnd)]
            if cacheInfo.mode == '1':
                print('Cache miss!\n\n')
                print('Tag Updated ')
            return
        if (set0.way0tag == memAddr[0 : int(setEnd)]):

            cacheInfo.hitCount+= 1
            if cacheInfo.mode == '1':
                print('Cache hit!\n\n')
        else:

            cacheInfo.missCount+= 1
            set0.way0tag = memAddr[0: int(setEnd)]
            if cacheInfo.mode == '1':
                print('Cache miss!\n\n')
                print('Tag Updated ')



    elif memAddr[int(setEnd): int(blockEnd)] == '01':
        if (set1.valid == 0):

            cacheInfo.missCount+= 1
            set1.valid = 1
            set1.way0tag = memAddr[0: int(setEnd)]
            if cacheInfo.mode == '1':
                print('Cache miss!\n\n')
                print('Tag Updated ')
            return
        if (set1.way0tag == memAddr[0 : int(setEnd)]):

            cacheInfo.hitCount+= 1
            if cacheInfo.mode == '1':
                print('Cache hit!\n\n')
        else:

            cacheInfo.missCount+= 1
            set1.way0tag = memAddr[0: int(setEnd)]
            if cacheInfo.mode == '1':
                print('Cache miss!\n\n')
                print('Tag Updated ')

    elif memAddr[int(setEnd): int(blockEnd)] == '10':
        if (set2.valid == 0):

            cacheInfo.missCount+= 1
            set2.valid = 1
            set2.way0tag = memAddr[0: int(setEnd)]
            if cacheInfo.mode == '1':
                print('Cache miss!\n\n')
                print('Tag Updated ')
            return

        if (set2.way0tag == memAddr[0 : int(setEnd)]):

            cacheInfo.hitCount+= 1
            if cacheInfo.mode == '1':
                print('Cache hit!\n\n')
        else:

            cacheInfo.missCount+= 1
            set2.way0tag = memAddr[0: int(setEnd)]
            if cacheInfo.mode == '1':
                print('Cache miss!\n\n')
                print('Tag Updated ')

    elif memAddr[int(setEnd): int(blockEnd)] == '11':
        if (set3.valid == 0):

            cacheInfo.missCount+= 1
            set3.valid = 1
            set3.way0tag = memAddr[0: int(setEnd)]
            if cacheInfo.mode == '1':
                print('Cache miss!\n\n')
                print('Tag Updated ')
            return
        if (set3.way0tag == memAddr[0 : int(setEnd)]):
            cacheInfo.hitCount+= 1
            if cacheInfo.mode == '1':
                print('Cache hit!\n\n')
        else:
            cacheInfo.missCount+= 1
            set3.way0tag = memAddr[0: int(setEnd)]
            if cacheInfo.mode == '1':
                print('Cache miss!\n\n')
                print('Tag Updated ')



# Creates array of registers
n = 33
registers = array('i', [])
for i in range(n):
    x = 0
    registers.append(x)

# Creates dictionary of memory spaces and fill with zeros
memory = {'0x2000' : 0}
curAddress = '0x2000'
count = 0
n = 1024
while count != n:
    hexAsInt = int(curAddress, 16)
    hexAsInt = hexAsInt + 4
    curAddress = hex(hexAsInt)
    memory[curAddress] = 0
    count = count + 1

# DONE: create pc dictionary and populate with binary machine code
pc = 0
PC = {pc: 0}

for line in f:
    # convert line from hex to binary and read into dictionary
    line1 = format(int(line, 16), "032b")
    PC[pc] = line1
    pc = pc + 4

pcmax = pc                                      # used in main loop.
pc = 0

# MAIN LOOP
# NEED: Condition statements for remaining functions (mult,div)

print('Please select a cache configuration\n Enter...')
print('1: 1 way, 1 set, 32 bytes')
print('2: 1 way, 4 sets, 128 bytes')
print('3: 2 way, 4 sets, 64 bytes')
print('4: 4 way, 1 set, 64 bytes')
userChoice = input()
print(userChoice)
print('Choose a mode')
print('1: Detailed Display Mode')
print('2: Fast Mode\n\n')
cacheInfo.mode = input()
print(cacheInfo.mode)

if (userChoice == '1'):
    userWay = 1
    userSet = 1
    userBytes = 32
elif (userChoice == '2'):
    userWay = 1
    userSet = 4
    userBytes = 128
elif (userChoice == '3'):
    userWay = 2
    userSet = 4
    userBytes = 64
elif (userChoice == '4'):
    userWay = 4
    userSet = 1
    userBytes = 64
offset = math.log(userBytes, 2)

# Identifies instruction using opcode then calls function
while pc in range(pcmax):
    #b = 15
    instruction = PC[int(pc)]
    h = instruction[0:6]
    x = instruction[6:11]
    y = instruction[11:16]
    z = instruction[16:32]
    a = instruction[26:32]

    if (h == "000000" and a == "100000"):               # add
        #rd is going to register destination
        rd = int(instruction[16:21], 2)
        rs = int(instruction[6:11], 2)
        rt = int(instruction[11:16], 2)
        add(rd,rs,rt)
        pc = pc + 4
    elif (h == "000000" and a == "100010"):             # sub
        #rd is going to register destination
        rd = int(instruction[16:21], 2)
        rs = int(instruction[6:11], 2)
        rt = int(instruction[11:16], 2)
        sub(rd,rs,rt)
        pc = pc + 4
    elif (h == "000000" and a == "101010"):             # slt
        rd = int(instruction[16:21], 2)
        rs = int(instruction[6:11], 2)
        rt = int(instruction[11:16], 2)
        slt(rd,rs,rt)
        pc = pc + 4
    elif(h == "000000" and a == "011010"):              # div
        rs = int(instruction[6:11], 2)
        rt = int(instruction[11:16], 2)
        div(rs,rt)
        pc = pc + 4
    elif(h == "011100"):                                # mult
        r2 = int(instruction[6:11], 2)
        r1 = int(instruction[16:21], 2)
        r3 = int(instruction[11:16], 2)
        mult(r1,r2,r3)
        pc = pc + 4
    elif (h == "000000" and a == "010010"):             # mflo
        rd = int(instruction[16:21], 2)
        mflo(rd)
        pc = pc + 4
    elif (h == "000000" and a == "010000"):             # mfhi
        rd = int(instruction[16:21], 2)
        mfhi(rd)
        pc = pc + 4
    elif (h == "001000"):                               # addi
        r1 = int(x, 2)
        r2 = int(y, 2)
        imm = int(z, 2)
        ori(r1, r2, imm)
        pc = pc + 4
    elif (h == "000000" and a == "100001"):             # addu
        rd = int(instruction[16:21], 2)
        rs = int(instruction[6:11], 2)
        rt = int(instruction[11:16], 2)
        add(rd,rs,rt)
        pc = pc + 4
    elif (h == "001101"):                               # ori
        r1 = int(x, 2)
        r2 = int(y, 2)
        imm = int(z, 2)
        addi(r1, r2, imm)
        pc = pc + 4
    elif (h == "000100"):                               # beq
        r1 = int(x, 2)
        r2 = int(y, 2)
        if registers[r1] == registers[r2]:
            pc = branchtaken(z, pc)
        else:
            pc = pc + 4
    elif (h == "000101"):                               # bne
        r1 = int(x, 2)
        r2 = int(y, 2)
        if registers[r1] != registers[r2]:
            pc = branchtaken(z, pc)
        else:
            pc = pc + 4
    elif (h == "000001"):                               # bltz
        r1 = int(x, 2)
        if registers[r1] < 0:
            pc = branchtaken(z, pc)
        else:
            pc = pc + 4
    elif (h == "101011"):                               # sw
        r1 = int(x, 2)
        r2 = int(y, 2)
        imm = int(z, 2)
        storeword(r1, r2, imm, userChoice, offset)
        pc = pc + 4
    elif (h == "100011"):                               # lw
        r1 = int(x,2)  #rs
        r2 = int(y,2)  #rt
        imm = int(z, 2)
        loadword(r1,r2, imm, userChoice, offset)
        pc = pc + 4
    elif (h == "100000"):                               # lb
        r1 = int(x,2)
        r2 = int(y,2)
        imm = int(z, 2)
        loadword(r1,r2, imm)
        pc = pc + 4
    elif (h == "101000"):                               # sb
        r1 = int(x, 2)
        r2 = int(y, 2)
        imm = int(z, 2)
        storeword(r1, r2, imm)
        pc = pc + 4

print('\n\n********************** Simulation complete. **********************\nResults:')
print('Total Count:  ',cacheInfo.totalCount)
print('Hit Count:    ', cacheInfo.hitCount)
print('Miss Count:   ', cacheInfo.missCount)
print('Hit Rate:     ', (cacheInfo.hitCount / (cacheInfo.hitCount + cacheInfo.missCount)) * 100, '%')

