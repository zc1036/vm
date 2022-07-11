
import sys
import struct
from sys import stdout
import hexdump

OP_ADD            = 1
OP_SUB            = 2
OP_DIV            = 3
OP_MUL            = 4
OP_BIT_AND        = 5
OP_BIT_OR         = 6
OP_FADD           = 7
OP_FSUB           = 8
OP_FDIV           = 9
OP_FMUL           = 0xA
OP_LOAD_BYTE      = 0xB
OP_LOAD_2BYTE     = 0xC
OP_LOAD_4BYTE     = 0xD
OP_LOAD_WORD      = 0xE
OP_LOAD_SLIMM     = 0xF
OP_LOAD_ULIMM     = 0x10
OP_OR_UUIMM       = 0x11
OP_STORE_BYTE     = 0x12
OP_STORE_2BYTE    = 0x13
OP_STORE_4BYTE    = 0x14
OP_STORE_WORD     = 0x15
OP_REGCALL        = 0x16
OP_RELCALL        = 0x17
OP_RELJUMP_IF0    = 0x19
OP_RELJUMP_IFLT0  = 0x1A
OP_RELJUMP_IFGT0  = 0x1B
OP_RELJUMP_IFLTE0 = 0x1C
OP_RELJUMP_IFGTE0 = 0x1D
OP_SYSCALL        = 0x1F

(r0, r1, r2, r3, r4, r5, r6, r7, r8, r9, r10, r11, r12, r13, r14, r15, r16, r17, r18, r19, r20, r21, r22, r23,
r24, r25, r26, r27, r28, r29, r30, r31, r32, r33, r34, r35, r36, r37, r38, r39, r40, r41, r42, r43, r44, r45,
r46, r47, r48, r49, r50, r51, r52, r53, r54, r55, r56, r57, r58, r59, r60, r61, r62, r63, r64, r65, r66, r67,
r68, r69, r70, r71, r72, r73, r74, r75, r76, r77, r78, r79, r80, r81, r82, r83, r84, r85, r86, r87, r88, r89,
r90, r91, r92, r93, r94, r95, r96, r97, r98, r99, r100, r101, r102, r103, r104, r105, r106, r107, r108, r109,
r110, r111, r112, r113, r114, r115, r116, r117, r118, r119, r120, r121, r122, r123, r124, r125, r126, r127,
r128, r129, r130, r131, r132, r133, r134, r135, r136, r137, r138, r139, r140, r141, r142, r143, r144, r145,
r146, r147, r148, r149, r150, r151, r152, r153, r154, r155, r156, r157, r158, r159, r160, r161, r162, r163,
r164, r165, r166, r167, r168, r169, r170, r171, r172, r173, r174, r175, r176, r177, r178, r179, r180, r181,
r182, r183, r184, r185, r186, r187, r188, r189, r190, r191, r192, r193, r194, r195, r196, r197, r198, r199,
r200, r201, r202, r203, r204, r205, r206, r207, r208, r209, r210, r211, r212, r213, r214, r215, r216, r217,
r218, r219, r220, r221, r222, r223, r224, r225, r226, r227, r228, r229, r230, r231, r232, r233, r234, r235,
r236, r237, r238, r239, r240, r241, r242, r243, r244, r245, r246, r247, r248, r249, r250, r251, r252, r253,
r254, r255) = (
    ("reg", 0), ("reg", 1), ("reg", 2), ("reg", 3), ("reg", 4), ("reg", 5), ("reg", 6), ("reg", 7), ("reg", 8),
    ("reg", 9), ("reg", 10), ("reg", 11), ("reg", 12), ("reg", 13), ("reg", 14), ("reg", 15), ("reg", 16),
    ("reg", 17), ("reg", 18), ("reg", 19), ("reg", 20), ("reg", 21), ("reg", 22), ("reg", 23), ("reg", 24),
    ("reg", 25), ("reg", 26), ("reg", 27), ("reg", 28), ("reg", 29), ("reg", 30), ("reg", 31), ("reg", 32),
    ("reg", 33), ("reg", 34), ("reg", 35), ("reg", 36), ("reg", 37), ("reg", 38), ("reg", 39), ("reg", 40),
    ("reg", 41), ("reg", 42), ("reg", 43), ("reg", 44), ("reg", 45), ("reg", 46), ("reg", 47), ("reg", 48),
    ("reg", 49), ("reg", 50), ("reg", 51), ("reg", 52), ("reg", 53), ("reg", 54), ("reg", 55), ("reg", 56),
    ("reg", 57), ("reg", 58), ("reg", 59), ("reg", 60), ("reg", 61), ("reg", 62), ("reg", 63), ("reg", 64),
    ("reg", 65), ("reg", 66), ("reg", 67), ("reg", 68), ("reg", 69), ("reg", 70), ("reg", 71), ("reg", 72),
    ("reg", 73), ("reg", 74), ("reg", 75), ("reg", 76), ("reg", 77), ("reg", 78), ("reg", 79), ("reg", 80),
    ("reg", 81), ("reg", 82), ("reg", 83), ("reg", 84), ("reg", 85), ("reg", 86), ("reg", 87), ("reg", 88),
    ("reg", 89), ("reg", 90), ("reg", 91), ("reg", 92), ("reg", 93), ("reg", 94), ("reg", 95), ("reg", 96),
    ("reg", 97), ("reg", 98), ("reg", 99), ("reg", 100), ("reg", 101), ("reg", 102), ("reg", 103), ("reg", 104), 
    ("reg", 105), ("reg", 106), ("reg", 107), ("reg", 108), ("reg", 109), ("reg", 110), ("reg", 111), ("reg", 112), 
    ("reg", 113), ("reg", 114), ("reg", 115), ("reg", 116), ("reg", 117), ("reg", 118), ("reg", 119), ("reg", 120),
    ("reg", 121), ("reg", 122), ("reg", 123), ("reg", 124), ("reg", 125), ("reg", 126), ("reg", 127), ("reg", 128),
    ("reg", 129), ("reg", 130), ("reg", 131), ("reg", 132), ("reg", 133), ("reg", 134), ("reg", 135), ("reg", 136),
    ("reg", 137), ("reg", 138), ("reg", 139), ("reg", 140), ("reg", 141), ("reg", 142), ("reg", 143), ("reg", 144),
    ("reg", 145), ("reg", 146), ("reg", 147), ("reg", 148), ("reg", 149), ("reg", 150), ("reg", 151), ("reg", 152),
    ("reg", 153), ("reg", 154), ("reg", 155), ("reg", 156), ("reg", 157), ("reg", 158), ("reg", 159), ("reg", 160),
    ("reg", 161), ("reg", 162), ("reg", 163), ("reg", 164), ("reg", 165), ("reg", 166), ("reg", 167), ("reg", 168),
    ("reg", 169), ("reg", 170), ("reg", 171), ("reg", 172), ("reg", 173), ("reg", 174), ("reg", 175), ("reg", 176),
    ("reg", 177), ("reg", 178), ("reg", 179), ("reg", 180), ("reg", 181), ("reg", 182), ("reg", 183), ("reg", 184),
    ("reg", 185), ("reg", 186), ("reg", 187), ("reg", 188), ("reg", 189), ("reg", 190), ("reg", 191), ("reg", 192),
    ("reg", 193), ("reg", 194), ("reg", 195), ("reg", 196), ("reg", 197), ("reg", 198), ("reg", 199), ("reg", 200),
    ("reg", 201), ("reg", 202), ("reg", 203), ("reg", 204), ("reg", 205), ("reg", 206), ("reg", 207), ("reg", 208),
    ("reg", 209), ("reg", 210), ("reg", 211), ("reg", 212), ("reg", 213), ("reg", 214), ("reg", 215), ("reg", 216),
    ("reg", 217), ("reg", 218), ("reg", 219), ("reg", 220), ("reg", 221), ("reg", 222), ("reg", 223), ("reg", 224),
    ("reg", 225), ("reg", 226), ("reg", 227), ("reg", 228), ("reg", 229), ("reg", 230), ("reg", 231), ("reg", 232),
    ("reg", 233), ("reg", 234), ("reg", 235), ("reg", 236), ("reg", 237), ("reg", 238), ("reg", 239), ("reg", 240),
    ("reg", 241), ("reg", 242), ("reg", 243), ("reg", 244), ("reg", 245), ("reg", 246), ("reg", 247), ("reg", 248),
    ("reg", 249), ("reg", 250), ("reg", 251), ("reg", 252), ("reg", 253), ("reg", 254), ("reg", 255)
)

rip = r0
rlr = r1
rsp = r2

(fr0, fr1, fr2, fr3, fr4, fr5, fr6, fr7, fr8, fr9, fr10, fr11, fr12, fr13, fr14, fr15, fr16, fr17, fr18, fr19, fr20, fr21, fr22, fr23,
fr24, fr25, fr26, fr27, fr28, fr29, fr30, fr31, fr32, fr33, fr34, fr35, fr36, fr37, fr38, fr39, fr40, fr41, fr42, fr43, fr44, fr45,
fr46, fr47, fr48, fr49, fr50, fr51, fr52, fr53, fr54, fr55, fr56, fr57, fr58, fr59, fr60, fr61, fr62, fr63, fr64, fr65, fr66, fr67,
fr68, fr69, fr70, fr71, fr72, fr73, fr74, fr75, fr76, fr77, fr78, fr79, fr80, fr81, fr82, fr83, fr84, fr85, fr86, fr87, fr88, fr89,
fr90, fr91, fr92, fr93, fr94, fr95, fr96, fr97, fr98, fr99, fr100, fr101, fr102, fr103, fr104, fr105, fr106, fr107, fr108, fr109,
fr110, fr111, fr112, fr113, fr114, fr115, fr116, fr117, fr118, fr119, fr120, fr121, fr122, fr123, fr124, fr125, fr126, fr127,
fr128, fr129, fr130, fr131, fr132, fr133, fr134, fr135, fr136, fr137, fr138, fr139, fr140, fr141, fr142, fr143, fr144, fr145,
fr146, fr147, fr148, fr149, fr150, fr151, fr152, fr153, fr154, fr155, fr156, fr157, fr158, fr159, fr160, fr161, fr162, fr163,
fr164, fr165, fr166, fr167, fr168, fr169, fr170, fr171, fr172, fr173, fr174, fr175, fr176, fr177, fr178, fr179, fr180, fr181,
fr182, fr183, fr184, fr185, fr186, fr187, fr188, fr189, fr190, fr191, fr192, fr193, fr194, fr195, fr196, fr197, fr198, fr199,
fr200, fr201, fr202, fr203, fr204, fr205, fr206, fr207, fr208, fr209, fr210, fr211, fr212, fr213, fr214, fr215, fr216, fr217,
fr218, fr219, fr220, fr221, fr222, fr223, fr224, fr225, fr226, fr227, fr228, fr229, fr230, fr231, fr232, fr233, fr234, fr235,
fr236, fr237, fr238, fr239, fr240, fr241, fr242, fr243, fr244, fr245, fr246, fr247, fr248, fr249, fr250, fr251, fr252, fr253,
fr254, fr255) = (
    ("freg", 0), ("freg", 1), ("freg", 2), ("freg", 3), ("freg", 4), ("freg", 5), ("freg", 6), ("freg", 7), ("freg", 8),
    ("freg", 9), ("freg", 10), ("freg", 11), ("freg", 12), ("freg", 13), ("freg", 14), ("freg", 15), ("freg", 16),
    ("freg", 17), ("freg", 18), ("freg", 19), ("freg", 20), ("freg", 21), ("freg", 22), ("freg", 23), ("freg", 24),
    ("freg", 25), ("freg", 26), ("freg", 27), ("freg", 28), ("freg", 29), ("freg", 30), ("freg", 31), ("freg", 32),
    ("freg", 33), ("freg", 34), ("freg", 35), ("freg", 36), ("freg", 37), ("freg", 38), ("freg", 39), ("freg", 40),
    ("freg", 41), ("freg", 42), ("freg", 43), ("freg", 44), ("freg", 45), ("freg", 46), ("freg", 47), ("freg", 48),
    ("freg", 49), ("freg", 50), ("freg", 51), ("freg", 52), ("freg", 53), ("freg", 54), ("freg", 55), ("freg", 56),
    ("freg", 57), ("freg", 58), ("freg", 59), ("freg", 60), ("freg", 61), ("freg", 62), ("freg", 63), ("freg", 64),
    ("freg", 65), ("freg", 66), ("freg", 67), ("freg", 68), ("freg", 69), ("freg", 70), ("freg", 71), ("freg", 72),
    ("freg", 73), ("freg", 74), ("freg", 75), ("freg", 76), ("freg", 77), ("freg", 78), ("freg", 79), ("freg", 80),
    ("freg", 81), ("freg", 82), ("freg", 83), ("freg", 84), ("freg", 85), ("freg", 86), ("freg", 87), ("freg", 88),
    ("freg", 89), ("freg", 90), ("freg", 91), ("freg", 92), ("freg", 93), ("freg", 94), ("freg", 95), ("freg", 96),
    ("freg", 97), ("freg", 98), ("freg", 99), ("freg", 100), ("freg", 101), ("freg", 102), ("freg", 103), ("freg", 104), 
    ("freg", 105), ("freg", 106), ("freg", 107), ("freg", 108), ("freg", 109), ("freg", 110), ("freg", 111), ("freg", 112), 
    ("freg", 113), ("freg", 114), ("freg", 115), ("freg", 116), ("freg", 117), ("freg", 118), ("freg", 119), ("freg", 120),
    ("freg", 121), ("freg", 122), ("freg", 123), ("freg", 124), ("freg", 125), ("freg", 126), ("freg", 127), ("freg", 128),
    ("freg", 129), ("freg", 130), ("freg", 131), ("freg", 132), ("freg", 133), ("freg", 134), ("freg", 135), ("freg", 136),
    ("freg", 137), ("freg", 138), ("freg", 139), ("freg", 140), ("freg", 141), ("freg", 142), ("freg", 143), ("freg", 144),
    ("freg", 145), ("freg", 146), ("freg", 147), ("freg", 148), ("freg", 149), ("freg", 150), ("freg", 151), ("freg", 152),
    ("freg", 153), ("freg", 154), ("freg", 155), ("freg", 156), ("freg", 157), ("freg", 158), ("freg", 159), ("freg", 160),
    ("freg", 161), ("freg", 162), ("freg", 163), ("freg", 164), ("freg", 165), ("freg", 166), ("freg", 167), ("freg", 168),
    ("freg", 169), ("freg", 170), ("freg", 171), ("freg", 172), ("freg", 173), ("freg", 174), ("freg", 175), ("freg", 176),
    ("freg", 177), ("freg", 178), ("freg", 179), ("freg", 180), ("freg", 181), ("freg", 182), ("freg", 183), ("freg", 184),
    ("freg", 185), ("freg", 186), ("freg", 187), ("freg", 188), ("freg", 189), ("freg", 190), ("freg", 191), ("freg", 192),
    ("freg", 193), ("freg", 194), ("freg", 195), ("freg", 196), ("freg", 197), ("freg", 198), ("freg", 199), ("freg", 200),
    ("freg", 201), ("freg", 202), ("freg", 203), ("freg", 204), ("freg", 205), ("freg", 206), ("freg", 207), ("freg", 208),
    ("freg", 209), ("freg", 210), ("freg", 211), ("freg", 212), ("freg", 213), ("freg", 214), ("freg", 215), ("freg", 216),
    ("freg", 217), ("freg", 218), ("freg", 219), ("freg", 220), ("freg", 221), ("freg", 222), ("freg", 223), ("freg", 224),
    ("freg", 225), ("freg", 226), ("freg", 227), ("freg", 228), ("freg", 229), ("freg", 230), ("freg", 231), ("freg", 232),
    ("freg", 233), ("freg", 234), ("freg", 235), ("freg", 236), ("freg", 237), ("freg", 238), ("freg", 239), ("freg", 240),
    ("freg", 241), ("freg", 242), ("freg", 243), ("freg", 244), ("freg", 245), ("freg", 246), ("freg", 247), ("freg", 248),
    ("freg", 249), ("freg", 250), ("freg", 251), ("freg", 252), ("freg", 253), ("freg", 254), ("freg", 255)
)

output = b''

def p(x):
    global output
    output += x

def encode_reg(r):
    assert(r[0] == 'reg')
    p(struct.pack('B', r[1]))

def encode_freg(r):
    assert(r[0] == 'freg')
    p(struct.pack('B', r[1]))

def encode_litu8(l):
    assert(type(l) == int)
    p(struct.pack('B', l))

def encode_litu16(l):
    assert(type(l) == int)
    p(struct.pack('!H', l))

def threeop(op, dst, lhs, rhs):
    encode_litu8(op)
    encode_reg(dst)
    encode_reg(lhs)
    encode_reg(rhs)

def threefop(op, dst, lhs, rhs):
    encode_litu8(op)
    encode_freg(dst)
    encode_freg(lhs)
    encode_freg(rhs)


def add(dst, lhs, rhs): threeop(OP_ADD, dst, lhs, rhs)
def sub(dst, lhs, rhs): threeop(OP_SUB, dst, lhs, rhs)
def div(dst, lhs, rhs): threeop(OP_DIV, dst, lhs, rhs)
def mul(dst, lhs, rhs): threeop(OP_MUL, dst, lhs, rhs)
def band(dst, lhs, rhs): threeop(OP_BIT_AND, dst, lhs, rhs)
def bor(dst, lhs, rhs): threeop(OP_BIT_OR, dst, lhs, rhs)

def fadd(dst, lhs, rhs): threefop(OP_FADD, dst, lhs, rhs)
def fsub(dst, lhs, rhs): threefop(OP_FSUB, dst, lhs, rhs)
def fdiv(dst, lhs, rhs): threefop(OP_FDIV, dst, lhs, rhs)
def fmul(dst, lhs, rhs): threefop(OP_FMUL, dst, lhs, rhs)

def encodeloadstore(loadtype, dst, addr, offset = 0):
    encode_litu8(loadtype)
    encode_reg(dst)
    encode_reg(addr)
    encode_litu8(offset)

def load8(dst, src, offset = 0): encodeloadstore(OP_LOAD_BYTE, dst, src, offset)
def load16(dst, src, offset = 0): encodeloadstore(OP_LOAD_2BYTE, dst, src, offset)
def load32(dst, src, offset = 0): encodeloadstore(OP_LOAD_4BYTE, dst, src, offset)
def loadw(dst, src, offset = 0): encodeloadstore(OP_LOAD_WORD, dst, src, offset)

def encode_immload(loadtype, dst, value):
    encode_litu8(loadtype)
    encode_reg(dst)
    encode_litu16(value)

def loadslimm(dst, value): encode_immload(OP_LOAD_SLIMM, dst, value)
def loadulimm(dst, value): encode_immload(OP_LOAD_ULIMM, dst, value)
def oruuimm(dst, value): encode_immload(OP_OR_UUIMM, dst, value)

def store8(dst, src, offset = 0): encodeloadstore(OP_STORE_BYTE, dst, src, offset)
def store16(dst, src, offset = 0): encodeloadstore(OP_STORE_2BYTE, dst, src, offset)
def store32(dst, src, offset = 0): encodeloadstore(OP_STORE_4BYTE, dst, src, offset)
def storew(dst, src, offset = 0): encodeloadstore(OP_STORE_WORD, dst, src, offset)

def regcall(reg):
    encode_litu8(OP_REGCALL)
    encode_reg(reg)
    encode_litu16(0)

def relcall(reg, offset):
    encode_litu8(OP_RELCALL)
    encode_reg(reg)
    encode_litu16(offset)

def encode_reljump(op, reg, offset):
    encode_litu8(op)
    encode_reg(reg)
    encode_litu16(offset)

def reljump_if0(reg, offset): encode_reljump(OP_RELJUMP_IF0, reg, offset)
def reljump_iflt0(reg, offset): encode_reljump(OP_RELJUMP_IFLT0, reg, offset)
def reljump_ifgt0(reg, offset): encode_reljump(OP_RELJUMP_IFGT0, reg, offset)
def reljump_iflte0(reg, offset): encode_reljump(OP_RELJUMP_IFLTE0, reg, offset)
def reljump_ifgte0(reg, offset): encode_reljump(OP_RELJUMP_IFGTE0, reg, offset)

def syscall():
    encode_litu8(OP_SYSCALL)
    encode_litu8(0)
    encode_litu16(0)

def done():
    hexdump.hexdump(output)
    open('out.bin', 'wb').write(output)
