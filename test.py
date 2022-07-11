
from asm import *

loadw(r10, r10, 4)
loadslimm(r11, 0x8321)
oruuimm(r11, 0x0234)
store32(r11, r10, 0)

load32(r20, r10, 1)

syscall()

done()
