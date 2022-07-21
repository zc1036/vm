
from asm import *

loadregs(r6, r10, r20)

loadulimm(r4, 400)
storeregs(r4, r10, r20)

loadregs(r4, r100, r110)

syscall()

done()
